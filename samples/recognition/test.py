import os
import torch
from dataLoader import *
from preprocessing import *
from utils import *
from config import *
from models.LightCNN.light_cnn import *

def l2_norm(input,axis=1):
    norm = torch.norm(input,2,axis,True)
    output = torch.div(input, norm)
    return output

config = configuration()
if config.device == -1:
    device_info = "cpu"
else:
    device_info = "cuda:" + str(config.device)
device = torch.device(device_info)

model = LightCNN_29Layers_v2(1)
model = loadModel(model, config.pretrained_model, device)
model.to(device)
model.eval()

ref = []
query = []

with torch.no_grad():
    ref.append(image_norm(config.refImg))
    ref = np.array(ref, dtype='float32')
    refData = torch.from_numpy(ref).float()
    refData = refData.to(device)
    refFeatVec = model(refData, embedding=True).to(device)
    refFeatVec = refFeatVec.detach()
    refFeatVec = l2_norm(refFeatVec)

    query.append(image_norm(config.queryImg))
    query = np.array(query, dtype='float32')
    queryData = torch.from_numpy(query).float()
    queryData = queryData.to(device)
    queryFeatVec = model(queryData, embedding=True)
    queryFeatVec = queryFeatVec.detach()
    queryFeatVec = l2_norm(queryFeatVec)

    refFV = refFeatVec.detach().cpu().numpy()
    queryFV = queryFeatVec.detach().cpu().numpy()

    dist_mat = np.dot(refFV, queryFV.T)
    dist = np.diag(dist_mat)

    print("Matching Score : " , dist)