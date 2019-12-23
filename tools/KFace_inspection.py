# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 12:03:20 2019

@purpose: to inspect the data (check around 100 figures at once; same conditions)
"""

import numpy as np
import glob
import os
import cv2

import sys
import argparse

# Only for 100 subjects data inspection
def data_inspection(root_dir, resolution, session, light, emotion, camera):
    
    
    print('Loading images from "%s"' % root_dir)
    
    resolution_nm = resolution + '_Resolution'
    full_dir_pth = root_dir + resolution_nm
    
    # extract total folder name
    totfold = sorted(glob.glob(os.path.join(full_dir_pth, '*')))
    
    totfoldlength = len(totfold)/100

    totfoldnm = list()
    totfoldpth = list()
    
    for foldidx in range(0, len(totfold)):
        foldtmp = []; foldtmp = totfold[foldidx].split('/')
        totfoldnm.append(foldtmp[-1])
        totfoldpth.append(foldtmp)
    
    if camera == 'all':
    
        for camidx in range(1, 21):
            camnm = []
            camnm = 'C'+str(camidx)+'.jpg'
            
            opnimg1 = list(); opnimg2 = list(); opnimg3 = list(); opnimg4 = list(); opnimg5 = list()
            opnimg6 = list(); opnimg7 = list(); opnimg8 = list(); opnimg9 = list(); opnimg10 = list()
            
            count = 0
            current_pth = session + '_' + light +'_' + emotion +'_' + camnm
            
            for totfoldidx in range(1, len(totfoldpth)):
                
                if totfoldlength == 0:
                    break

                fullpth = []; tmpimg = []
                fullpth = glob.glob(os.path.join(full_dir_pth, totfoldnm[totfoldidx], session, light, emotion, camnm))
                tmpimg = cv2.imread(fullpth[0], cv2.IMREAD_COLOR)
                
                
                if count < 10:
                    opnimg1.append(tmpimg)
                    count += 1
                elif count>=10 and count<20:
                    opnimg2.append(tmpimg)
                    count+=1
                elif count>=20 and count<30:
                    opnimg3.append(tmpimg)
                    count+=1
                elif count>=30 and count<40:
                    opnimg4.append(tmpimg)
                    count+=1
                elif count>=40 and count<50:
                    opnimg5.append(tmpimg)
                    count+=1
                elif count>=50 and count<60:
                    opnimg6.append(tmpimg)
                    count+=1
                elif count>=60 and count<70:
                    opnimg7.append(tmpimg)
                    count+=1
                elif count>=70 and count<80:
                    opnimg8.append(tmpimg)
                    count+=1
                elif count>=80 and count<90:
                    opnimg9.append(tmpimg)
                    count+=1
                elif count>=90 and count<100:
                    opnimg10.append(tmpimg)
                    count+=1
                    
                if count == 100:
                    concat1 = np.concatenate((opnimg1[0], opnimg1[1], opnimg1[2], opnimg1[3], opnimg1[4], opnimg1[5], opnimg1[6], opnimg1[7], opnimg1[8], opnimg1[9]))
                    concat2 = np.concatenate((opnimg2[0], opnimg2[1], opnimg2[2], opnimg2[3], opnimg2[4], opnimg2[5], opnimg2[6], opnimg2[7], opnimg2[8], opnimg2[9]))
                    concat3 = np.concatenate((opnimg3[0], opnimg3[1], opnimg3[2], opnimg3[3], opnimg3[4], opnimg3[5], opnimg3[6], opnimg3[7], opnimg3[8], opnimg3[9]))
                    concat4 = np.concatenate((opnimg4[0], opnimg4[1], opnimg4[2], opnimg4[3], opnimg4[4], opnimg4[5], opnimg4[6], opnimg4[7], opnimg4[8], opnimg4[9]))
                    concat5 = np.concatenate((opnimg5[0], opnimg5[1], opnimg5[2], opnimg5[3], opnimg5[4], opnimg5[5], opnimg5[6], opnimg5[7], opnimg5[8], opnimg5[9]))
                    concat6 = np.concatenate((opnimg6[0], opnimg6[1], opnimg6[2], opnimg6[3], opnimg6[4], opnimg6[5], opnimg6[6], opnimg6[7], opnimg6[8], opnimg6[9]))
                    concat7 = np.concatenate((opnimg7[0], opnimg7[1], opnimg7[2], opnimg7[3], opnimg7[4], opnimg7[5], opnimg7[6], opnimg7[7], opnimg7[8], opnimg7[9]))
                    concat8 = np.concatenate((opnimg8[0], opnimg8[1], opnimg8[2], opnimg8[3], opnimg8[4], opnimg8[5], opnimg8[6], opnimg8[7], opnimg8[8], opnimg8[9]))
                    concat9 = np.concatenate((opnimg9[0], opnimg9[1], opnimg9[2], opnimg9[3], opnimg9[4], opnimg9[5], opnimg9[6], opnimg9[7], opnimg9[8], opnimg9[9]))
                    concat10 = np.concatenate((opnimg10[0], opnimg10[1], opnimg10[2], opnimg10[3], opnimg10[4], opnimg10[5], opnimg10[6], opnimg10[7], opnimg10[8], opnimg10[9]))
                    
                    vertical_image = np.concatenate((concat1, concat2, concat3, concat4, concat5, concat6, concat7, concat8, concat9, concat10), axis = 1)
                    
                    print("==========================================")
                    print(current_pth)
            
                    real_vertical_image = cv2.resize(vertical_image, (1870, 1000))
    
                    cv2.imshow('img', real_vertical_image)
                    cv2.waitKey(0)
                    count = 0
                    opnimg1 = list(); opnimg2 = list(); opnimg3 = list(); opnimg4 = list(); opnimg5 = list()
                    opnimg6 = list(); opnimg7 = list(); opnimg8 = list(); opnimg9 = list(); opnimg10 = list()

                    totfoldlength -= 1
    else:
        
        
        count = 0
        opnimg1 = list(); opnimg2 = list(); opnimg3 = list(); opnimg4 = list(); opnimg5 = list()
        opnimg6 = list(); opnimg7 = list(); opnimg8 = list(); opnimg9 = list(); opnimg10 = list()
        
        
        for totfoldidx in range(1, len(totfoldpth)):

            if totfoldlength == 0:
                break

            current_pth = []
            current_pth = session + '_' + light +'_' + emotion + '_' + camera + '.jpg'
            camera_jpg = camera+'.jpg' 


            fullpth = []; tmpimg = []; xsize = []; ysize = []; shrinkimg = []
            fullpth = glob.glob(os.path.join(full_dir_pth, totfoldnm[totfoldidx], session, light, emotion, camera_jpg))
            tmpimg = cv2.imread(fullpth[0], cv2.IMREAD_COLOR)
            
            
            if count < 10:
                opnimg1.append(tmpimg)
                count += 1
            elif count>=10 and count<20:
                opnimg2.append(tmpimg)
                count+=1
            elif count>=20 and count<30:
                opnimg3.append(tmpimg)
                count+=1
            elif count>=30 and count<40:
                opnimg4.append(tmpimg)
                count+=1
            elif count>=40 and count<50:
                opnimg5.append(tmpimg)
                count+=1
            elif count>=50 and count<60:
                opnimg6.append(tmpimg)
                count+=1
            elif count>=60 and count<70:
                opnimg7.append(tmpimg)
                count+=1
            elif count>=70 and count<80:
                opnimg8.append(tmpimg)
                count+=1
            elif count>=80 and count<90:
                opnimg9.append(tmpimg)
                count+=1
            elif count>=90 and count<100:
                opnimg10.append(tmpimg)
                count+=1
                
            if count == 100:
                concat1 = np.concatenate((opnimg1[0], opnimg1[1], opnimg1[2], opnimg1[3], opnimg1[4], opnimg1[5], opnimg1[6], opnimg1[7], opnimg1[8], opnimg1[9]))
                concat2 = np.concatenate((opnimg2[0], opnimg2[1], opnimg2[2], opnimg2[3], opnimg2[4], opnimg2[5], opnimg2[6], opnimg2[7], opnimg2[8], opnimg2[9]))
                concat3 = np.concatenate((opnimg3[0], opnimg3[1], opnimg3[2], opnimg3[3], opnimg3[4], opnimg3[5], opnimg3[6], opnimg3[7], opnimg3[8], opnimg3[9]))
                concat4 = np.concatenate((opnimg4[0], opnimg4[1], opnimg4[2], opnimg4[3], opnimg4[4], opnimg4[5], opnimg4[6], opnimg4[7], opnimg4[8], opnimg4[9]))
                concat5 = np.concatenate((opnimg5[0], opnimg5[1], opnimg5[2], opnimg5[3], opnimg5[4], opnimg5[5], opnimg5[6], opnimg5[7], opnimg5[8], opnimg5[9]))
                concat6 = np.concatenate((opnimg6[0], opnimg6[1], opnimg6[2], opnimg6[3], opnimg6[4], opnimg6[5], opnimg6[6], opnimg6[7], opnimg6[8], opnimg6[9]))
                concat7 = np.concatenate((opnimg7[0], opnimg7[1], opnimg7[2], opnimg7[3], opnimg7[4], opnimg7[5], opnimg7[6], opnimg7[7], opnimg7[8], opnimg7[9]))
                concat8 = np.concatenate((opnimg8[0], opnimg8[1], opnimg8[2], opnimg8[3], opnimg8[4], opnimg8[5], opnimg8[6], opnimg8[7], opnimg8[8], opnimg8[9]))
                concat9 = np.concatenate((opnimg9[0], opnimg9[1], opnimg9[2], opnimg9[3], opnimg9[4], opnimg9[5], opnimg9[6], opnimg9[7], opnimg9[8], opnimg9[9]))
                concat10 = np.concatenate((opnimg10[0], opnimg10[1], opnimg10[2], opnimg10[3], opnimg10[4], opnimg10[5], opnimg10[6], opnimg10[7], opnimg10[8], opnimg10[9]))
                
                vertical_image = np.concatenate((concat1, concat2, concat3, concat4, concat5, concat6, concat7, concat8, concat9, concat10), axis = 1)
                
                print("==========================================")
                print(current_pth)
        
                real_vertical_image = cv2.resize(vertical_image, (1870, 1000))
    
                cv2.imshow('img', real_vertical_image)
                cv2.waitKey(0)
                opnimg1 = list(); opnimg2 = list(); opnimg3 = list(); opnimg4 = list(); opnimg5 = list()
                opnimg6 = list(); opnimg7 = list(); opnimg8 = list(); opnimg9 = list(); opnimg10 = list()
                totfoldlength -= 1
                count = 0



# Only for 100 subjects bounding box inspection
def bbox(root_dir, resolution, light, camera):
    
    print('Loading bounding box images from "%s"' % root_dir)
    
    resolution_nm = resolution + '_Resolution'
    full_dir_pth = os.path.join(root_dir, resolution_nm)
    
    session = 'S001'; emotion = 'E01'
    
    totfold = sorted(glob.glob(os.path.join(full_dir_pth, '*')))
    
    # extract total folder name
    totfoldnm = list()
    totfoldpth = list()
    
    totfoldlength = len(totfold)/100
    
    for foldidx in range(0, len(totfold)):
        foldtmp = []; foldtmp = totfold[foldidx].split('/')
        totfoldnm.append(foldtmp[-1])
        totfoldpth.append(foldtmp)
    
    if camera == 'all':
        for camidx in range(1, 21):
            camnm = []
            camnm = 'C'+str(camidx)+'.jpg'
            camnm_txt = 'C'+str(camidx)+'.txt'
            
            opnimg1 = list(); opnimg2 = list(); opnimg3 = list(); opnimg4 = list(); opnimg5 = list()
            opnimg6 = list(); opnimg7 = list(); opnimg8 = list(); opnimg9 = list(); opnimg10 = list()
            
            count = 0
            current_pth = session + '_' + light +'_' + emotion +'_' + camnm
            
            for totfoldidx in range(1, len(totfoldpth)):
                
                if totfoldlength == 0:
                    break

                fullpth = []; tmpimg = []; xsize = []; ysize = []; shrinkimg = []
                fullpth = glob.glob(os.path.join(full_dir_pth, totfoldnm[totfoldidx], session, light, emotion, camnm))
                tmpimg = cv2.imread(fullpth[0], cv2.IMREAD_COLOR)
                
                bbox_pth = glob.glob(os.path.join(full_dir_pth, totfoldnm[totfoldidx], session, light, emotion, camnm_txt))
                bbox_f = open(bbox_pth[0], "r")
                
                bbox_info_tot = bbox_f.readlines()
                
                for splitidx in range(7, len(bbox_info_tot)):
                    
                    bbsplit_tmp = bbox_info_tot[splitidx].replace('/t','/n')
                    bbox_info_split = bbsplit_tmp.split()
                    x = 0; y = 0; w = 0; h = 0
                    x = int(bbox_info_split[0])
                    y = int(bbox_info_split[1])
                    w = int(bbox_info_split[2])
                    h = int(bbox_info_split[3])
                    
                    cv2.rectangle(tmpimg, (x,y,w,h), (255,255,00), 12)
                
                
                if count < 10:
                    opnimg1.append(tmpimg)
                    count += 1
                elif count>=10 and count<20:
                    opnimg2.append(tmpimg)
                    count+=1
                elif count>=20 and count<30:
                    opnimg3.append(tmpimg)
                    count+=1
                elif count>=30 and count<40:
                    opnimg4.append(tmpimg)
                    count+=1
                elif count>=40 and count<50:
                    opnimg5.append(tmpimg)
                    count+=1
                elif count>=50 and count<60:
                    opnimg6.append(tmpimg)
                    count+=1
                elif count>=60 and count<70:
                    opnimg7.append(tmpimg)
                    count+=1
                elif count>=70 and count<80:
                    opnimg8.append(tmpimg)
                    count+=1
                elif count>=80 and count<90:
                    opnimg9.append(tmpimg)
                    count+=1
                elif count>=90 and count<100:
                    opnimg10.append(tmpimg)
                    count+=1
                    
                if count == 100:
                    concat1 = np.concatenate((opnimg1[0], opnimg1[1], opnimg1[2], opnimg1[3], opnimg1[4], opnimg1[5], opnimg1[6], opnimg1[7], opnimg1[8], opnimg1[9]))
                    concat2 = np.concatenate((opnimg2[0], opnimg2[1], opnimg2[2], opnimg2[3], opnimg2[4], opnimg2[5], opnimg2[6], opnimg2[7], opnimg2[8], opnimg2[9]))
                    concat3 = np.concatenate((opnimg3[0], opnimg3[1], opnimg3[2], opnimg3[3], opnimg3[4], opnimg3[5], opnimg3[6], opnimg3[7], opnimg3[8], opnimg3[9]))
                    concat4 = np.concatenate((opnimg4[0], opnimg4[1], opnimg4[2], opnimg4[3], opnimg4[4], opnimg4[5], opnimg4[6], opnimg4[7], opnimg4[8], opnimg4[9]))
                    concat5 = np.concatenate((opnimg5[0], opnimg5[1], opnimg5[2], opnimg5[3], opnimg5[4], opnimg5[5], opnimg5[6], opnimg5[7], opnimg5[8], opnimg5[9]))
                    concat6 = np.concatenate((opnimg6[0], opnimg6[1], opnimg6[2], opnimg6[3], opnimg6[4], opnimg6[5], opnimg6[6], opnimg6[7], opnimg6[8], opnimg6[9]))
                    concat7 = np.concatenate((opnimg7[0], opnimg7[1], opnimg7[2], opnimg7[3], opnimg7[4], opnimg7[5], opnimg7[6], opnimg7[7], opnimg7[8], opnimg7[9]))
                    concat8 = np.concatenate((opnimg8[0], opnimg8[1], opnimg8[2], opnimg8[3], opnimg8[4], opnimg8[5], opnimg8[6], opnimg8[7], opnimg8[8], opnimg8[9]))
                    concat9 = np.concatenate((opnimg9[0], opnimg9[1], opnimg9[2], opnimg9[3], opnimg9[4], opnimg9[5], opnimg9[6], opnimg9[7], opnimg9[8], opnimg9[9]))
                    concat10 = np.concatenate((opnimg10[0], opnimg10[1], opnimg10[2], opnimg10[3], opnimg10[4], opnimg10[5], opnimg10[6], opnimg10[7], opnimg10[8], opnimg10[9]))
                    
                    vertical_image = np.concatenate((concat1, concat2, concat3, concat4, concat5, concat6, concat7, concat8, concat9, concat10), axis = 1)
                    
                    print("==========================================")
                    print(current_pth)
            
                    real_vertical_image = cv2.resize(vertical_image, (1870, 1000))
    
                    cv2.imshow('img', real_vertical_image)
                    cv2.waitKey(0)
                    
                    opnimg1 = list(); opnimg2 = list(); opnimg3 = list(); opnimg4 = list(); opnimg5 = list()
                    opnimg6 = list(); opnimg7 = list(); opnimg8 = list(); opnimg9 = list(); opnimg10 = list()
                    
                    totfoldlength -= 1
                    count = 0

    else:
        
        count = 0
        opnimg1 = list(); opnimg2 = list(); opnimg3 = list(); opnimg4 = list(); opnimg5 = list()
        opnimg6 = list(); opnimg7 = list(); opnimg8 = list(); opnimg9 = list(); opnimg10 = list()
            
        for totfoldidx in range(1, len(totfoldpth)): 
                       
            current_pth = []
            current_pth = session + '_' + light +'_' + emotion + '_' + camera + '.jpg'
            camera_jpg = camera+'.jpg'
            camnm_txt = camera+'.txt'
    
            
            fullpth = []; tmpimg = []; xsize = []; ysize = []; shrinkimg = []
            fullpth = glob.glob(os.path.join(full_dir_pth, totfoldnm[totfoldidx], session, light, emotion, camera_jpg))
            tmpimg = cv2.imread(fullpth[0], cv2.IMREAD_COLOR)
    
            bbox_pth = glob.glob(os.path.join(full_dir_pth, totfoldnm[totfoldidx], session, light, emotion, camnm_txt))
            bbox_f = open(bbox_pth[0], "r")
            
            bbox_info_tot = bbox_f.readlines()
            
            for splitidx in range(7, len(bbox_info_tot)):
                
                bbsplit_tmp = bbox_info_tot[splitidx].replace('/t','/n')
                bbox_info_split = bbsplit_tmp.split()
                x = 0; y = 0; w = 0; h = 0
                x = int(bbox_info_split[0])
                y = int(bbox_info_split[1])
                w = int(bbox_info_split[2])
                h = int(bbox_info_split[3])
                
                cv2.rectangle(tmpimg, (x,y,w,h), (255,255,00), 12)
            
    
            if count < 10:
                opnimg1.append(tmpimg)
                count += 1
            elif count>=10 and count<20:
                opnimg2.append(tmpimg)
                count+=1
            elif count>=20 and count<30:
                opnimg3.append(tmpimg)
                count+=1
            elif count>=30 and count<40:
                opnimg4.append(tmpimg)
                count+=1
            elif count>=40 and count<50:
                opnimg5.append(tmpimg)
                count+=1
            elif count>=50 and count<60:
                opnimg6.append(tmpimg)
                count+=1
            elif count>=60 and count<70:
                opnimg7.append(tmpimg)
                count+=1
            elif count>=70 and count<80:
                opnimg8.append(tmpimg)
                count+=1
            elif count>=80 and count<90:
                opnimg9.append(tmpimg)
                count+=1
            elif count>=90 and count<100:
                opnimg10.append(tmpimg)
                count+=1
                
            if count == 100:
                concat1 = np.concatenate((opnimg1[0], opnimg1[1], opnimg1[2], opnimg1[3], opnimg1[4], opnimg1[5], opnimg1[6], opnimg1[7], opnimg1[8], opnimg1[9]))
                concat2 = np.concatenate((opnimg2[0], opnimg2[1], opnimg2[2], opnimg2[3], opnimg2[4], opnimg2[5], opnimg2[6], opnimg2[7], opnimg2[8], opnimg2[9]))
                concat3 = np.concatenate((opnimg3[0], opnimg3[1], opnimg3[2], opnimg3[3], opnimg3[4], opnimg3[5], opnimg3[6], opnimg3[7], opnimg3[8], opnimg3[9]))
                concat4 = np.concatenate((opnimg4[0], opnimg4[1], opnimg4[2], opnimg4[3], opnimg4[4], opnimg4[5], opnimg4[6], opnimg4[7], opnimg4[8], opnimg4[9]))
                concat5 = np.concatenate((opnimg5[0], opnimg5[1], opnimg5[2], opnimg5[3], opnimg5[4], opnimg5[5], opnimg5[6], opnimg5[7], opnimg5[8], opnimg5[9]))
                concat6 = np.concatenate((opnimg6[0], opnimg6[1], opnimg6[2], opnimg6[3], opnimg6[4], opnimg6[5], opnimg6[6], opnimg6[7], opnimg6[8], opnimg6[9]))
                concat7 = np.concatenate((opnimg7[0], opnimg7[1], opnimg7[2], opnimg7[3], opnimg7[4], opnimg7[5], opnimg7[6], opnimg7[7], opnimg7[8], opnimg7[9]))
                concat8 = np.concatenate((opnimg8[0], opnimg8[1], opnimg8[2], opnimg8[3], opnimg8[4], opnimg8[5], opnimg8[6], opnimg8[7], opnimg8[8], opnimg8[9]))
                concat9 = np.concatenate((opnimg9[0], opnimg9[1], opnimg9[2], opnimg9[3], opnimg9[4], opnimg9[5], opnimg9[6], opnimg9[7], opnimg9[8], opnimg9[9]))
                concat10 = np.concatenate((opnimg10[0], opnimg10[1], opnimg10[2], opnimg10[3], opnimg10[4], opnimg10[5], opnimg10[6], opnimg10[7], opnimg10[8], opnimg10[9]))
                
                vertical_image = np.concatenate((concat1, concat2, concat3, concat4, concat5, concat6, concat7, concat8, concat9, concat10), axis = 1)
                
                print("==========================================")
                print(current_pth)
        
                real_vertical_image = cv2.resize(vertical_image, (1870, 1000))
    
                cv2.imshow('img', real_vertical_image)
                cv2.waitKey(0)
                
                opnimg1 = list(); opnimg2 = list(); opnimg3 = list(); opnimg4 = list(); opnimg5 = list()
                opnimg6 = list(); opnimg7 = list(); opnimg8 = list(); opnimg9 = list(); opnimg10 = list()
                totfoldlength = totfoldlength -1
                count = 0

                if totfoldlength == 0:
                    break

    
def feature_point(root_dir, resolution, light, camera):
    session = 'S001'
    emotion = 'E01'
    
    print('Loading feature point images from "%s"' % root_dir)
    
    resolution_nm = resolution + '_Resolution'
    full_dir_pth = os.path.join(root_dir, resolution_nm)
    
    # extract total folder name
    totfold = sorted(glob.glob(os.path.join(full_dir_pth, '*')))
    totfoldlength = len(totfold)/100
    totfoldnm = list()
    totfoldpth = list()
    
    for foldidx in range(0, len(totfold)):
        foldtmp = []; foldtmp = totfold[foldidx].split('/')
        totfoldnm.append(foldtmp[-1])
        totfoldpth.append(foldtmp)
        
    if camera == 'all':

        for camidx in range(1, 21):
            camnm = []
            camnm = 'C'+str(camidx)+'.jpg'
            camnm_txt = 'C'+str(camidx)+'.txt'
            
            opnimg1 = list(); opnimg2 = list(); opnimg3 = list(); opnimg4 = list(); opnimg5 = list()
            opnimg6 = list(); opnimg7 = list(); opnimg8 = list(); opnimg9 = list(); opnimg10 = list()
            
            count = 0
            current_pth = session + '_' + light +'_' + emotion +'_' + camnm
            
            for totfoldidx in range(1, len(totfoldpth)):
                
                if totfoldlength == 0:
                    break

                fullpth = []; tmpimg = []; xsize = []; ysize = []; shrinkimg = []
                fullpth = glob.glob(os.path.join(full_dir_pth, totfoldnm[totfoldidx], session, light, emotion, camnm))
                tmpimg = cv2.imread(fullpth[0], cv2.IMREAD_COLOR)
                
                bbox_pth = glob.glob(os.path.join(full_dir_pth, totfoldnm[totfoldidx], session, light, emotion, camnm_txt))
                bbox_f = open(bbox_pth[0], "r")
                
                bbox_info_tot = bbox_f.readlines()
                
                for splitidx in range(0, 7):
                    
                    bbsplit_tmp = bbox_info_tot[splitidx].replace('/t','/n')
                    bbox_info_split = bbsplit_tmp.split()
                    x = 0; y = 0
                    x = int(bbox_info_split[0])
                    y = int(bbox_info_split[1])
                    
                    cv2.circle(tmpimg, (x, y), 7, (255,255,00), 15)
                
                
                if count < 10:
                    opnimg1.append(tmpimg)
                    count += 1
                elif count>=10 and count<20:
                    opnimg2.append(tmpimg)
                    count+=1
                elif count>=20 and count<30:
                    opnimg3.append(tmpimg)
                    count+=1
                elif count>=30 and count<40:
                    opnimg4.append(tmpimg)
                    count+=1
                elif count>=40 and count<50:
                    opnimg5.append(tmpimg)
                    count+=1
                elif count>=50 and count<60:
                    opnimg6.append(tmpimg)
                    count+=1
                elif count>=60 and count<70:
                    opnimg7.append(tmpimg)
                    count+=1
                elif count>=70 and count<80:
                    opnimg8.append(tmpimg)
                    count+=1
                elif count>=80 and count<90:
                    opnimg9.append(tmpimg)
                    count+=1
                elif count>=90 and count<100:
                    opnimg10.append(tmpimg)
                    count+=1
                    
                if count == 100:
                    concat1 = np.concatenate((opnimg1[0], opnimg1[1], opnimg1[2], opnimg1[3], opnimg1[4], opnimg1[5], opnimg1[6], opnimg1[7], opnimg1[8], opnimg1[9]))
                    concat2 = np.concatenate((opnimg2[0], opnimg2[1], opnimg2[2], opnimg2[3], opnimg2[4], opnimg2[5], opnimg2[6], opnimg2[7], opnimg2[8], opnimg2[9]))
                    concat3 = np.concatenate((opnimg3[0], opnimg3[1], opnimg3[2], opnimg3[3], opnimg3[4], opnimg3[5], opnimg3[6], opnimg3[7], opnimg3[8], opnimg3[9]))
                    concat4 = np.concatenate((opnimg4[0], opnimg4[1], opnimg4[2], opnimg4[3], opnimg4[4], opnimg4[5], opnimg4[6], opnimg4[7], opnimg4[8], opnimg4[9]))
                    concat5 = np.concatenate((opnimg5[0], opnimg5[1], opnimg5[2], opnimg5[3], opnimg5[4], opnimg5[5], opnimg5[6], opnimg5[7], opnimg5[8], opnimg5[9]))
                    concat6 = np.concatenate((opnimg6[0], opnimg6[1], opnimg6[2], opnimg6[3], opnimg6[4], opnimg6[5], opnimg6[6], opnimg6[7], opnimg6[8], opnimg6[9]))
                    concat7 = np.concatenate((opnimg7[0], opnimg7[1], opnimg7[2], opnimg7[3], opnimg7[4], opnimg7[5], opnimg7[6], opnimg7[7], opnimg7[8], opnimg7[9]))
                    concat8 = np.concatenate((opnimg8[0], opnimg8[1], opnimg8[2], opnimg8[3], opnimg8[4], opnimg8[5], opnimg8[6], opnimg8[7], opnimg8[8], opnimg8[9]))
                    concat9 = np.concatenate((opnimg9[0], opnimg9[1], opnimg9[2], opnimg9[3], opnimg9[4], opnimg9[5], opnimg9[6], opnimg9[7], opnimg9[8], opnimg9[9]))
                    concat10 = np.concatenate((opnimg10[0], opnimg10[1], opnimg10[2], opnimg10[3], opnimg10[4], opnimg10[5], opnimg10[6], opnimg10[7], opnimg10[8], opnimg10[9]))
                    
                    vertical_image = np.concatenate((concat1, concat2, concat3, concat4, concat5, concat6, concat7, concat8, concat9, concat10), axis = 1)
                    
                    print("==========================================")
                    print(current_pth)
            
                    real_vertical_image = cv2.resize(vertical_image, (1870, 1000))
    
                    cv2.imshow('img', real_vertical_image)
                    cv2.waitKey(0)
                    count = 0
                    opnimg1 = list(); opnimg2 = list(); opnimg3 = list(); opnimg4 = list(); opnimg5 = list()
                    opnimg6 = list(); opnimg7 = list(); opnimg8 = list(); opnimg9 = list(); opnimg10 = list()


                    totfoldlength =- 1
    else:
        
        count = 0
        opnimg1 = list(); opnimg2 = list(); opnimg3 = list(); opnimg4 = list(); opnimg5 = list()
        opnimg6 = list(); opnimg7 = list(); opnimg8 = list(); opnimg9 = list(); opnimg10 = list()
            
        for totfoldidx in range(1, len(totfoldpth)):
            if totfoldlength == 0:
                break

            current_pth = []
            current_pth = session + '_' + light +'_' + emotion + '_' + camera + '.jpg'
            camera_jpg = camera+'.jpg'
            camnm_txt = camera+'.txt'
    
            
            fullpth = []; tmpimg = []; xsize = []; ysize = []; shrinkimg = []
            fullpth = glob.glob(os.path.join(full_dir_pth, totfoldnm[totfoldidx], session, light, emotion, camera_jpg))
            tmpimg = cv2.imread(fullpth[0], cv2.IMREAD_COLOR)
    
            bbox_pth = glob.glob(os.path.join(full_dir_pth, totfoldnm[totfoldidx], session, light, emotion, camnm_txt))
            bbox_f = open(bbox_pth[0], "r")
            
            bbox_info_tot = bbox_f.readlines()
                
            for splitidx in range(0, 7):
                
                bbsplit_tmp = bbox_info_tot[splitidx].replace('/t','/n')
                bbox_info_split = bbsplit_tmp.split()
                x = 0; y = 0
                x = int(bbox_info_split[0])
                y = int(bbox_info_split[1])
                                                
                cv2.circle(tmpimg, (x, y), 7, (255,255,00), 15)
            
    
            if count < 10:
                opnimg1.append(tmpimg)
                count += 1
            elif count>=10 and count<20:
                opnimg2.append(tmpimg)
                count+=1
            elif count>=20 and count<30:
                opnimg3.append(tmpimg)
                count+=1
            elif count>=30 and count<40:
                opnimg4.append(tmpimg)
                count+=1
            elif count>=40 and count<50:
                opnimg5.append(tmpimg)
                count+=1
            elif count>=50 and count<60:
                opnimg6.append(tmpimg)
                count+=1
            elif count>=60 and count<70:
                opnimg7.append(tmpimg)
                count+=1
            elif count>=70 and count<80:
                opnimg8.append(tmpimg)
                count+=1
            elif count>=80 and count<90:
                opnimg9.append(tmpimg)
                count+=1
            elif count>=90 and count<100:
                opnimg10.append(tmpimg)
                count+=1
                
            if count == 100:
                concat1 = np.concatenate((opnimg1[0], opnimg1[1], opnimg1[2], opnimg1[3], opnimg1[4], opnimg1[5], opnimg1[6], opnimg1[7], opnimg1[8], opnimg1[9]))
                concat2 = np.concatenate((opnimg2[0], opnimg2[1], opnimg2[2], opnimg2[3], opnimg2[4], opnimg2[5], opnimg2[6], opnimg2[7], opnimg2[8], opnimg2[9]))
                concat3 = np.concatenate((opnimg3[0], opnimg3[1], opnimg3[2], opnimg3[3], opnimg3[4], opnimg3[5], opnimg3[6], opnimg3[7], opnimg3[8], opnimg3[9]))
                concat4 = np.concatenate((opnimg4[0], opnimg4[1], opnimg4[2], opnimg4[3], opnimg4[4], opnimg4[5], opnimg4[6], opnimg4[7], opnimg4[8], opnimg4[9]))
                concat5 = np.concatenate((opnimg5[0], opnimg5[1], opnimg5[2], opnimg5[3], opnimg5[4], opnimg5[5], opnimg5[6], opnimg5[7], opnimg5[8], opnimg5[9]))
                concat6 = np.concatenate((opnimg6[0], opnimg6[1], opnimg6[2], opnimg6[3], opnimg6[4], opnimg6[5], opnimg6[6], opnimg6[7], opnimg6[8], opnimg6[9]))
                concat7 = np.concatenate((opnimg7[0], opnimg7[1], opnimg7[2], opnimg7[3], opnimg7[4], opnimg7[5], opnimg7[6], opnimg7[7], opnimg7[8], opnimg7[9]))
                concat8 = np.concatenate((opnimg8[0], opnimg8[1], opnimg8[2], opnimg8[3], opnimg8[4], opnimg8[5], opnimg8[6], opnimg8[7], opnimg8[8], opnimg8[9]))
                concat9 = np.concatenate((opnimg9[0], opnimg9[1], opnimg9[2], opnimg9[3], opnimg9[4], opnimg9[5], opnimg9[6], opnimg9[7], opnimg9[8], opnimg9[9]))
                concat10 = np.concatenate((opnimg10[0], opnimg10[1], opnimg10[2], opnimg10[3], opnimg10[4], opnimg10[5], opnimg10[6], opnimg10[7], opnimg10[8], opnimg10[9]))
                
                vertical_image = np.concatenate((concat1, concat2, concat3, concat4, concat5, concat6, concat7, concat8, concat9, concat10), axis = 1)
                
                print("==========================================")
                print(current_pth)
        
                real_vertical_image = cv2.resize(vertical_image, (1870, 1000))
    
                cv2.imshow('img', real_vertical_image)
                cv2.waitKey(0)
                opnimg1 = list(); opnimg2 = list(); opnimg3 = list(); opnimg4 = list(); opnimg5 = list()
                opnimg6 = list(); opnimg7 = list(); opnimg8 = list(); opnimg9 = list(); opnimg10 = list()


                count = 0
                totfoldlength -= 1

#----------------------------------------------------------------------------

def execute_cmdline(argv):
    prog = argv[0]
    parser = argparse.ArgumentParser(
        prog        = prog,
        description = 'Tool for K-Face dataset inspection.',
        epilog      = 'Type "%s <command> -h" for more information.' % prog)
        
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    def add_command(cmd, desc, example=None):
        epilog = 'Example: %s %s' % (prog, example) if example is not None else None
        return subparsers.add_parser(cmd, description=desc, help=desc, epilog=epilog)
    
    p = add_command(    'data_inspection', 'Check 100 subjects of K-Face images at once.',
                                            'data_inspection /K-Face/root/dir/pth')
    p.add_argument(     '--root_dir',       help='K-Face directory path', type=str)
    p.add_argument(     '--resolution',     help='Select resolution type. Input one of three types: High, Middle, Low (default: High)', type=str, default='High')
    p.add_argument(     '--session',        help='Select one session type [S001~S006] (default: S001)', type=str, default='S001')
    p.add_argument(     '--light',          help='Select one light type [L1~L30] (default: L1)', type=str, default='L1')
    p.add_argument(     '--emotion',        help='Select one emotion type [E01, E02, E03] (default: E01)', type=str, default='E01')
    p.add_argument(     '--camera',         help='Select one camera(degree) type [C1~C20 or all] (default: C7)', type=str, default='C7')
    
    
    p = add_command(    'bbox', 'Check 100 subjects of K-Face images at once (bounding boxes).',
                                            'data_inspection /K-Face/root/dir/pth')
    p.add_argument(     '--root_dir',       help='K-Face directory path', type=str)
    p.add_argument(     '--resolution',     help='Select resolution type. Input one of three types: High, Middle, Low (default: High)', type=str, default='High')
    p.add_argument(     '--light',          help='Select one light type [L1,L3,L6,L7] (default: L1)', type=str, default='L1')
    p.add_argument(     '--camera',         help='Select one camera(degree) type [C1~C20 or all] (default: C7)', type=str, default='C7')
    
    
    p = add_command(    'feature_point', 'Check 100 subjects of K-Face images at once (feature points).',
                                            'data_inspection /K-Face/root/dir/pth')
    p.add_argument(     '--root_dir',       help='K-Face directory path', type=str)
    p.add_argument(     '--resolution',     help='Select resolution type. Input one of three types: High, Middle, Low (default: High)', type=str, default='High')
    p.add_argument(     '--light',          help='Select one light type [L1,L3,L6,L7] (default: L1)', type=str, default='L1')
    p.add_argument(     '--camera',         help='Select one camera(degree) type [C1~C20 or all] (default: C7)', type=str, default='C7')
    
    
    args = parser.parse_args(argv[1:] if len(argv) > 1 else ['-h'])
    func = globals()[args.command]
    del args.command
    func(**vars(args))

#----------------------------------------------------------------------------

if __name__ == "__main__":
    execute_cmdline(sys.argv)

#----------------------------------------------------------------------------
