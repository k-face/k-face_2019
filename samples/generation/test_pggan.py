import os
import sys
import argparse
import pickle
import numpy as np
import tensorflow as tf
import PIL.Image


def test_img_pggan(pkl_path, save_dir, pick_latents):
    
    # Initialize TensorFlow session.
    tf.InteractiveSession()
    
    # Import trained network(.pkl).
    with open(pkl_path, 'rb') as file:
        G, D, Gs = pickle.load(file)
    
    # Generate latent vectors.
    latents = np.random.RandomState(1000).randn(1000, *Gs.input_shapes[0][1:])
    tmp_latent = []; tmp_latent = pick_latents.split(',')
    tmp_pick_latents = [];
    
    for idx in range(len(tmp_latent)):
        tmp_pick_latents.append(int(tmp_latent[idx]))
    
    latents = latents[tmp_pick_latents] # pick latent numbers
    
    # Generate dummy labels (not used by the official networks).
    labels = np.zeros([latents.shape[0]] + Gs.input_shapes[1][1:])
    
    # Run the generator to produce a set of images.
    images = Gs.run(latents, labels)
    
    # Convert images to PIL-compatible format.
    images = np.clip(np.rint((images + 1.0) / 2.0 * 255.0), 0.0, 255.0).astype(np.uint8) # [-1,1] => [0,255]
    images = images.transpose(0, 2, 3, 1) # NCHW => NHWC
    
    # Save images as PNG.
    for idx in range(images.shape[0]):
        imagenm = []; imagenm = os.path.join(save_dir, 'img'+str(idx)+'.png')
        PIL.Image.fromarray(images[idx], 'RGB').save(imagenm)

def execute_cmdline(argv):
    prog = argv[0]
    parser = argparse.ArgumentParser(
        prog        = prog,
        description = 'Tool for process trained GAN model and generate new images.',
        epilog      = 'Type "%s <command> -h" for more information.' % prog)
        
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    def add_command(cmd, desc, example=None):
        epilog = 'Example: %s %s' % (prog, example) if example is not None else None
        return subparsers.add_parser(cmd, description=desc, help=desc, epilog=epilog)

    p = add_command(    'test_img_pggan', 'Generate example images from trained network.',
                                            'test_img_pggan datasets/my/pkl/path my/saving/dir')
    p.add_argument(     'pkl_path',     help='Input pkl data path including pkl file name')
    p.add_argument(     'save_dir',  help='Directory for saving generated sample images')
    p.add_argument(     '--pick_latents',     help='Pick latent values to generate images (default: 0,1,90,99)', type=str, default='0,1,90,99')
    

    args = parser.parse_args(argv[1:] if len(argv) > 1 else ['-h'])
    func = globals()[args.command]
    del args.command
    func(**vars(args))

#----------------------------------------------------------------------------

if __name__ == "__main__":
    execute_cmdline(sys.argv)

#----------------------------------------------------------------------------
