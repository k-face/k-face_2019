import sys, os, re
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5 import Qt, QtCore, QtGui, QtWidgets


# Basic image viewer class to show an image w/ zoom & pan
# Pre-requisite: QLabel, QMainWindow class
class ImageViewer:
    def __init__(self, qlabel, qmain):
        self.qmain_window = qmain
        self.qlabel_image = qlabel      # widget/window name where image is displayed (I'm usiing qlabel)
        self.qimage_scaled = QImage()   # scaled image to fit to the size of qlabel_image
        self.qpixmap = QPixmap()        # qpixmap to fill the qlabel_image

        self.zoomX = 1                  # zoom factor w.r.t size of qlabel_image
        self.position = [0, 0]          # position of top left corner of qimage_label w.r.t. qimage_scaled
        self.panFlag = False            # to enable or disable pan
        self.pressed = None

        self.selectFlag = False         # TODO selection
        self.selectPointId = -1         # TODO
        self.selectRectId = -1          # TODO

        self.qlabel_image.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.__connectEvents()

    def __connectEvents(self):
        # Mouse events
        self.qlabel_image.mousePressEvent = self.mousePressAction
        self.qlabel_image.mouseMoveEvent = self.mouseMoveAction
        self.qlabel_image.mouseReleaseEvent = self.mouseReleaseAction

    def onResize(self):
        self.qpixmap = QPixmap(self.qlabel_image.size())
        self.qpixmap.fill(QtCore.Qt.gray)
        self.qimage_scaled = self.qimage.scaled(self.qlabel_image.width() * self.zoomX, self.qlabel_image.height() * self.zoomX, QtCore.Qt.KeepAspectRatio)
        self.update()

    def loadImage(self, imagePath):
        self.qimage = QImage(imagePath)
        self.qpixmap = QPixmap(self.qlabel_image.size())
        if not self.qimage.isNull():
            # reset Zoom factor and Pan position
            self.zoomX = 1
            self.position = [0, 0]
            self.qimage_scaled = self.qimage.scaled(self.qlabel_image.width(), self.qlabel_image.height(), QtCore.Qt.KeepAspectRatio)
            self.update()
        else:
            self.statusbar.showMessage('Cannot open this image! Try another one.', 5000)

    def update(self):
        if not self.qimage_scaled.isNull():
            # check if position is within limits to prevent unbounded panning.
            px, py = self.position
            px = px if (px <= self.qimage_scaled.width() - self.qlabel_image.width()) else (self.qimage_scaled.width() - self.qlabel_image.width())
            py = py if (py <= self.qimage_scaled.height() - self.qlabel_image.height()) else (self.qimage_scaled.height() - self.qlabel_image.height())
            px = px if (px >= 0) else 0
            py = py if (py >= 0) else 0
            self.position = (px, py)

            if self.zoomX == 1:
                self.qpixmap.fill(QtCore.Qt.white)

            # the act of painting the qpixmap
            painter = QPainter()
            painter.begin(self.qpixmap)
            painter.drawImage(QtCore.QPoint(0, 0), self.qimage_scaled,
                    QtCore.QRect(self.position[0], self.position[1], self.qlabel_image.width(), self.qlabel_image.height()) )
            painter.end()
            self.qlabel_image.setPixmap(self.qpixmap)

            # draw annotations
            self.drawAnnotationRect(self.qmain_window.annot_manager.bboxes)
            self.drawAnnotationPoint(self.qmain_window.annot_manager.points)

        else:
            pass

    def drawAnnotationPoint(self, points):
        ratio = float(self.qimage_scaled.width()) / float(self.qimage.width());
        painter = QPainter()
        painter.begin(self.qpixmap)
        r = 10              # point radius
        if len(points["nose"]) > 0:
            p = [int(i*ratio) for i in points["nose"]]; painter.setBrush(QtCore.Qt.green); painter.drawEllipse(p[0], p[1], r, r)
        if len(points["eyeR"]) > 0:
            p = [int(i*ratio) for i in points["eyeR"]]; painter.setBrush(QtCore.Qt.yellow); painter.drawEllipse(p[0], p[1], r, r)
        if len(points["eyeL"]) > 0:
            p = [int(i*ratio) for i in points["eyeL"]]; painter.setBrush(QtCore.Qt.darkYellow); painter.drawEllipse(p[0], p[1], r, r)
        if len(points["mouthR"]) > 0:
            p = [int(i*ratio) for i in points["mouthR"]]; painter.setBrush(QtCore.Qt.cyan); painter.drawEllipse(p[0], p[1], r, r)
        if len(points["mouthL"]) > 0:
            p = [int(i*ratio) for i in points["mouthL"]]; painter.setBrush(QtCore.Qt.darkCyan); painter.drawEllipse(p[0], p[1], r, r)
        if len(points["earR"]) > 0:
            p = [int(i*ratio) for i in points["earR"]]; painter.setBrush(QtCore.Qt.magenta); painter.drawEllipse(p[0], p[1], r, r)
        if len(points["earL"]) > 0:
            p = [int(i*ratio) for i in points["earL"]]; painter.setBrush(QtCore.Qt.darkMagenta); painter.drawEllipse(p[0], p[1], r, r)
        painter.end()
        self.qlabel_image.setPixmap(self.qpixmap)

    def drawAnnotationRect(self, bboxes):
        ratio = float(self.qimage_scaled.width()) / float(self.qimage.width());
        painter = QPainter()
        painter.begin(self.qpixmap)
        pen = QtGui.QPen()
        pen.setWidth(2)     # line width
        if bboxes["face"]:
            p = [int(i*ratio) for i in bboxes["face"]]; pen.setColor(QtCore.Qt.red); painter.setPen(pen); painter.drawRect(p[0], p[1], p[2], p[3])
        if bboxes["eyeR"]:
            p = [int(i*ratio) for i in bboxes["eyeR"]]; pen.setColor(QtCore.Qt.yellow); painter.setPen(pen); painter.drawRect(p[0], p[1], p[2], p[3])
        if bboxes["eyeL"]:
            p = [int(i*ratio) for i in bboxes["eyeL"]]; pen.setColor(QtCore.Qt.darkYellow); painter.setPen(pen); painter.drawRect(p[0], p[1], p[2], p[3])
        if bboxes["nose"]:
            p = [int(i*ratio) for i in bboxes["nose"]]; pen.setColor(QtCore.Qt.green); painter.setPen(pen); painter.drawRect(p[0], p[1], p[2], p[3])
        if bboxes["mouth"]:
            p = [int(i*ratio) for i in bboxes["mouth"]]; pen.setColor(QtCore.Qt.cyan); painter.setPen(pen); painter.drawRect(p[0], p[1], p[2], p[3])
        if bboxes["earR"]:
            p = [int(i*ratio) for i in bboxes["earR"]]; pen.setColor(QtCore.Qt.magenta); painter.setPen(pen); painter.drawRect(p[0], p[1], p[2], p[3])
        if bboxes["earL"]:
            p = [int(i*ratio) for i in bboxes["earL"]]; pen.setColor(QtCore.Qt.darkMagenta); painter.setPen(pen); painter.drawRect(p[0], p[1], p[2], p[3])
        painter.end()
        self.qlabel_image.setPixmap(self.qpixmap)

    def drawRect(self, x, y, w, h):
        tmp_pixmap = QtGui.QPixmap(self.qpixmap)
        painter = QtGui.QPainter(tmp_pixmap)    # create painter
        pen = QtGui.QPen(QtCore.Qt.green)       # set rectangle color and thickness
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(x, y, w, h)
        painter.end()
        self.qlabel_image.setPixmap(tmp_pixmap)

    def drawPoint(self, x, y):
        r = 10
        tmp_pixmap = QtGui.QPixmap(self.qpixmap)
        painter = QtGui.QPainter(tmp_pixmap)  # create painter
        painter.setBrush(QtCore.Qt.green);
        painter.drawEllipse(x, y, r, r)
        painter.end()
        self.qlabel_image.setPixmap(tmp_pixmap)

    def mousePressAction(self, QMouseEvent):
        if not hasattr(self, 'qimage'):
            return
        x, y = QMouseEvent.pos().x(), QMouseEvent.pos().y()
        if self.panFlag:
            self.pressed = QMouseEvent.pos()    # starting point of drag vector
            self.anchor = self.position         # save the pan position when panning starts

        if self.qmain_window.toggle_bbox.isChecked():
            # TODO: check if position is within limits to prevent unbounded panning
            self.pressed = QMouseEvent.pos()
            self.anchor = self.position

        if self.qmain_window.toggle_point.isChecked():
            # TODO: check if position is within limits to prevent unbounded panning
            self.pressed = QMouseEvent.pos()
            self.anchor = self.position
            self.drawPoint(x, y)


    def mouseMoveAction(self, QMouseEvent):
        if not hasattr(self, 'qimage'):
            return
        x, y = QMouseEvent.pos().x(), QMouseEvent.pos().y()
        if self.pressed:
            dx, dy = x - self.pressed.x(), y - self.pressed.y()         # calculate the drag vector
            self.position = self.anchor[0] - dx, self.anchor[1] - dy    # update pan position using drag vector
            self.update()                                               # show the image with updated pan position

            if self.qmain_window.toggle_bbox.isChecked():
                sx, sy = min(x, self.pressed.x()), min(y, self.pressed.y())
                ex, ey = max(x, self.pressed.x()), max(y, self.pressed.y())
                self.drawRect(sx,sy, ex-sx, ey-sy)

    def mouseReleaseAction(self, QMouseEvent):
        if not hasattr(self, 'qimage'):
            return
        x, y = QMouseEvent.pos().x(), QMouseEvent.pos().y()

        if self.qmain_window.toggle_point.isChecked():
            scale = float(self.qimage.width()) / float(self.qimage_scaled.width())
            P = [int(x*scale), int(y*scale)]
            if not self.qmain_window.annot_manager.points["nose"]:
                self.qmain_window.annot_manager.points["nose"] = P
            elif not self.qmain_window.annot_manager.points["eyeR"]:
                self.qmain_window.annot_manager.points["eyeR"] = P
            elif not self.qmain_window.annot_manager.points["eyeL"]:
                self.qmain_window.annot_manager.points["eyeL"] = P
            elif not self.qmain_window.annot_manager.points["mouthR"]:
                self.qmain_window.annot_manager.points["mouthR"] = P
            elif not self.qmain_window.annot_manager.points["mouthL"]:
                self.qmain_window.annot_manager.points["mouthL"] = P
            elif not self.qmain_window.annot_manager.points["earR"]:
                self.qmain_window.annot_manager.points["earR"] = P
            elif not self.qmain_window.annot_manager.points["earL"]:
                self.qmain_window.annot_manager.points["earL"] = P
            self.qmain_window.statusBar().showMessage("point is added: [" + str(P[0]) + " " + str(P[1]) + "]")

        elif self.qmain_window.toggle_bbox.isChecked():
            scale = float(self.qimage.width()) / float(self.qimage_scaled.width())
            sx = min(x, self.pressed.x())
            sy = min(y, self.pressed.y())
            ex = max(x, self.pressed.x())
            ey = max(y, self.pressed.y())
            P = [int(sx*scale), int(sy*scale), int((ex-sx)*scale), int((ey-sy)*scale)]
            if self.qmain_window.annot_manager.bboxesFlag["face"] and not self.qmain_window.annot_manager.bboxes["face"]:
                self.qmain_window.annot_manager.bboxes["face"] = P
            elif self.qmain_window.annot_manager.bboxesFlag["eyeR"] and not self.qmain_window.annot_manager.bboxes["eyeR"]:
                self.qmain_window.annot_manager.bboxes["eyeR"] = P
            elif self.qmain_window.annot_manager.bboxesFlag["eyeL"] and not self.qmain_window.annot_manager.bboxes["eyeL"]:
                self.qmain_window.annot_manager.bboxes["eyeL"] = P
            elif self.qmain_window.annot_manager.bboxesFlag["nose"] and not self.qmain_window.annot_manager.bboxes["nose"]:
                self.qmain_window.annot_manager.bboxes["nose"] = P
            elif self.qmain_window.annot_manager.bboxesFlag["mouth"] and not self.qmain_window.annot_manager.bboxes["mouth"]:
                self.qmain_window.annot_manager.bboxes["mouth"] = P
            elif self.qmain_window.annot_manager.bboxesFlag["earR"] and not self.qmain_window.annot_manager.bboxes["earR"]:
                self.qmain_window.annot_manager.bboxes["earR"] = P
            elif self.qmain_window.annot_manager.bboxesFlag["earL"] and not self.qmain_window.annot_manager.bboxes["earL"]:
                self.qmain_window.annot_manager.bboxes["earL"] = P
            self.qmain_window.statusBar().showMessage("bbox is added: [" + str(P[0]) + " " + str(P[1]) + " " + str(P[2]) + " " + str(P[3]) + "]")

        self.pressed = None  # clear the starting point of drag vector
        self.update()

    def zoomPlus(self):
        if not hasattr(self, 'qimage'):
            return
        self.zoomX += 1
        px, py = self.position
        px += self.qlabel_image.width()/2
        py += self.qlabel_image.height()/2
        self.position = (px, py)
        self.qimage_scaled = self.qimage.scaled(self.qlabel_image.width() * self.zoomX, self.qlabel_image.height() * self.zoomX, QtCore.Qt.KeepAspectRatio)
        self.update()

    def zoomMinus(self):
        if not hasattr(self, 'qimage'):
            return
        if self.zoomX > 1:
            self.zoomX -= 1
            px, py = self.position
            px -= self.qlabel_image.width()/2
            py -= self.qlabel_image.height()/2
            self.position = (px, py)
            self.qimage_scaled = self.qimage.scaled(self.qlabel_image.width() * self.zoomX, self.qlabel_image.height() * self.zoomX, QtCore.Qt.KeepAspectRatio)
            self.update()

    def resetZoom(self):
        if not hasattr(self, 'qimage'):
            return
        self.zoomX = 1
        self.position = [0, 0]
        self.qimage_scaled = self.qimage.scaled(self.qlabel_image.width() * self.zoomX, self.qlabel_image.height() * self.zoomX, QtCore.Qt.KeepAspectRatio)
        self.update()

    def enablePan(self, value):
        self.panFlag = value


###############################################################################
class AnnotationManager:
    def __init__(self):
        # the dict can be orderless in Python 3.x => we use these keys to access it
        self.pkeys = ["nose", "eyeR", "eyeL", "mouthR", "mouthL", "earR", "earL"]
        self.bkeys = ["face", "eyeR", "eyeL", "nose", "mouth", "earR", "earL"]
        self.points = {}
        self.bboxes = {}
        self.bboxesFlag = {}
        self.cam_index = 0
        self.reset()

    def reset(self):
        self.points = { key:[] for key in self.pkeys }
        self.bboxes = { key:[] for key in self.bkeys }
        self.bboxesFlag = {key:0 for key in self.bkeys}

    def numAnnotations(self, cam_index):
        np = 7  # number of points
        nb = 0  # number of bboxes
        if cam_index == 7 or cam_index == 16: nb = 7
        elif 1 <= cam_index <= 2 or 12 <= cam_index <= 13: nb = 5
        else: nb = 6
        return np, nb

    def findCameraIndex(self, filePath):
        if os.path.exists(filePath) is False:
            return 0
        file_ext = os.path.basename(filePath)
        file, ext = os.path.splitext(file_ext)  # head, tail
        cam_num = re.findall('\d+|\D+', file)   # re.split('(\d+)', file)=> ['C','1','']   # matching 1-or-more digit
        return int(cam_num[1]) if len(cam_num) == 2 else 0
        # return 1~20

    '''
                        14(LU45),  15(LU15), 16(CU), 17(RU15),   18(RU45)
    1(L90),2(L75),3(L60),4(L45),5(L30),6(L15),7(C),8(R15),9(R30),10(R45),11(R60),12(R75),13(R90)
                        19(LL45),                                20(RL45)
    '''
    def findAnnotationFlag(self, cam_index):
        for i in range(0, 7):
            self.bboxesFlag[self.bkeys[i]] = 1
        if cam_index == 7 or cam_index == 16:
            pass # all exist if cam_index == 7, 16
        elif cam_index == 1 or cam_index == 2:
            self.bboxesFlag["eyeR"] = 0
            self.bboxesFlag["earR"] = 0
        elif cam_index == 12 or cam_index == 13:
            self.bboxesFlag["eyeL"] = 0
            self.bboxesFlag["earL"] = 0
        elif (3 <= cam_index <= 6) or cam_index == 14 or cam_index == 15 or cam_index == 19:  # no earR
            self.bboxesFlag["earR"] = 0
        else: #(8 <= cam_index <= 11) or cam_index == 17 or cam_index == 18 or cam_index == 20: # no earL
            self.bboxesFlag["earL"] = 0

    def loadFile(self, imgFilePath, txtFilePath):
        #print('loadFile: ' + txtFilePath)
        # (1)
        self.reset()
        self.cam_index = self.findCameraIndex(imgFilePath)
        self.findAnnotationFlag(self.cam_index)

        if txtFilePath is 'None' or os.path.exists(txtFilePath) is False:    # None or not exist
            self.reset()
            return

        # (2)
        lines = []
        try:
            def split_(line):
                return re.split('[ \t,;]+', line)  # space or tab

            with open(txtFilePath, 'r') as f:
                lines = [l.rstrip('\n').rstrip('\r') for l in f]
            f.close()

            # <1> 7 points
            for i in range(0, 7):
                x, y = split_(lines[i])
                self.points[self.pkeys[i]] = [int(x), int(y)]

            # <2> 5~7 bounding boxes
            # Sorry, we should have changed the annotation file format... :_(
            blines = lines[7:]
            lcount = 0
            for i in range(0, 7):
                if self.bboxesFlag[self.bkeys[i]] == 1:
                    xywh = split_(blines[lcount])
                    self.bboxes[self.bkeys[i]] = list(map(int, xywh))
                    lcount += 1

            #print(self.points)
            #print(self.bboxes)
        except:
            return

    def saveFile(self, txtFilePath):

        return

