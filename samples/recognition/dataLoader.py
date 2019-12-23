import os
from preprocessing import *
import torchvision.transforms as transforms
transformation = transforms.Compose([transforms.Resize(112), transforms.ToTensor(), transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])])

def imageListLoaderKFace(root_path):
    root = root_path
    img_list = []
    label = []
    labelIdx = 0;

    NUMBER_OF_SESSION = 6
    NUMBER_OF_LIGHT = 30
    NUMBER_OF_EXPRESSION = 3

    listResolution = ['High_Resolution', 'Middle_Resolution', 'Low_Resolution']
    listSession = []
    listLight = []
    listExpression = []

    for idx in range(NUMBER_OF_SESSION):
        sessionName = str('S%.3d' % (idx+1))
        listSession.append(sessionName)

    for idx in range(NUMBER_OF_LIGHT):
        lightName = str('L%d' % (idx+1))
        listLight.append(lightName)

    for idx in range(NUMBER_OF_EXPRESSION):
        expressionName = str('E%.2d' % (idx + 1))
        listExpression.append(expressionName)

    listClass = os.listdir(root+listResolution[0])
    for classId in listClass:
        if not os.path.isdir(root+listResolution[0]+'/'+classId):
            continue
        for resolution in listResolution:
            for session in listSession:
                for light in listLight:
                    for expression in listExpression:
                        sub_path = root + resolution + '/' + classId + '/' + session + '/' + light + '/' + expression + '/'
                        if os.path.isdir(sub_path) is False:
                            continue

                        listImage = os.listdir(sub_path)

                        for imageName in listImage:
                            ftitle, ext = os.path.splitext(imageName)
                            if ext != '.jpg':
                                continue

                            img_list.append(sub_path+imageName)
                            label.append(labelIdx)


        labelIdx += 1

    return img_list, label, labelIdx

def dataLoaderWithLabel(image_list, label_list, nTrainImg, it, batch_size):
    data = []
    labels = []

    for idx in range(batch_size):
        cur_idx = it * batch_size + idx
        if cur_idx >= nTrainImg:
            break
        normImg = image_norm(image_list[cur_idx])

        if len(normImg) == 0:
            continue

        data.append(normImg)
        labels.append(label_list[cur_idx])
    return data, labels

