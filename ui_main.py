# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        MainWindow.setMaximumSize(QSize(800, 600))
        MainWindow.setIconSize(QSize(24, 24))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setIconSize(QSize(16, 16))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        font1 = QFont()
        font1.setPointSize(10)
        self.tab.setFont(font1)
        self.tab.setAutoFillBackground(True)
        self.raw = QLabel(self.tab)
        self.raw.setObjectName(u"raw")
        self.raw.setGeometry(QRect(30, 20, 64, 18))
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.raw.sizePolicy().hasHeightForWidth())
        self.raw.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setPointSize(11)
        self.raw.setFont(font2)
        self.raw.setToolTipDuration(-1)
        self.browse_button = QPushButton(self.tab)
        self.browse_button.setObjectName(u"browse_button")
        self.browse_button.setGeometry(QRect(450, 240, 81, 21))
        self.browse_button.setFont(font1)
        self.browse_button.setAutoFillBackground(True)
        self.browse_button.setStyleSheet(u"")
        self.raw_box = QSpinBox(self.tab)
        self.raw_box.setObjectName(u"raw_box")
        self.raw_box.setGeometry(QRect(200, 20, 91, 22))
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.raw_box.sizePolicy().hasHeightForWidth())
        self.raw_box.setSizePolicy(sizePolicy2)
        self.tao_box = QSpinBox(self.tab)
        self.tao_box.setObjectName(u"tao_box")
        self.tao_box.setGeometry(QRect(200, 60, 91, 22))
        sizePolicy2.setHeightForWidth(self.tao_box.sizePolicy().hasHeightForWidth())
        self.tao_box.setSizePolicy(sizePolicy2)
        self.tao = QLabel(self.tab)
        self.tao.setObjectName(u"tao")
        self.tao.setGeometry(QRect(30, 60, 64, 18))
        sizePolicy1.setHeightForWidth(self.tao.sizePolicy().hasHeightForWidth())
        self.tao.setSizePolicy(sizePolicy1)
        self.tao.setFont(font2)
        self.strands_data_length = QLabel(self.tab)
        self.strands_data_length.setObjectName(u"strands_data_length")
        self.strands_data_length.setGeometry(QRect(30, 100, 131, 18))
        sizePolicy1.setHeightForWidth(self.strands_data_length.sizePolicy().hasHeightForWidth())
        self.strands_data_length.setSizePolicy(sizePolicy1)
        self.strands_data_length.setFont(font2)
        self.b_force = QLabel(self.tab)
        self.b_force.setObjectName(u"b_force")
        self.b_force.setGeometry(QRect(30, 180, 101, 18))
        sizePolicy1.setHeightForWidth(self.b_force.sizePolicy().hasHeightForWidth())
        self.b_force.setSizePolicy(sizePolicy1)
        self.b_force.setFont(font2)
        self.assumption = QLabel(self.tab)
        self.assumption.setObjectName(u"assumption")
        self.assumption.setGeometry(QRect(30, 140, 81, 18))
        sizePolicy1.setHeightForWidth(self.assumption.sizePolicy().hasHeightForWidth())
        self.assumption.setSizePolicy(sizePolicy1)
        self.assumption.setFont(font2)
        self.strands_box = QSpinBox(self.tab)
        self.strands_box.setObjectName(u"strands_box")
        self.strands_box.setGeometry(QRect(200, 100, 91, 22))
        sizePolicy2.setHeightForWidth(self.strands_box.sizePolicy().hasHeightForWidth())
        self.strands_box.setSizePolicy(sizePolicy2)
        self.strands_box.setMaximum(1000)
        self.assumption_box = QComboBox(self.tab)
        self.assumption_box.addItem("")
        self.assumption_box.addItem("")
        self.assumption_box.setObjectName(u"assumption_box")
        self.assumption_box.setGeometry(QRect(200, 140, 111, 22))
        sizePolicy1.setHeightForWidth(self.assumption_box.sizePolicy().hasHeightForWidth())
        self.assumption_box.setSizePolicy(sizePolicy1)
        self.b_force_box = QComboBox(self.tab)
        self.b_force_box.addItem("")
        self.b_force_box.addItem("")
        self.b_force_box.setObjectName(u"b_force_box")
        self.b_force_box.setGeometry(QRect(200, 180, 111, 22))
        sizePolicy1.setHeightForWidth(self.b_force_box.sizePolicy().hasHeightForWidth())
        self.b_force_box.setSizePolicy(sizePolicy1)
        self.test_input_file = QLabel(self.tab)
        self.test_input_file.setObjectName(u"test_input_file")
        self.test_input_file.setGeometry(QRect(29, 239, 101, 18))
        sizePolicy1.setHeightForWidth(self.test_input_file.sizePolicy().hasHeightForWidth())
        self.test_input_file.setSizePolicy(sizePolicy1)
        self.test_input_file.setFont(font2)
        self.encode_button = QPushButton(self.tab)
        self.encode_button.setObjectName(u"encode_button")
        self.encode_button.setGeometry(QRect(30, 320, 81, 31))
        self.encode_button.setFont(font2)
        self.browse_line_edit = QLineEdit(self.tab)
        self.browse_line_edit.setObjectName(u"browse_line_edit")
        self.browse_line_edit.setGeometry(QRect(200, 239, 231, 21))
        self.infoccc = QLabel(self.tab)
        self.infoccc.setObjectName(u"infoccc")
        self.infoccc.setGeometry(QRect(750, 10, 21, 21))
        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(130, 240, 21, 21))
        self.moreinfoccc = QLabel(self.tab)
        self.moreinfoccc.setObjectName(u"moreinfoccc")
        self.moreinfoccc.setGeometry(QRect(0, 520, 271, 16))
        self.moreinfoccc.setOpenExternalLinks(True)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tab_2.setAutoFillBackground(True)
        self.label = QLabel(self.tab_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(140, 20, 81, 21))
        font3 = QFont()
        font3.setPointSize(16)
        self.label.setFont(font3)
        self.line = QFrame(self.tab_2)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(360, 10, 20, 511))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(530, 20, 81, 21))
        font4 = QFont()
        font4.setPointSize(16)
        font4.setItalic(False)
        font4.setUnderline(False)
        self.label_2.setFont(font4)
        self.sigma_len_label = QLabel(self.tab_2)
        self.sigma_len_label.setObjectName(u"sigma_len_label")
        self.sigma_len_label.setGeometry(QRect(20, 100, 101, 21))
        font5 = QFont()
        font5.setPointSize(12)
        self.sigma_len_label.setFont(font5)
        self.sigma_len_box = QSpinBox(self.tab_2)
        self.sigma_len_box.setObjectName(u"sigma_len_box")
        self.sigma_len_box.setGeometry(QRect(130, 100, 61, 22))
        self.sigma_len_box.setMinimum(1)
        self.balanced_knuth_encode_button = QPushButton(self.tab_2)
        self.balanced_knuth_encode_button.setObjectName(u"balanced_knuth_encode_button")
        self.balanced_knuth_encode_button.setGeometry(QRect(250, 280, 71, 21))
        self.output_label_knuth = QLabel(self.tab_2)
        self.output_label_knuth.setObjectName(u"output_label_knuth")
        self.output_label_knuth.setGeometry(QRect(20, 300, 71, 41))
        self.len_decoded_word = QLabel(self.tab_2)
        self.len_decoded_word.setObjectName(u"len_decoded_word")
        self.len_decoded_word.setGeometry(QRect(170, 490, 221, 31))
        self.len_encoded_word = QLabel(self.tab_2)
        self.len_encoded_word.setObjectName(u"len_encoded_word")
        self.len_encoded_word.setGeometry(QRect(170, 470, 221, 31))
        self.sigma_len_label_2 = QLabel(self.tab_2)
        self.sigma_len_label_2.setObjectName(u"sigma_len_label_2")
        self.sigma_len_label_2.setGeometry(QRect(410, 60, 101, 21))
        self.sigma_len_label_2.setFont(font5)
        self.sigma_len_box_2 = QSpinBox(self.tab_2)
        self.sigma_len_box_2.setObjectName(u"sigma_len_box_2")
        self.sigma_len_box_2.setGeometry(QRect(530, 60, 61, 22))
        self.sigma_len_box_2.setMinimum(1)
        self.len_encoded_word_for_dec = QLabel(self.tab_2)
        self.len_encoded_word_for_dec.setObjectName(u"len_encoded_word_for_dec")
        self.len_encoded_word_for_dec.setGeometry(QRect(410, 90, 161, 31))
        self.encode_word_box = QSpinBox(self.tab_2)
        self.encode_word_box.setObjectName(u"encode_word_box")
        self.encode_word_box.setGeometry(QRect(580, 90, 61, 22))
        self.balanced_decode_button = QPushButton(self.tab_2)
        self.balanced_decode_button.setObjectName(u"balanced_decode_button")
        self.balanced_decode_button.setGeometry(QRect(650, 280, 71, 21))
        self.output_label_knuth_2 = QLabel(self.tab_2)
        self.output_label_knuth_2.setObjectName(u"output_label_knuth_2")
        self.output_label_knuth_2.setGeometry(QRect(410, 300, 71, 41))
        self.knuth_text_encode = QPlainTextEdit(self.tab_2)
        self.knuth_text_encode.setObjectName(u"knuth_text_encode")
        self.knuth_text_encode.setGeometry(QRect(20, 130, 311, 131))
        self.knuth_text_encode.setFocusPolicy(Qt.StrongFocus)
        self.knuth_text_encode.setTabChangesFocus(True)
        self.knuth_text_encode.setOverwriteMode(False)
        self.knuth_text_encode_2 = QPlainTextEdit(self.tab_2)
        self.knuth_text_encode_2.setObjectName(u"knuth_text_encode_2")
        self.knuth_text_encode_2.setGeometry(QRect(20, 340, 311, 131))
        self.knuth_text_encode_2.setTabChangesFocus(True)
        self.knuth_text_decode = QPlainTextEdit(self.tab_2)
        self.knuth_text_decode.setObjectName(u"knuth_text_decode")
        self.knuth_text_decode.setGeometry(QRect(410, 130, 311, 131))
        self.knuth_text_decode.setFocusPolicy(Qt.StrongFocus)
        self.knuth_text_decode.setTabChangesFocus(True)
        self.knuth_text_decode_2 = QPlainTextEdit(self.tab_2)
        self.knuth_text_decode_2.setObjectName(u"knuth_text_decode_2")
        self.knuth_text_decode_2.setGeometry(QRect(410, 340, 311, 131))
        self.knuth_text_decode_2.setTabChangesFocus(True)
        self.infobck = QLabel(self.tab_2)
        self.infobck.setObjectName(u"infobck")
        self.infobck.setGeometry(QRect(750, 10, 21, 21))
        self.notebck = QLabel(self.tab_2)
        self.notebck.setObjectName(u"notebck")
        self.notebck.setGeometry(QRect(310, 100, 21, 21))
        self.notebck_2 = QLabel(self.tab_2)
        self.notebck_2.setObjectName(u"notebck_2")
        self.notebck_2.setGeometry(QRect(700, 100, 21, 21))
        self.moreinforbck = QLabel(self.tab_2)
        self.moreinforbck.setObjectName(u"moreinforbck")
        self.moreinforbck.setGeometry(QRect(0, 520, 271, 16))
        self.moreinforbck.setOpenExternalLinks(True)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tab_3.setAutoFillBackground(True)
        self.label_4 = QLabel(self.tab_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(80, 30, 16, 16))
        self.n_spin_box = QSpinBox(self.tab_3)
        self.n_spin_box.setObjectName(u"n_spin_box")
        self.n_spin_box.setGeometry(QRect(100, 30, 51, 22))
        self.n_spin_box.setMaximum(1000)
        self.c_spin_box = QSpinBox(self.tab_3)
        self.c_spin_box.setObjectName(u"c_spin_box")
        self.c_spin_box.setGeometry(QRect(280, 30, 51, 22))
        self.c_spin_box.setMaximum(1000)
        self.label_9 = QLabel(self.tab_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(260, 30, 16, 16))
        self.d_spin_box = QSpinBox(self.tab_3)
        self.d_spin_box.setObjectName(u"d_spin_box")
        self.d_spin_box.setGeometry(QRect(450, 30, 51, 22))
        self.d_spin_box.setMaximum(1)
        self.label_10 = QLabel(self.tab_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(430, 30, 16, 16))
        self.p_spin_box = QSpinBox(self.tab_3)
        self.p_spin_box.setObjectName(u"p_spin_box")
        self.p_spin_box.setGeometry(QRect(620, 30, 51, 22))
        self.label_11 = QLabel(self.tab_3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(600, 30, 16, 16))
        self.line_5 = QFrame(self.tab_3)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setGeometry(QRect(370, 80, 20, 451))
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)
        self.label_12 = QLabel(self.tab_3)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(150, 90, 71, 21))
        self.label_12.setFont(font3)
        self.shifted_encode_button = QPushButton(self.tab_3)
        self.shifted_encode_button.setObjectName(u"shifted_encode_button")
        self.shifted_encode_button.setGeometry(QRect(270, 300, 71, 21))
        self.output_label_knuth_5 = QLabel(self.tab_3)
        self.output_label_knuth_5.setObjectName(u"output_label_knuth_5")
        self.output_label_knuth_5.setGeometry(QRect(30, 330, 61, 41))
        self.output_label_knuth_5.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.label_13 = QLabel(self.tab_3)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(540, 90, 71, 21))
        self.label_13.setFont(font4)
        self.shifted_decode_button = QPushButton(self.tab_3)
        self.shifted_decode_button.setObjectName(u"shifted_decode_button")
        self.shifted_decode_button.setGeometry(QRect(660, 300, 71, 21))
        self.checkBox = QCheckBox(self.tab_3)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(420, 130, 81, 31))
        self.checkBox.setFont(font1)
        self.checkBox.setLayoutDirection(Qt.RightToLeft)
        self.checkBox.setAutoFillBackground(False)
        self.u_spin_box = QSpinBox(self.tab_3)
        self.u_spin_box.setObjectName(u"u_spin_box")
        self.u_spin_box.setGeometry(QRect(680, 130, 51, 22))
        self.label_23 = QLabel(self.tab_3)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setGeometry(QRect(660, 130, 16, 16))
        font6 = QFont()
        font6.setPointSize(7)
        self.label_23.setFont(font6)
        self.output_label_knuth_9 = QLabel(self.tab_3)
        self.output_label_knuth_9.setObjectName(u"output_label_knuth_9")
        self.output_label_knuth_9.setGeometry(QRect(420, 330, 61, 41))
        self.output_label_knuth_9.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.shifted_text_encode = QPlainTextEdit(self.tab_3)
        self.shifted_text_encode.setObjectName(u"shifted_text_encode")
        self.shifted_text_encode.setGeometry(QRect(30, 160, 311, 131))
        self.shifted_text_encode.setFocusPolicy(Qt.StrongFocus)
        self.shifted_text_encode.setTabChangesFocus(True)
        self.shifted_text_decode = QPlainTextEdit(self.tab_3)
        self.shifted_text_decode.setObjectName(u"shifted_text_decode")
        self.shifted_text_decode.setGeometry(QRect(420, 160, 311, 131))
        self.shifted_text_decode.setFocusPolicy(Qt.StrongFocus)
        self.shifted_text_decode.setTabChangesFocus(True)
        self.shifted_text_encode_2 = QPlainTextEdit(self.tab_3)
        self.shifted_text_encode_2.setObjectName(u"shifted_text_encode_2")
        self.shifted_text_encode_2.setGeometry(QRect(30, 380, 311, 131))
        self.shifted_text_encode_2.setTabChangesFocus(True)
        self.shifted_text_decode_2 = QPlainTextEdit(self.tab_3)
        self.shifted_text_decode_2.setObjectName(u"shifted_text_decode_2")
        self.shifted_text_decode_2.setGeometry(QRect(420, 380, 311, 131))
        self.shifted_text_decode_2.setTabChangesFocus(True)
        self.groupBox = QGroupBox(self.tab_3)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 751, 61))
        self.note_svtc1 = QLabel(self.groupBox)
        self.note_svtc1.setObjectName(u"note_svtc1")
        self.note_svtc1.setGeometry(QRect(670, 20, 21, 21))
        self.note_svtc1_2 = QLabel(self.groupBox)
        self.note_svtc1_2.setObjectName(u"note_svtc1_2")
        self.note_svtc1_2.setGeometry(QRect(330, 20, 21, 21))
        self.infosvtc = QLabel(self.tab_3)
        self.infosvtc.setObjectName(u"infosvtc")
        self.infosvtc.setGeometry(QRect(750, 10, 21, 21))
        self.moreinforbck_2 = QLabel(self.tab_3)
        self.moreinforbck_2.setObjectName(u"moreinforbck_2")
        self.moreinforbck_2.setGeometry(QRect(0, 520, 271, 16))
        self.moreinforbck_2.setOpenExternalLinks(True)
        self.tabWidget.addTab(self.tab_3, "")
        self.groupBox.raise_()
        self.label_4.raise_()
        self.n_spin_box.raise_()
        self.c_spin_box.raise_()
        self.label_9.raise_()
        self.d_spin_box.raise_()
        self.label_10.raise_()
        self.p_spin_box.raise_()
        self.label_11.raise_()
        self.line_5.raise_()
        self.label_12.raise_()
        self.shifted_encode_button.raise_()
        self.output_label_knuth_5.raise_()
        self.label_13.raise_()
        self.shifted_decode_button.raise_()
        self.checkBox.raise_()
        self.u_spin_box.raise_()
        self.label_23.raise_()
        self.output_label_knuth_9.raise_()
        self.shifted_text_encode.raise_()
        self.shifted_text_decode.raise_()
        self.shifted_text_encode_2.raise_()
        self.shifted_text_decode_2.raise_()
        self.infosvtc.raise_()
        self.moreinforbck_2.raise_()

        self.horizontalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.raw_box, self.tao_box)
        QWidget.setTabOrder(self.tao_box, self.strands_box)
        QWidget.setTabOrder(self.strands_box, self.assumption_box)
        QWidget.setTabOrder(self.assumption_box, self.b_force_box)
        QWidget.setTabOrder(self.b_force_box, self.browse_button)
        QWidget.setTabOrder(self.browse_button, self.encode_button)
        QWidget.setTabOrder(self.encode_button, self.sigma_len_box)
        QWidget.setTabOrder(self.sigma_len_box, self.knuth_text_encode)
        QWidget.setTabOrder(self.knuth_text_encode, self.balanced_knuth_encode_button)
        QWidget.setTabOrder(self.balanced_knuth_encode_button, self.sigma_len_box_2)
        QWidget.setTabOrder(self.sigma_len_box_2, self.encode_word_box)
        QWidget.setTabOrder(self.encode_word_box, self.knuth_text_decode)
        QWidget.setTabOrder(self.knuth_text_decode, self.balanced_decode_button)
        QWidget.setTabOrder(self.balanced_decode_button, self.n_spin_box)
        QWidget.setTabOrder(self.n_spin_box, self.c_spin_box)
        QWidget.setTabOrder(self.c_spin_box, self.shifted_encode_button)
        QWidget.setTabOrder(self.shifted_encode_button, self.shifted_decode_button)
        QWidget.setTabOrder(self.shifted_decode_button, self.checkBox)
        QWidget.setTabOrder(self.checkBox, self.u_spin_box)
        QWidget.setTabOrder(self.u_spin_box, self.browse_line_edit)
        QWidget.setTabOrder(self.browse_line_edit, self.p_spin_box)
        QWidget.setTabOrder(self.p_spin_box, self.knuth_text_encode_2)
        QWidget.setTabOrder(self.knuth_text_encode_2, self.d_spin_box)
        QWidget.setTabOrder(self.d_spin_box, self.knuth_text_decode_2)
        QWidget.setTabOrder(self.knuth_text_decode_2, self.shifted_text_encode)
        QWidget.setTabOrder(self.shifted_text_encode, self.shifted_text_decode)
        QWidget.setTabOrder(self.shifted_text_decode, self.shifted_text_encode_2)
        QWidget.setTabOrder(self.shifted_text_encode_2, self.shifted_text_decode_2)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.raw.setToolTip(QCoreApplication.translate("MainWindow", u"a system parameters which are used to make assumptions about output strands", None))
#endif // QT_CONFIG(tooltip)
        self.raw.setText(QCoreApplication.translate("MainWindow", u"Raw", None))
        self.browse_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
#if QT_CONFIG(tooltip)
        self.tao.setToolTip(QCoreApplication.translate("MainWindow", u"a system parameters which are used to make assumptions about output strands", None))
#endif // QT_CONFIG(tooltip)
        self.tao.setText(QCoreApplication.translate("MainWindow", u"Tao", None))
#if QT_CONFIG(tooltip)
        self.strands_data_length.setToolTip(QCoreApplication.translate("MainWindow", u"an integer denoting the data length of the strands", None))
#endif // QT_CONFIG(tooltip)
        self.strands_data_length.setText(QCoreApplication.translate("MainWindow", u"Strands data length", None))
#if QT_CONFIG(tooltip)
        self.b_force.setToolTip(QCoreApplication.translate("MainWindow", u"denoting whether we're using brute force manner in the encoding algorithm", None))
#endif // QT_CONFIG(tooltip)
        self.b_force.setText(QCoreApplication.translate("MainWindow", u"Is brute force", None))
#if QT_CONFIG(tooltip)
        self.assumption.setToolTip(QCoreApplication.translate("MainWindow", u"'M' for majority or 'D' for dominance", None))
#endif // QT_CONFIG(tooltip)
        self.assumption.setText(QCoreApplication.translate("MainWindow", u"Assumption", None))
        self.assumption_box.setItemText(0, QCoreApplication.translate("MainWindow", u"M", None))
        self.assumption_box.setItemText(1, QCoreApplication.translate("MainWindow", u"D", None))

        self.b_force_box.setItemText(0, QCoreApplication.translate("MainWindow", u"No", None))
        self.b_force_box.setItemText(1, QCoreApplication.translate("MainWindow", u"Yes", None))

#if QT_CONFIG(tooltip)
        self.test_input_file.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.test_input_file.setText(QCoreApplication.translate("MainWindow", u"Input File", None))
        self.encode_button.setText(QCoreApplication.translate("MainWindow", u"Encode", None))
#if QT_CONFIG(tooltip)
        self.infoccc.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Algorithm implemented by : Elon Grubman and Amit Weil</p><p>Algorithm invented by : Tal Shinkar,Eitan Yaakobi, Andreas Lenz, and Antonia Wachter-Zeh</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.infoccc.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/images/info2.png\"/></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("MainWindow", u"the name should be test_file_updated.txt", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/images/note4.png\"/></p></body></html>", None))
#if QT_CONFIG(whatsthis)
        self.moreinfoccc.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.moreinfoccc.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><a href=\"https://yaakobi.wixsite.com/dnacodingsoftware/post/clustering-correcting-codes\"><span style=\" font-size:9pt; text-decoration: underline; color:#0000ff;\">click for more information about the algorithem</span></a></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Clustering-correcting-codes", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Encode", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Decode", None))
        self.sigma_len_label.setText(QCoreApplication.translate("MainWindow", u"Sigma length:", None))
        self.balanced_knuth_encode_button.setText(QCoreApplication.translate("MainWindow", u"Encode", None))
        self.output_label_knuth.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Output:</span></p></body></html>", None))
        self.len_decoded_word.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Length Decoded word:</p></body></html>", None))
        self.len_encoded_word.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Length Encoded word:</p></body></html>", None))
        self.sigma_len_label_2.setText(QCoreApplication.translate("MainWindow", u"Sigma length:", None))
        self.len_encoded_word_for_dec.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt;\">Length Encoded word:</span></p></body></html>", None))
        self.balanced_decode_button.setText(QCoreApplication.translate("MainWindow", u"Decode", None))
        self.output_label_knuth_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Output:</span></p></body></html>", None))
        self.knuth_text_encode.setPlainText("")
        self.knuth_text_encode.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ender text", None))
        self.knuth_text_decode.setPlainText("")
        self.knuth_text_decode.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter text", None))
#if QT_CONFIG(tooltip)
        self.infobck.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Algorithm implemented by : Noa Marelly and Ohad Goudsmid </p><p>Algorithm invented by : Donald E. Knuth</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.infobck.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/images/info2.png\"/></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.notebck.setToolTip(QCoreApplication.translate("MainWindow", u"word length need to be mod 0 sigma length", None))
#endif // QT_CONFIG(tooltip)
        self.notebck.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/images/note4.png\"/></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.notebck_2.setToolTip(QCoreApplication.translate("MainWindow", u"word length need to be mod 0 sigma length", None))
#endif // QT_CONFIG(tooltip)
        self.notebck_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/images/note4.png\"/></p></body></html>", None))
        self.moreinforbck.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><a href=\"https://yaakobi.wixsite.com/dnacodingsoftware/post/efficient-balanced-codes\"><span style=\" text-decoration: underline; color:#0000ff;\">click for more information about the algorithem</span></a></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"BalancedCodesKnuth", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("MainWindow", u"n is a length of a codeword", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">N:</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.label_9.setToolTip(QCoreApplication.translate("MainWindow", u"c is the weighted sum", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">C:</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.label_10.setToolTip(QCoreApplication.translate("MainWindow", u"d is the parity", None))
#endif // QT_CONFIG(tooltip)
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">D:</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.label_11.setToolTip(QCoreApplication.translate("MainWindow", u"P is the maximum known distance of an error", None))
#endif // QT_CONFIG(tooltip)
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">P:</span></p></body></html>", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Encode", None))
        self.shifted_encode_button.setText(QCoreApplication.translate("MainWindow", u"Encode", None))
        self.output_label_knuth_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Output:</span></p></body></html>", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Decode", None))
        self.shifted_decode_button.setText(QCoreApplication.translate("MainWindow", u"Decode", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Error index", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">U:</span></p></body></html>", None))
        self.output_label_knuth_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Output:</span></p></body></html>", None))
        self.shifted_text_encode.setPlainText("")
        self.shifted_text_encode.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter text", None))
        self.shifted_text_decode.setPlainText("")
        self.shifted_text_decode.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter text", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Params", None))
#if QT_CONFIG(tooltip)
        self.note_svtc1.setToolTip(QCoreApplication.translate("MainWindow", u"p must be O(log(n))", None))
#endif // QT_CONFIG(tooltip)
        self.note_svtc1.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/images/note4.png\"/></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.note_svtc1_2.setToolTip(QCoreApplication.translate("MainWindow", u"c must be smaller than n+1", None))
#endif // QT_CONFIG(tooltip)
        self.note_svtc1_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/images/note4.png\"/></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.infosvtc.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Algorithm implemented by : Guy Shapiraand maxim barsky</p><p>Algorithm invented by : <span style=\" font-family:'Calibri';\">Clayton Schoeny, Antonia Wachter-Zeh, Ryan Gabrys, Eitan Yaakobi</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.infosvtc.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/images/info2.png\"/></p></body></html>", None))
        self.moreinforbck_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><a href=\"https://yaakobi.wixsite.com/dnacodingsoftware/post/new-typography-lines-you-need-to-know\"><span style=\" text-decoration: underline; color:#0000ff;\">click for more information about the algorithem</span></a></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Shifted VT-Codes", None))
    # retranslateUi

