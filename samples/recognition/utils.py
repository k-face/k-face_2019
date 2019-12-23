import torch

def saveModel(self, config, epoch):
    save_path = config.modelSavePath + str(epoch) + '.pth.tar'
    torch.save(self.backbone.state_dict(), save_path)

def loadModel(model, path_pretrainedModel, device):
    pretrained_dict = torch.load(path_pretrainedModel, map_location=device)
    model_dict = model.state_dict()

    pretrained_dict = {k: v for k, v in pretrained_dict.items() if
                       (k in model_dict) and (model_dict[k].shape == pretrained_dict[k].shape)}
    model_dict.update(pretrained_dict)
    model.load_state_dict(model_dict)

    return model

