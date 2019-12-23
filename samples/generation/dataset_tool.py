# Copyright (c) 2018, NVIDIA CORPORATION. All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
#
# Additionally created on Mon Oct 15 2019
# Purpose: to generate tfrecord data of K-Face

import os
import sys
import glob
import re
import argparse
import threading
import six.moves.queue as Queue
import traceback
import numpy as np
import tensorflow as tf
import PIL.Image

#----------------------------------------------------------------------------

def error(msg):
    print('Error: ' + msg)
    exit(1)

#----------------------------------------------------------------------------

class TFRecordExporter:
    def __init__(self, tfrecord_dir, expected_images, print_progress=True, progress_interval=10):
        self.tfrecord_dir       = tfrecord_dir
        
        if os.path.basename(self.tfrecord_dir) != 'kface':
            os.mkdir(os.path.join(self.tfrecord_dir, 'kface'))
            self.tfrecord_dir = os.path.join(self.tfrecord_dir, 'kface')
        
        self.tfr_prefix         = os.path.join(self.tfrecord_dir, os.path.basename(self.tfrecord_dir))
        self.expected_images    = expected_images
        self.cur_images         = 0
        self.shape              = None
        self.resolution_log2    = None
        self.tfr_writers        = []
        self.print_progress     = print_progress
        self.progress_interval  = progress_interval
        if self.print_progress:
            print('Creating dataset "%s"' % tfrecord_dir)
        if not os.path.isdir(self.tfrecord_dir):
            os.makedirs(self.tfrecord_dir)
        assert(os.path.isdir(self.tfrecord_dir))
        
        
    def close(self):
        if self.print_progress:
            print('%-40s\r' % 'Flushing data...', end='', flush=True)
        for tfr_writer in self.tfr_writers:
            tfr_writer.close()
        self.tfr_writers = []
        if self.print_progress:
            print('%-40s\r' % '', end='', flush=True)
            print('Added %d images.' % self.cur_images)

    def choose_shuffled_order(self): # Note: Images and labels must be added in shuffled order.
        order = np.arange(self.expected_images)
        np.random.RandomState(123).shuffle(order)
        return order

    def add_image(self, img):
        if self.print_progress and self.cur_images % self.progress_interval == 0:
            print('%d / %d\r' % (self.cur_images, self.expected_images), end='', flush=True)
        if self.shape is None:
            self.shape = img.shape
            self.resolution_log2 = int(np.log2(self.shape[1]))
            assert self.shape[0] in [1, 3]
            assert self.shape[1] == self.shape[2]
            assert self.shape[1] == 2**self.resolution_log2
            tfr_opt = tf.python_io.TFRecordOptions(tf.python_io.TFRecordCompressionType.NONE)
            for lod in range(self.resolution_log2 - 1):
                tfr_file = self.tfr_prefix + '-r%02d.tfrecords' % (self.resolution_log2 - lod)
                self.tfr_writers.append(tf.python_io.TFRecordWriter(tfr_file, tfr_opt))
        assert img.shape == self.shape
        for lod, tfr_writer in enumerate(self.tfr_writers):
            if lod:
                img = img.astype(np.float32)
                img = (img[:, 0::2, 0::2] + img[:, 0::2, 1::2] + img[:, 1::2, 0::2] + img[:, 1::2, 1::2]) * 0.25
            quant = np.rint(img).clip(0, 255).astype(np.uint8)
            ex = tf.train.Example(features=tf.train.Features(feature={
                'shape': tf.train.Feature(int64_list=tf.train.Int64List(value=quant.shape)),
                'data': tf.train.Feature(bytes_list=tf.train.BytesList(value=[quant.tostring()]))}))
            tfr_writer.write(ex.SerializeToString())
        self.cur_images += 1

    def add_labels(self, labels):
        if self.print_progress:
            print('%-40s\r' % 'Saving labels...', end='', flush=True)
        assert labels.shape[0] == self.cur_images
        with open(self.tfr_prefix + '-rxx.labels', 'wb') as f:
            np.save(f, labels.astype(np.float32))
            
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()

#----------------------------------------------------------------------------

class ExceptionInfo(object):
    def __init__(self):
        self.value = sys.exc_info()[1]
        self.traceback = traceback.format_exc()

#----------------------------------------------------------------------------

class WorkerThread(threading.Thread):
    def __init__(self, task_queue):
        threading.Thread.__init__(self)
        self.task_queue = task_queue

    def run(self):
        while True:
            func, args, result_queue = self.task_queue.get()
            if func is None:
                break
            try:
                result = func(*args)
            except:
                result = ExceptionInfo()
            result_queue.put((result, args))

#----------------------------------------------------------------------------

class ThreadPool(object):
    def __init__(self, num_threads):
        assert num_threads >= 1
        self.task_queue = Queue.Queue()
        self.result_queues = dict()
        self.num_threads = num_threads
        for idx in range(self.num_threads):
            thread = WorkerThread(self.task_queue)
            thread.daemon = True
            thread.start()

    def add_task(self, func, args=()):
        assert hasattr(func, '__call__') # must be a function
        if func not in self.result_queues:
            self.result_queues[func] = Queue.Queue()
        self.task_queue.put((func, args, self.result_queues[func]))

    def get_result(self, func): # returns (result, args)
        result, args = self.result_queues[func].get()
        if isinstance(result, ExceptionInfo):
            print('\n\nWorker thread caught an exception:\n' + result.traceback)
            raise result.value
        return result, args

    def finish(self):
        for idx in range(self.num_threads):
            self.task_queue.put((None, (), None))

    def __enter__(self): # for 'with' statement
        return self

    def __exit__(self, *excinfo):
        self.finish()

    def process_items_concurrently(self, item_iterator, process_func=lambda x: x, pre_func=lambda x: x, post_func=lambda x: x, max_items_in_flight=None):
        if max_items_in_flight is None: max_items_in_flight = self.num_threads * 4
        assert max_items_in_flight >= 1
        results = []
        retire_idx = [0]

        def task_func(prepared, idx):
            return process_func(prepared)
           
        def retire_result():
            processed, (prepared, idx) = self.get_result(task_func)
            results[idx] = processed
            while retire_idx[0] < len(results) and results[retire_idx[0]] is not None:
                yield post_func(results[retire_idx[0]])
                results[retire_idx[0]] = None
                retire_idx[0] += 1
    
        for idx, item in enumerate(item_iterator):
            prepared = pre_func(item)
            results.append(None)
            self.add_task(func=task_func, args=(prepared, idx))
            while retire_idx[0] < idx - max_items_in_flight + 2:
                for res in retire_result(): yield res
        while retire_idx[0] < len(results):
            for res in retire_result(): yield res

#----------------------------------------------------------------------------

def create_kface(tfrecord_dir, kface_image_dir, session, light, emotion, camera, resolution, resize_val, bbox, shuffle):
    
    
    print('Loading images from "%s"' % kface_image_dir)
    
    resolution_nm = resolution + '_Resolution'
    
    # Extract whole subject's dir name
    pth_subj_data = [];
    pth_subj_data = sorted(glob.glob(os.path.join(kface_image_dir, resolution_nm, '*')))
    len_subj_data = len(pth_subj_data)
    
    filenames = list()
    if bbox == 'Y':
        txtnames = list()
    
    for idx in range(0, len_subj_data):
        tmp_nm = [];
        tmp_nm = glob.glob(os.path.join(pth_subj_data[idx], session, light, emotion, camera+'.jpg'))
        filenames.append(tmp_nm)
        
        if bbox == 'Y':
            txt_nm = []
            txt_nm = glob.glob(os.path.join(pth_subj_data[idx], session, light, emotion, camera+'.txt'))
            txtnames.append(txt_nm)
    
    if len(filenames) == 0:
        error('No input images found')
    tmp_fname = []
    tmp_fname = filenames[0]
    img = np.asarray(PIL.Image.open(tmp_fname[0]))
    
    channels = img.shape[2] if img.ndim == 3 else 1
    
    with TFRecordExporter(tfrecord_dir, len(filenames)) as tfr:
        order = tfr.choose_shuffled_order() if shuffle else np.arange(len(filenames))
        for idx in range(order.size):

            if bbox == 'Y':
                # Extract bounding box value
                txt_f = open(txtnames[order[idx]][0])
                txt_lines = txt_f.readlines()
                txt8 = re.split(r'(\t|\n)\s*', txt_lines[7])
                x = int(txt8[0]); y = int(txt8[2]); w = int(txt8[4]); h = int(txt8[6])
                img_tmp = []; img_resized = [];
                img_tmp= PIL.Image.open(filenames[order[idx]][0]).crop((x,y,x+w,y+h))
            else:
                img_tmp = []; img_resized = [];
                img_tmp = PIL.Image.open(filenames[order[idx]][0])
            
            # Resize image
            img_resized = img_tmp.resize((resize_val,resize_val))
            img = np.asarray(img_resized)
            
            if channels == 1:
                img = img[np.newaxis, :, :] # HW => CHW
            else:
                img = img.transpose(2, 0, 1) # HWC => CHW
            tfr.add_image(img)
            
#----------------------------------------------------------------------------

def execute_cmdline(argv):
    prog = argv[0]
    parser = argparse.ArgumentParser(
        prog        = prog,
        description = 'Tool for creating Progressive GAN datasets.',
        epilog      = 'Type "%s <command> -h" for more information.' % prog)
        
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    def add_command(cmd, desc, example=None):
        epilog = 'Example: %s %s' % (prog, example) if example is not None else None
        return subparsers.add_parser(cmd, description=desc, help=desc, epilog=epilog)

    p = add_command(    'create_kface', 'Create dataset from a directory full of K-Face images.',
                                            'create_kface datasets/my/tfrecord/dir my/image/dir')
    p.add_argument(     'tfrecord_dir',     help='New tfrecord dataset directory to be created')
    p.add_argument(     'kface_image_dir',  help='Directory containing the K-Face images')
    p.add_argument(     '--session',        help='Select one session type [S001~S006] (default: S001)', type=str, default='S001')
    p.add_argument(     '--light',          help='Select one light type [L1~L30] (default: L1)', type=str, default='L1')
    p.add_argument(     '--emotion',        help='Select one emotion type [E01, E02, E03] (default: E01)', type=str, default='E01')
    p.add_argument(     '--camera',         help='Select one camera(degree) type [C1~C20] (default: C7)', type=str, default='C7')
    p.add_argument(     '--resolution',     help='Select resolution type. Input one of three types: High, Middle, Low (default: High)', type=str, default='High')
    p.add_argument(     '--resize_val',     help='Input resizing value (should be power of 2). (default: 512)', type=int, default=512)
    p.add_argument(     '--bbox',           help='Check whether using bbox info or not (Y/N). (default: Y)', type=str, default='Y')
    p.add_argument(     '--shuffle',        help='Randomize image order (default: 1)', type=int, default=1)


    args = parser.parse_args(argv[1:] if len(argv) > 1 else ['-h'])
    func = globals()[args.command]
    del args.command
    func(**vars(args))

#----------------------------------------------------------------------------

if __name__ == "__main__":
    execute_cmdline(sys.argv)

#----------------------------------------------------------------------------
