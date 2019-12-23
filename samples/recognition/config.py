from easydict import EasyDict as dict

def configuration():
    config = dict()
    #config.imagePath = "/Users/keepsnam/NIA/Test/"                                   # directory path of image data
    #config.modelSavePath = "/Users/keepsnam/NIA/NIA_FaceRecogSample/work/"    # directory path for model save / log
    config.imagePath = "f:/cropped_data/"   # directory path of image data
    config.modelSavePath = "./work/"        # directory path for model save / log
    config.batch_size = 20                  # mini batch size
    config.epochs = 30                      # total epochs number for training
    config.save_epochs = 1                  # epochs number for model save
    config.validate_epochs = 1              # epochs number for validation
    config.validate_ratio = 0.1             # ratio to divide the dataset as training / validation
    config.display_it = 10                  # iteration number for displaying of training procedure

    config.lr = 0.001                       # learning rate
    config.momentum = 0.9
    config.weight_decay = 0.0005
    config.schedule_lr = [10, 20, 30]       # epochs for applying of learning rate modification

    config.inputSize = 128
    #config.device = -1                     # if CPU : -1, GPU : device number
    config.device = 0                       # if CPU : -1, GPU : device number

    config.embedding_size = 256             # feature vector dimension

    # parameters for "test.py"
    config.pretrained_model = "/Users/keepsnam/NIA/NIA_FaceRecogSample/work/1.pth.tar"      # trained model full path
    config.refImg = "/Users/keepsnam/NIA/C7.jpg"                                            # reference image full path
    config.queryImg = "/Users/keepsnam/NIA/C8.jpg"                                          # query image full path
    return config
