import os
import sys
import platform
from math import ceil, log2

from PyQt5.QtWidgets import QMessageBox
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent, QProcess)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

## ==> SPLASH SCREEN
from ui_splash_screen import Ui_SplashScreen

## ==> MAIN WINDOW
from ui_main import Ui_MainWindow
from algorithems.knuth import (encode_knuth, decode_knuth)
from algorithems.ShiftedVTCode import (ShiftedVTCode)

## ==> GLOBALS
counter = 0


# YOUR APPLICATION
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, parent=None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # MAIN WINDOW LABEL
        # set the title
        self.setWindowTitle('The Ultimate Coding Tool')
        self.error_msg = QMessageBox()
        self.error_msg.setIcon(QMessageBox.Critical)
        self.error_msg.setWindowTitle('Error')
        self.ui.shifted_text_encode.clear()
        self.ui.shifted_text_decode.clear()
        self.ui.knuth_text_encode.clear()
        self.ui.knuth_text_decode.clear()
        # connect push buttons to an event
        self.ui.browse_button.clicked.connect(self.openFileDialog)
        self.ui.encode_button.clicked.connect(self.input_validation_CCC)
        self.ui.balanced_knuth_encode_button.clicked.connect(self.input_validation_encode_BCK)
        self.ui.balanced_decode_button.clicked.connect(self.input_validation_decode_BCK)
        self.ui.shifted_encode_button.clicked.connect(self.input_validation_encode_SVTC)
        self.ui.shifted_decode_button.clicked.connect(self.input_validation_decode_SVTC)

    def input_validation_CCC(self):
        raw = self.ui.raw_box.value()
        tao = self.ui.tao_box.value()
        strands_data_len = self.ui.strands_box.value()
        # do i need to cast to str??
        assumption = self.ui.assumption_box.currentText()
        b_force = self.ui.b_force_box.currentText()
        b_force_real = 'true' if b_force == 'Yes' else 'false'
        test_path = self.ui.browse_line_edit.text()
        process_path = "algorithems/clustering-correcting-codes-master/main.exe"
        e = -1
        t = raw * 4 + 1
        with open(r"results_before_encoding.txt", 'r') as fp:
            for count, line in enumerate(fp):
                pass
        index_length = ceil(log2(count))
        delta_2_size = ceil(log2(strands_data_len)) * (t - 1)
        for i in range(2 * tao, tao - 1, -1):
            delta_1_size = ceil(log2(index_length)) * i
            if b_force_real == 'true':
                if strands_data_len < index_length + 1 + delta_1_size + delta_2_size + 3 * t + 2 * delta_1_size:
                    pass
                else:
                    e = i
                    break
            else:
                if strands_data_len < index_length + 1 + delta_1_size + delta_2_size + t * ceil(log2(count)):
                    pass
                else:
                    e = i
                    break
        self.inputDNAPath = self.ui.browse_line_edit.text()
        if not os.path.isfile(self.inputDNAPath):
            self.error_msg.setText("The input file you chosen doesn't exist")
            self.error_msg.exec_()
            self.ui.browse_line_edit.clear()
        elif e == -1:
            self.error_msg.setText("the given strands data length is not holding the encoding constraints")
            self.error_msg.exec_()
        else:
            self.runCCCencode()

    def input_validation_encode_BCK(self):
        vec_orig = self.ui.knuth_text_encode.toPlainText().strip()
        sigma_len = self.ui.sigma_len_box.value()
        if len(vec_orig) % sigma_len:
            self.error_msg.setText("word length is not modolo 0 of sigma length")
            self.error_msg.exec_()
        else:
            self.runBCKencode()

    def input_validation_decode_BCK(self):
        vec_decode = self.ui.knuth_text_decode.toPlainText().strip()
        sigma_len = self.ui.sigma_len_box_2.value()
        if len(vec_decode) % sigma_len:
            self.error_msg.setText("word length is not modolo 0 of sigma length")
            self.error_msg.exec_()
        else:
            self.runBCKdecode()

    def input_validation_SVTC(self):
        n = self.ui.n_spin_box.value()
        c = self.ui.c_spin_box.value()
        return c <= n

    def input_validation_encode_SVTC(self):
        if not self.input_validation_SVTC():
            self.error_msg.setText("c must be smaller than n+1")
            self.error_msg.exec_()
        else:
            self.runSVTCencode()

    def input_validation_decode_SVTC(self):
        if not self.input_validation_SVTC():
            self.error_msg.setText("c must be smaller than n+1")
            self.error_msg.exec_()
        else:
            self.runSVTCdecode()

    def openFileDialog(self):
        self.inputDNAPath, _ = QFileDialog.getOpenFileName(self, "Select an input file", './', filter="*.txt")
        self.ui.browse_line_edit.setText(self.inputDNAPath)

    def runBCKencode(self):
        vec_orig = self.ui.knuth_text_encode.toPlainText().strip()
        sigma_len = self.ui.sigma_len_box.value()
        decode_vec = encode_knuth(vec_orig, sigma_len)
        len_vec_orig = len(vec_orig)
        len_vec_decode = len(decode_vec)
        self.ui.knuth_text_encode_2.setPlainText(decode_vec)
        self.ui.len_encoded_word.setText('Length Encoded word: ' + str(len_vec_orig))
        self.ui.len_decoded_word.setText('Length Decoded word: ' + str(len_vec_decode))

    def runBCKdecode(self):
        vec_decode = self.ui.knuth_text_decode.toPlainText().strip()
        sigma_len = self.ui.sigma_len_box_2.value()
        len_vec_orig = self.ui.encode_word_box.value()
        encode_vec = decode_knuth(vec_decode, sigma_len, len_vec_orig)
        self.ui.knuth_text_decode_2.setPlainText(encode_vec)

    def runSVTCencode(self):
        n = self.ui.n_spin_box.value()
        c = self.ui.c_spin_box.value()
        d = self.ui.d_spin_box.value()
        p = self.ui.p_spin_box.value()
        word_encode = self.ui.shifted_text_encode.toPlainText().strip()
        lst_word_encode = list(word_encode)
        lst_word_encode = [int(i) for i in lst_word_encode]
        svtc_obj = ShiftedVTCode(n, c, d, p)
        lst_word_decode = svtc_obj.encode(lst_word_encode)
        lst_word_decode = [str(i) for i in lst_word_decode]
        self.ui.shifted_text_encode_2.setPlainText(''.join(lst_word_decode))

    def runSVTCdecode(self):
        n = self.ui.n_spin_box.value()
        c = self.ui.c_spin_box.value()
        d = self.ui.d_spin_box.value()
        p = self.ui.p_spin_box.value()
        word_decode = self.ui.shifted_text_decode.toPlainText().strip()
        lst_word_decode = list(word_decode)
        lst_word_decode = [int(i) for i in lst_word_decode]
        svtc_obj = ShiftedVTCode(n, c, d, p)
        lst_word_encode = None
        if self.ui.checkBox.isChecked():
            # should i do u-1 beca 0 means place 1????
            # msg to user index starts from 0
            u = self.ui.u_spin_box.value()
            lst_word_encode = svtc_obj.decode(lst_word_decode, u)
        else:
            lst_word_encode = svtc_obj.decode(lst_word_decode)
        lst_word_encode = [str(i) for i in lst_word_encode]
        self.ui.shifted_text_decode_2.setPlainText(''.join(lst_word_encode))

    def runCCCencode(self):
        raw = self.ui.raw_box.value()
        tao = self.ui.tao_box.value()
        strands_data_len = self.ui.strands_box.value()
        # do i need to cast to str??
        assumption = self.ui.assumption_box.currentText()
        b_force = self.ui.b_force_box.currentText()
        b_force_real = 'true' if b_force == 'Yes' else 'false'
        test_path = self.ui.browse_line_edit.text()
        process_path = "algorithems/clustering-correcting-codes-master/main.exe"
        arguments = [str(raw), str(tao), str(strands_data_len), assumption, b_force_real, test_path]
        # print(process_path)
        # print(arguments)
        # self.progressBar.setVisible(True)
        # self.label_progress.setText('Running reconstruction, please wait!')
        self.process = QProcess()
        self.process.setWorkingDirectory('.')
        self.process.start(process_path, arguments)
        # self.process.readyRead.connect(self.dataReady)
        # self.process.finished.connect(self.reconstruction_finished)


# def reconstruction_finished(self):
#    self.label_progress.setText('We are done :)')
#   self.progressBar.setVisible(False)
#  text = open('output/output.txt').read()
# self.reconstruction_output_textEdit.setText(text)
# self.show_hist_graph_result()
# SPLASH SCREEN
class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, parent=None)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        ## UI ==> INTERFACE CODES
        ########################################################################

        ## REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        ## DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        # CHANGE DESCRIPTION

        # Initial Text
        self.ui.label_description.setText("<strong>Starting</strong>")

        # Change Texts
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QtCore.QTimer.singleShot(3000,
                                 lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))

        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ## ==> APP FUNCTIONS
    ########################################################################
    def progress(self):
        global counter

        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.main = MainWindow()
            self.main.show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        counter += 1


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
