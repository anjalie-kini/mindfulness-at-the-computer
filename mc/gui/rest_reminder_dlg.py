import logging
import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import mc.mc_global
import mc.model


class RestReminderDlg(QtWidgets.QFrame):
    # close_signal = QtCore.pyqtSignal(list, list)
    rest_signal = QtCore.pyqtSignal()
    skip_signal = QtCore.pyqtSignal()
    wait_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.hover_and_kb_active_bool = False

        self.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
        )
        # | QtCore.Qt.WindowStaysOnTopHint
        # | QtCore.Qt.X11BypassWindowManagerHint

        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(1)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.reminder_qll = QtWidgets.QLabel("Please take good care of your body and mind")
        vbox_l2.addWidget(self.reminder_qll)

        hbox = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox)

        self.rest_qpb = CustomButton("Rest")
        hbox.addWidget(self.rest_qpb)
        self.rest_qpb.clicked.connect(self.on_rest_button_clicked)
        self.rest_qpb.setFont(mc.mc_global.get_font_medium(i_bold=True))
        # self.rest_qpb.clicked.connect(self.on_close_button_clicked)
        # self.rest_qpb.entered_signal.connect(self.on_close_button_hover)

        self.wait_qpb = CustomButton("Wait")
        hbox.addWidget(self.wait_qpb)
        self.wait_qpb.clicked.connect(self.on_wait_button_clicked)

        self.skip_qpb = CustomButton("Skip")
        hbox.addWidget(self.skip_qpb)
        self.skip_qpb.clicked.connect(self.on_skip_button_clicked)

        self.show()  # -done after all the widget have been added so that the right size is set
        self.raise_()
        self.showNormal()

        # Set position - done after show to get the right size hint
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        self.xpos_int = screen_qrect.left() + (screen_qrect.width() - self.sizeHint().width()) // 2
        self.ypos_int = screen_qrect.bottom() - self.sizeHint().height() - 50
        self.move(self.xpos_int, self.ypos_int)

        self.start_cursor_timer()

    def start_cursor_timer(self):
        self.cursor_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.cursor_qtimer.setSingleShot(True)
        self.cursor_qtimer.timeout.connect(self.cursor_timer_timeout)
        self.cursor_qtimer.start(2500)

    def cursor_timer_timeout(self):
        cursor = QtGui.QCursor()
        if self.geometry().contains(cursor.pos()):
            pass
        else:
            cursor.setPos(
                self.xpos_int + self.width() // 2,
                self.ypos_int + self.height() // 2
            )
            self.setCursor(cursor)

    def on_rest_button_clicked(self):
        self.rest_signal.emit()
        self.close()

    def on_skip_button_clicked(self):
        self.skip_signal.emit()
        self.close()

    def on_wait_button_clicked(self):
        self.wait_signal.emit()
        self.close()


class CustomLabel(QtWidgets.QLabel):
    def __init__(self, i_title: str):
        super().__init__(i_title)

    # Overridden
    # noinspection PyPep8Naming
    def enterEvent(self, i_QEvent):
        logging.debug("enterEvent")


class CustomButton(QtWidgets.QPushButton):
    entered_signal = QtCore.pyqtSignal()

    def __init__(self, i_title: str):
        super().__init__(i_title)

    # Overridden
    # noinspection PyPep8Naming
    def enterEvent(self, i_QEvent):
        self.entered_signal.emit()
        logging.debug("CustomButton: enterEvent")

