import os
import sys
import platform
from math import ceil, log2, log
from typing import List
from random import choice

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
from algorithms.decoder import Decoder
from algorithms.encoder import Encoder
from ui_splash_screen import Ui_SplashScreen

## ==> MAIN WINDOW
from ui_main import Ui_MainWindow
from algorithms.knuth import (encode_knuth, decode_knuth)
from algorithms.ShiftedVTCode import (ShiftedVTCode)

## ==> GLOBALS
counter = 0

def generate_test(output_file, strand_num, strand_len):
    file = open(output_file, 'w')
    for i in range(0, strand_num):
        strand = ''.join(choice('01') for _ in range(strand_len))
        file.write(strand)
        file.write('\n')

def is_binary_or_newline(string):
    for letter in string:
        if letter != '0' and letter != '1' and letter != '\n':
            return False
    return True

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
        self.run_msg = QMessageBox()
        self.error_msg.setIcon(QMessageBox.Critical)
        self.error_msg.setWindowTitle('Error')
        self.ui.shifted_text_encode.clear()
        self.ui.shifted_text_decode.clear()
        self.ui.knuth_text_encode.clear()
        self.ui.knuth_text_decode.clear()
        self.ui.repeat_text_encode.clear()
        self.ui.repeat_text_decode.clear()
        # connect push buttons to an event
        self.ui.browse_gen_output_button.clicked.connect(self.openFileDialogGenOut)
        self.ui.generate_button.clicked.connect(self.run_generator)
        self.ui.browse_input_button.clicked.connect(self.openFileDialogIn)
        self.ui.browse_output_button.clicked.connect(self.openFileDialogOut)
        self.ui.run_button.clicked.connect(self.input_validation_CCC)
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

    def run_generator(self):
        output_file = self.ui.browse_gen_output_line_edit.text()
        output_dir = os.path.dirname(output_file)
        if not os.path.isdir(output_dir):
            self.error_msg = QMessageBox()
            self.error_msg.setIcon(QMessageBox.Critical)
            self.error_msg.setText("Output file path doesn't exist")
            self.error_msg.setWindowTitle("Output Error")
            self.error_msg.exec_()
            return
        strand_num = self.ui.strand_num_box.value()
        strand_len = self.ui.strand_len_box.value()

        self.run_msg.setStandardButtons(QMessageBox.NoButton)
        self.run_msg.setText("Running...Please wait")
        self.run_msg.setStyleSheet("QLabel{min-width: 150px;}")
        self.run_msg.setWindowTitle("Execution")
        self.run_msg.show()
        QApplication.processEvents()
        generate_test(output_file, strand_num, strand_len)
        self.run_msg.setStandardButtons(QMessageBox.Ok)
        self.run_msg.setText("Done!")
        self.run_msg.show()

    def input_validation_CCC(self):
        raw = self.ui.rho_box.value()
        tao = self.ui.tao_box.value()
        strands_data_len = self.ui.strands_box.value()
        b_force = self.ui.b_force_box.currentText()
        input_file = self.ui.browse_input_line_edit.text()
        output_file = self.ui.browse_output_line_edit.text()

        # file validation
        # input file
        if not os.path.isfile(input_file):
            self.error_msg = QMessageBox()
            self.error_msg.setIcon(QMessageBox.Critical)
            self.error_msg.setText("Input file not found")
            self.error_msg.setWindowTitle("Input Error")
            self.error_msg.exec_()
            return
        # output file
        output_dir = os.path.dirname(output_file)
        if not os.path.isdir(output_dir):
            self.error_msg = QMessageBox()
            self.error_msg.setIcon(QMessageBox.Critical)
            self.error_msg.setText("Output file path doesn't exist")
            self.error_msg.setWindowTitle("Output Error")
            self.error_msg.exec_()
            return

        # raw, tao, strands length > 0

        e = -1
        t = raw * 4 + 1
        len_error = False
        bin_error = False
        with open(input_file, 'r') as fp:
            for count, line in enumerate(fp):
                # print(line)
                # print("\n")
                # print(count)
                if not is_binary_or_newline(line):
                    bin_error = True
                    break
                if len(line) != strands_data_len + 1:
                    len_error = True
                    break

        fp.close()
        if len_error:
            self.error_msg = QMessageBox()
            self.error_msg.setIcon(QMessageBox.Critical)
            self.error_msg.setText("Strand length in input file differs from given length")
            self.error_msg.setWindowTitle("Invalid input file")
            self.error_msg.exec_()
            return

        if bin_error:
            self.error_msg = QMessageBox()
            self.error_msg.setIcon(QMessageBox.Critical)
            self.error_msg.setText("Input file is not binary")
            self.error_msg.setWindowTitle("Invalid input file")
            self.error_msg.exec_()
            return
        # print(f'count {count}')
        # #print(f'count {log2(count)}')
        # count = 1 if count==0 else count
        index_length = ceil(log2(count))
        delta_2_size = ceil(log2(strands_data_len)) * (t - 1)
        for i in range(2 * tao, tao - 1, -1):
            delta_1_size = ceil(log2(index_length)) * i
            if b_force == 'true':
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

        if e == -1:
            self.error_msg = QMessageBox()
            self.error_msg.setIcon(QMessageBox.Critical)
            self.error_msg.setText("Strand length doesn't hold the algorithm constraints")
            self.error_msg.setWindowTitle("Invalid parameters")
            self.error_msg.exec_()
            return

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

    def openFileDialogIn(self):
        self.inputDNAPath, _ = QFileDialog.getOpenFileName(self, "Select an input file", './', filter="*.txt")
        self.ui.browse_input_line_edit.setText(self.inputDNAPath)

    def openFileDialogOut(self):
        self.inputDNAPath, _ = QFileDialog.getSaveFileName(self, "Select an output file", './', filter="*.txt")
        self.ui.browse_output_line_edit.setText(self.inputDNAPath)

    def openFileDialogGenOut(self):
        self.inputDNAPath, _ = QFileDialog.getSaveFileName(self, "Select an output file", './', filter="*.txt")
        self.ui.browse_gen_output_line_edit.setText(self.inputDNAPath)

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
        raw = self.ui.rho_box.value()
        tao = self.ui.tao_box.value()
        strands_data_len = self.ui.strands_box.value()
        b_force = self.ui.b_force_box.currentText()

        if self.ui.encode_decode_box.currentText() == "Encode":
            encode_decode = "E"
        else:
            encode_decode = "D"

        input_path = self.ui.browse_input_line_edit.text()
        output_path = self.ui.browse_output_line_edit.text()
        process_path = "algorithms/clustering-correcting-codes-master/CCC.exe"
        if not os.path.isfile(process_path):
            self.error_msg = QMessageBox()
            self.error_msg.setIcon(QMessageBox.Critical)
            self.error_msg.setText("Executable doesn't exist!")
            self.error_msg.setInformativeText("Place CCC.exe in algoritehms/clustering-correcting-codes-master/")
            self.error_msg.setWindowTitle("Executable Error")
            self.error_msg.exec_()
            return
        arguments = [encode_decode, str(raw), str(tao), str(strands_data_len), b_force, input_path, output_path]

        self.process = QProcess()
        self.process.setWorkingDirectory('.')
        self.process.start(process_path, arguments)

        started = self.process.waitForStarted(-1)
        if not started:
            self.error_msg = QMessageBox()
            self.error_msg.setIcon(QMessageBox.Critical)
            self.error_msg.setText("Encoder/Decoder process couldn't be started")
            self.error_msg.setWindowTitle("Execution error")
            self.error_msg.exec_()
            return

        self.run_msg = QMessageBox()
        self.run_msg.setIcon(QMessageBox.NoIcon)
        self.run_msg.setStandardButtons(QMessageBox.NoButton)
        self.run_msg.setStyleSheet("QLabel{min-width: 150px;}")
        self.run_msg.setWindowTitle("Progress")
        self.run_msg.setText("Running...Please wait")
        self.run_msg.show()
        QApplication.processEvents()

        self.process.waitForFinished(-1)
        self.run_msg.setText("Done!")
        self.run_msg.setStandardButtons(QMessageBox.Ok)


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
