import sys, os, re
try:
    from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
except:
    print('No pyqt5: pip install pyqt5')
    quit()
from utils import ImageViewer
from utils import AnnotationManager

gui = uic.loadUiType("main.ui")[0]  # pyuic5 -o main_form.py main.ui

def nicekey(s):
    def tryint(s):
        try: return int(s)
        except: return s
    return [tryint(c) for c in re.split('(\d+)', s)] # matching ([0-9]+) 1-or-more digit

def getImages(folder):
    image_formats = ('.BMP', '.JPG', '.JPEG', '.PNG')
    image_list = []
    annot_list = []
    if os.path.isdir(folder):
        im_path_list = []
        for file in os.listdir(folder):
            if file.upper().endswith(image_formats):
                im_path = os.path.join(folder, file)
                im_path_list.append(im_path)

        im_path_list.sort(key=nicekey)

        for im_path in im_path_list:
            file = os.path.basename(im_path)
            image_obj = {'name': file, 'path': im_path}
            image_list.append(image_obj)

            annot_file = os.path.splitext(file)[0] + ".txt"
            annot_path = os.path.join(folder, annot_file)
            annot_obj = {'name': annot_file, 'path': annot_path } if os.path.exists(annot_path) else {'name':'None', 'path':'None'}
            annot_list.append(annot_obj)

    return image_list, annot_list

class Iwindow(QtWidgets.QMainWindow, gui):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.image_id = -1      # the info of which image is selected/displayed
        self.numImages = -1
        self.image_viewer = ImageViewer(self.qlabel_image, self)
        self.annot_manager = AnnotationManager()
        self.__connectEvents()
        self.showNormal()
        self.statusBar().showMessage('Select a folder to annotate images')

    def __connectEvents(self):
        self.open_folder.clicked.connect(self.selectDir)
        self.next_im.clicked.connect(self.nextImg)
        self.prev_im.clicked.connect(self.prevImg)
        #self.qlist_images.itemClicked.connect(self.item_click)
        self.qlist_images.itemSelectionChanged.connect(self.item_select)
        self.save_annot.clicked.connect(self.saveAnnotation)

        self.zoom_plus.clicked.connect(self.image_viewer.zoomPlus)
        self.zoom_minus.clicked.connect(self.image_viewer.zoomMinus)
        self.reset_zoom.clicked.connect(self.image_viewer.resetZoom)

        self.toggle_pan.toggled.connect(self.action_pan)
        self.toggle_point.toggled.connect(self.action_point)
        self.toggle_bbox.toggled.connect(self.action_bbox)

    def selectDir(self):
        self.folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if not self.folder:
            QtWidgets.QMessageBox.warning(self, 'No folder selected', 'Please select a valid folder')
            return
        
        self.image_list, self.annot_list = getImages(self.folder)
        self.numImages = len(self.image_list)
        if self.numImages < 1:
            QtWidgets.QMessageBox.warning(self, 'No images', 'There are no images')
            return

        # make qt items
        self.annot_items = [QtWidgets.QListWidgetItem(l['name']) for l in self.annot_list]
        # Warning: self.qlist_annots.clear()
        while (self.qlist_annots.count() > 0):
            self.qlist_annots.takeItem(0)
        for item in self.annot_items:
            self.qlist_annots.addItem(item)

        self.image_items = [QtWidgets.QListWidgetItem(l['name']) for l in self.image_list]
        # Error: self.qlist_images.clear()
        # Instead, use takeItem (https://stackoverflow.com/questions/9594768/how-can-i-empty-a-qlistwidget-without-having-it-delete-all-of-the-qlistitemwidge)
        while(self.qlist_images.count()>0):
            self.qlist_images.takeItem(0)
        for item in self.image_items:
            self.qlist_images.addItem(item)

        # display first image and enable Pan 
        self.image_id = 0
        self.annot_manager.loadFile(self.image_list[self.image_id]['path'], self.annot_list[self.image_id]['path'])
        self.annot_items[self.image_id].setSelected(True)
        self.image_viewer.enablePan(True)
        self.image_viewer.loadImage(self.image_list[self.image_id]['path'])
        self.image_items[self.image_id].setSelected(True)
        self.statusBar().showMessage(self.image_list[self.image_id]['path'])

        # enable the next image button on the gui if multiple images are loaded
        if self.numImages > 1:
            self.next_im.setEnabled(True)

    def resizeEvent(self, evt):
        if self.image_id >= 0:
            self.image_viewer.onResize()

    def nextImg(self):
        if self.image_id < self.numImages - 1:
            self.image_id += 1
            self.annot_manager.loadFile(self.image_list[self.image_id]['path'], self.annot_list[self.image_id]['path'])
            self.annot_items[self.image_id].setSelected(True)
            self.image_viewer.loadImage(self.image_list[self.image_id]['path'])
            self.image_items[self.image_id].setSelected(True)

        else:
            QtWidgets.QMessageBox.warning(self, 'Sorry', 'No more Images!')

    def prevImg(self):
        if self.image_id > 0:
            self.image_id -= 1
            self.annot_manager.loadFile(self.image_list[self.image_id]['path'], self.annot_list[self.image_id]['path'])
            self.annot_items[self.image_id].setSelected(True)
            self.image_viewer.loadImage(self.image_list[self.image_id]['path'])
            self.image_items[self.image_id].setSelected(True)
        else:
            QtWidgets.QMessageBox.warning(self, 'Sorry', 'No previous Image!')

    def saveAnnotation(self):
        QtWidgets.QMessageBox.information(self, 'Save', 'Annotation file is saved.')

    def item_click(self, item):
        self.image_id = self.image_items.index(item)
        self.annot_manager.loadFile(self.image_list[self.image_id]['path'], self.annot_list[self.image_id]['path'])
        self.image_viewer.loadImage(self.image_list[self.image_id]['path'])
        self.annot_items[self.image_id].setSelected(True)
        self.statusBar().showMessage(self.image_list[self.image_id]['path'])

    def item_select(self):
        item = self.qlist_images.currentItem()
        if item != None:
            self.item_click(item)

    def action_pan(self):
        if self.toggle_pan.isChecked():
            self.qlabel_image.setCursor(QtCore.Qt.OpenHandCursor)
            self.image_viewer.enablePan(True)

    def action_point(self):
        if self.toggle_point.isChecked():
            self.qlabel_image.setCursor(QtCore.Qt.CrossCursor)
            self.image_viewer.enablePan(False)
            self.statusBar().showMessage("Draw points [nose, eye_R, eye_L, mouth_R, mouth_L, ear_R, ear_L]")

    def action_bbox(self):
        if self.toggle_bbox.isChecked():
            self.qlabel_image.setCursor(QtCore.Qt.CrossCursor)
            self.image_viewer.enablePan(False)
            self.statusBar().showMessage("Draw bbox [face, eye_R, eye_L, nose, mouth, ear_R, ear_L]")

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(Qt.QStyleFactory.create("cleanlooks"))
    app.setPalette(QtWidgets.QApplication.style().standardPalette())
    parentWindow = Iwindow(None)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()