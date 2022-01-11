import os
import sys
import platform
from math import ceil, log2, log
from typing import List

from PyQt5.QtWidgets import QMessageBox
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject,
                            QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent, QProcess)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon,
                           QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

## ==> SPLASH SCREEN
from algorithems.decoder import Decoder
from algorithems.encoder import Encoder
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
        self.ui.repeat_text_encode.clear()
        self.ui.repeat_text_decode.clear()
        # connect push buttons to an event
        self.ui.browse_button.clicked.connect(self.openFileDialog)
        self.ui.encode_button.clicked.connect(self.input_validation_CCC)
        self.ui.balanced_knuth_encode_button.clicked.connect(self.input_validation_encode_BCK)
        self.ui.balanced_decode_button.clicked.connect(self.input_validation_decode_BCK)
        self.ui.shifted_encode_button.clicked.connect(self.input_validation_encode_SVTC)
        self.ui.shifted_decode_button.clicked.connect(self.input_validation_decode_SVTC)
        self.ui.repeat_encode_button.clicked.connect(self.input_validation_encode_RFC)
        self.ui.repeat_decode_button.clicked.connect(self.input_validation_decode_RFC)

        self.text_to_extract_file = ""
        self.name_of_file_to_extract = ""
        self.ui.bck_to_file_button.clicked.connect(
            self.extract_to_file)
        self.ui.bck_to_file_button_2.clicked.connect(
            self.extract_to_file)
        self.ui.SVTC_to_file_button.clicked.connect(
            self.extract_to_file)
        self.ui.SVTC_to_file_button_2.clicked.connect(
            self.extract_to_file)
        self.ui.repeat_to_file_button.clicked.connect(
            self.extract_to_file)
        self.ui.repeat_to_file_button_2.clicked.connect(
            self.extract_to_file)

    def input_validation_CCC(self):
        raw = self.ui.raw_box.value()
        tao = self.ui.tao_box.value()
        strands_data_len = self.ui.strands_box.value()
        # do i need to cast to str??
        assumption = self.ui.assumption_box.currentText()
        b_force = self.ui.b_force_box.currentText()
        b_force_real = 'true' if b_force == 'Yes' else 'false'
        test_path = self.ui.browse_line_edit.text()
        if test_path == "":
            self.error_msg.setText(
                "please insert input for the algorithm")
            self.error_msg.exec_()
            return
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
                if strands_data_len < index_length + 1 + delta_1_size + delta_2_size + t * ceil(
                        log2(count)):
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
            self.error_msg.setText(
                "the given strands data length is not holding the encoding constraints")
            self.error_msg.exec_()
        else:
            self.runCCCencode()

    def input_validation_encode_BCK(self):
        vec_orig = self.ui.knuth_text_encode.toPlainText().strip()
        if vec_orig == "":
            self.error_msg.setText(
                "please insert input for the algorithm")
            self.error_msg.exec_()
            return
        sigma_len = self.ui.sigma_len_box.value()
        if len(vec_orig) % sigma_len:
            self.error_msg.setText("word length is not modulo 0 of sigma length")
            self.error_msg.exec_()
        else:
            self.runBCKencode()

    def input_validation_decode_BCK(self):
        vec_decode = self.ui.knuth_text_decode.toPlainText().strip()
        if vec_decode == "":
            self.error_msg.setText(
                "please insert input for the algorithm")
            self.error_msg.exec_()
            return
        sigma_len = self.ui.sigma_len_box_2.value()
        if len(vec_decode) % sigma_len:
            self.error_msg.setText("word length is not modulo 0 of sigma length")
            self.error_msg.exec_()
            return
        else:
            self.runBCKdecode()

    def input_validation_SVTC(self):
        n = self.ui.n_spin_box.value()
        c = self.ui.c_spin_box.value()
        return c <= n

    def input_validation_encode_SVTC(self):
        word_encode = self.ui.shifted_text_encode.toPlainText().strip()
        if word_encode == "":
            self.error_msg.setText(
                "please insert input for the algorithm")
            self.error_msg.exec_()
            return
        redundancy = ceil(log2(self.ui.p_spin_box.value())) + 1
        lst_word_encode = list(word_encode)
        lst_word_encode = [int(i) for i in lst_word_encode]
        if len(lst_word_encode) != self.ui.n_spin_box.value() - redundancy:
            self.error_msg.setText("Invalid vector length! cannot map to a legal codeword")
            self.error_msg.exec_()
        elif not self.input_validation_SVTC():
            self.error_msg.setText("c must be smaller than n+1")
            self.error_msg.exec_()
        else:
            self.runSVTCencode()

    def input_validation_decode_SVTC(self):
        word_decode = self.ui.shifted_text_decode.toPlainText().strip()
        if word_decode == "":
            self.error_msg.setText(
                "please insert input for the algorithm")
            self.error_msg.exec_()
            return
        if not self.input_validation_SVTC():
            self.error_msg.setText("c must be smaller than n+1")
            self.error_msg.exec_()
            return
        else:
            self.runSVTCdecode()

    def input_validation_encode_RFC(self):
        vec_orig = self.ui.repeat_text_encode.toPlainText().strip()
        if vec_orig == "":
            self.error_msg.setText(
                "please insert input for the algorithm")
            self.error_msg.exec_()
            return
        else:
            self.runRFCencode()

    def input_validation_decode_RFC(self):
        vec_decode = self.ui.repeat_text_decode.toPlainText().strip()
        if vec_decode == "":
            self.error_msg.setText(
                "please insert input for the algorithm")
            self.error_msg.exec_()
            return
        else:
            self.runRFCdecode()

    def openFileDialog(self):
        self.inputDNAPath, _ = QFileDialog.getOpenFileName(self, "Select an input file", './',
                                                           filter="*.txt")
        self.ui.browse_line_edit.setText(self.inputDNAPath)

    def runBCKencode(self):
        vec_orig = self.ui.knuth_text_encode.toPlainText().strip()
        sigma_len = self.ui.sigma_len_box.value()
        decode_vec = encode_knuth(vec_orig, sigma_len)
        len_vec_orig = len(vec_orig)
        len_vec_decode = len(decode_vec)
        self.text_to_extract_file = str(decode_vec)
        self.name_of_file_to_extract = "bck_encode_output"
        self.ui.knuth_text_encode_2.setPlainText(decode_vec)
        self.ui.len_encoded_word.setText('Length Encoded word: ' + str(len_vec_orig))
        self.ui.len_decoded_word.setText('Length Decoded word: ' + str(len_vec_decode))

    def runBCKdecode(self):
        vec_decode = self.ui.knuth_text_decode.toPlainText().strip()
        sigma_len = self.ui.sigma_len_box_2.value()
        len_vec_orig = self.ui.encode_word_box.value()
        encode_vec = decode_knuth(vec_decode, sigma_len, len_vec_orig)
        self.text_to_extract_file = str(encode_vec)
        self.name_of_file_to_extract = "bck_decode_output"
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
        self.text_to_extract_file = str(''.join(lst_word_decode))
        self.name_of_file_to_extract = "svtc_encode_output"
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
        self.text_to_extract_file = str(''.join(lst_word_encode))
        self.name_of_file_to_extract = "svtc_decode_output"
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
        self.process = QProcess()
        self.process.setWorkingDirectory('.')
        self.process.start(process_path, arguments)


    def run_action(self, w: List, q, action, redundancy, complexity_mode, verbose_mode,
                   test_mode, comma_mode):
        n = len(w) + redundancy if action == "encode" else len(w)
        orig_w = w.copy()
        log_n = ceil(log(n, q))
        k = 2 * log_n + 2
        file_to_print = self.ui.repeat_text_encode_2 if action == "encode" \
            else self.ui.repeat_text_decode_2
        res_word, text_to_print = Encoder(complexity_mode, redundancy, verbose_mode, q).input(
            w).encode().output() if \
            action == "encode" else Decoder(redundancy, verbose_mode, q).input(w).decode().output()
        if verbose_mode:
            file_to_print.setPlainText(f'n      ={n}\n'
                                       f'q      ={q}\n'
                                       f'log_n  ={log_n}\n'
                                       f'k      ={k}\n'
                                       f'w      ={w}\n'
                                       f'{text_to_print}'
                                       f'output ={"".join(map(str, res_word))}')
            self.text_to_extract_file = f'n      ={n}\n'\
                                        f'q      ={q}\n'\
                                        f'log_n  ={log_n}\n'\
                                        f'k      ={k}\n'\
                                        f'w      ={w}\n'\
                                        f'{text_to_print}'\
                                        f'output ={"".join(map(str, res_word))}'

        else:
            file_to_print.setPlainText(f'output ={"".join(map(str, res_word))}')
            self.text_to_extract_file = f'output ={"".join(map(str, res_word))}'

    def runRFCencode(self):
        action = 'encode'
        r = self.ui.nrb_assumptionbox.currentText()
        q = self.ui.ab_spinbox.value()
        t = self.ui.imp_assumptionbox.currentText()
        v = self.ui.log_assumptionbox.currentText()
        v = False if v == 'no' else True
        vec_orig = self.ui.repeat_text_encode.toPlainText().strip()
        sequence = [int(x) for x in list(vec_orig)]
        self.run_action(sequence, int(q), action, int(r), t, v, test_mode=False, comma_mode=(q > 2))
        self.name_of_file_to_extract = "rfc_encode_output"

    def runRFCdecode(self):
        action = 'decode'
        r = self.ui.nrb_assumptionbox.currentText()
        q = self.ui.ab_spinbox.value()
        t = self.ui.imp_assumptionbox.currentText()
        v = self.ui.log_assumptionbox.currentText()
        v = False if v == 'no' else True
        vec_decode = self.ui.repeat_text_decode.toPlainText().strip()
        sequence = [int(x) for x in list(vec_decode)]
        self.run_action(sequence, int(q), action, int(r), t, v, test_mode=False, comma_mode=(q > 2))
        self.name_of_file_to_extract = "rfc_decode_output"


    def extract_to_file(self):
        if self.text_to_extract_file == "" or self.name_of_file_to_extract == "":
            self.error_msg.setText(
                "there is no output to extract")
            self.error_msg.exec_()
            return
        with open(f'{self.name_of_file_to_extract}.txt', 'w') as f:
            f.write(self.text_to_extract_file)
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
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText(
            "<strong>LOADING</strong> DATABASE"))
        QtCore.QTimer.singleShot(3000,
                                 lambda: self.ui.label_description.setText(
                                     "<strong>LOADING</strong> USER INTERFACE"))

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
