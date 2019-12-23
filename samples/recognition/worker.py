import os
import torch
from torch.autograd import Variable
import torch.nn.functional as F
import torch.optim as optim

from dataLoader import *
from utils import *

from sklearn import datasets, model_selection
from dataLoader import *
from models.LightCNN.light_cnn import *


class worker(object):
    def __init__(self, config, inference=False):
        print(config)

        img_list, label, self.class_num = imageListLoaderKFace(config.imagePath)
        self.train_img, self.test_img, self.train_label, self.test_label = model_selection.train_test_split(img_list, label, test_size=config.validate_ratio)

        modelPath = config.modelSavePath
        if not os.path.exists(modelPath):
            os.makedirs(modelPath)

        self.backbone = LightCNN_29Layers_v2(self.class_num)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.backbone.parameters(), lr=config.lr, momentum=config.momentum, weight_decay=5e-4)
        print(self.optimizer)

        if config.device == -1:
            device_info = "cpu"
        else:
            device_info = "cuda:"+str(config.device)

        self.device = torch.device(device_info)
        self.backbone.to(self.device)

        self.lr_step = config.schedule_lr
        self.batch_size = config.batch_size
        self.max_epochs = config.epochs
        self.display_it = config.display_it
        self.save_epoch = config.save_epochs
        self.validate_epoch = config.validate_epochs
        
    def eval(self):
        print("======== Validation ========")
        sum_matched = 0
        test_img_cnt = len(self.test_img)
        iteration = int(len(self.test_img) / self.batch_size)

        for it in range(iteration):
            data, labels = dataLoaderWithLabel(self.test_img, self.test_label, len(self.test_img), it, self.batch_size)

            if len(data) == 0:
                break
            data_test = np.array(data, dtype='float32')
            labels_test = np.array(labels, dtype='int64')
            testX = torch.from_numpy(data_test).float()
            testY = torch.from_numpy(labels_test).long()

            testX, testY = Variable(testX).to(self.device), Variable(testY).to(self.device)
            output = self.backbone(testX)
            result = torch.max(output,1)[1]
            sum_matched += sum(testY.cpu().numpy() == result.cpu().numpy())

        accuracy = float(sum_matched) / float(test_img_cnt)

        print('TEST ACCURACY : ', accuracy)
        return

    def train(self, config):
        # self.model.train()
        self.eval()

        it_train = int(len(self.train_img) / self.batch_size)
        for epoch in range(self.max_epochs):
            print("======== TRAIN EPOCH ", epoch+1, "========")
            total_loss = 0

            for schedule in config.schedule_lr:
                if epoch == schedule:
                    for params in self.optimizer.param_groups:
                        params['lr'] /= 10
                    break

            for it in range(it_train):
                data, labels = dataLoaderWithLabel(self.train_img, self.train_label, len(self.train_img), it, self.batch_size)

                if len(data) == 0:
                    break;
                data = np.array(data, dtype='float32')
                labels = np.array(labels, dtype='int64')
                trainX = torch.from_numpy(data).float()
                trainY = torch.from_numpy(labels).long()

                trainX, trainY = Variable(trainX).to(self.device), Variable(trainY).to(self.device)
                self.optimizer.zero_grad()

                output = self.backbone(trainX)

                loss = self.criterion(output, trainY)
                loss.backward()
                self. optimizer.step()

                total_loss += loss

                if (it + 1) % self.display_it == 0:
                    print(it + 1, '/', it_train, ' : ', loss)

            print(epoch + 1, total_loss)

            if (epoch+1) % self.validate_epoch == 0:
                self.eval()

            if (epoch+1) % self.save_epoch == 0:
                saveModel(self, config, epoch+1)
        return

