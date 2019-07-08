# -*- coding: utf-8 -*-
"""."""
import sys
from os.path import expanduser

import pyqrcode
from PySide2.QtCore import QFile, QBuffer, QIODevice
from PySide2.QtGui import QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (QApplication, QLineEdit, QPushButton, QLabel,
                               QSpinBox, QColorDialog, QFileDialog, QWidget)


class GenerateQRCode:
    filters = (
        'eps (*.eps);;'
        'png (*.png);;'
        'svg (*.svg)'
    )
    text = ''
    scale = 1
    fg_color = ''
    bg_color = ''

    def __init__(self, window):
        self.window = window.findChild(QWidget, 'Form')

        self.le_qr_code = window.findChild(QLineEdit, 'le_qr_code')

        self.sb_scale = window.findChild(QSpinBox, 'sb_scale')

        self.btn_fg = window.findChild(QPushButton, 'btn_fg')
        self.btn_fg.clicked.connect(lambda: self.color_picker(self.btn_fg))

        self.btn_bg = window.findChild(QPushButton, 'btn_bg')
        self.btn_bg.clicked.connect(lambda: self.color_picker(self.btn_bg))

        btn_generate_qr = window.findChild(QPushButton, 'btn_generate_qr')
        btn_generate_qr.clicked.connect(self.show_qr_code)

        self.lb_qr_img_info = window.findChild(QLabel, 'lb_qr_img_info')
        self.lb_qr_img = window.findChild(QLabel, 'lb_qr_img')

        self.btn_save_qr = window.findChild(QPushButton, 'btn_save_qr')
        self.btn_save_qr.clicked.connect(self.save_qr_code)

    def color_picker(self, button):
        color = QColorDialog.getColor()
        if color.isValid() and button.objectName() == 'btn_fg':
            self.btn_fg.setStyleSheet(f'background-color: {color.name()}')
        elif color.isValid() and button.objectName() == 'btn_bg':
            self.btn_bg.setStyleSheet(f'background-color: {color.name()}')

    def show_qr_code(self):
        buffer_png = QBuffer()
        buffer_png.open(QIODevice.ReadWrite)

        self.text = self.le_qr_code.text()
        self.fg_color = self.btn_fg.palette().button().color().name()
        self.bg_color = self.btn_bg.palette().button().color().name()
        self.scale = self.sb_scale.value()

        qrcode = pyqrcode.create(self.text)
        qrcode.png(
            file=buffer_png,
            scale=self.scale,
            module_color=self.fg_color,
            background=self.bg_color
        )

        pixmap_png = QPixmap()
        pixmap_png.loadFromData(buffer_png.buffer())
        self.lb_qr_img_info.setText(f'QR Code com {pixmap_png.width()}x{pixmap_png.height()}')
        self.lb_qr_img.setPixmap(pixmap_png)
        buffer_png.close()

    def save_qr_code(self):
        home = expanduser("~")
        response = QFileDialog.getSaveFileName(
            parent=self.window,
            caption='Salvar QR Code',
            dir=home,
            filter=self.filters,
            selectedFilter='png (*.png)'
        )
        if response[0]:
            qrcode = pyqrcode.create(self.text)
            if response[1] == 'eps (*.eps)':
                qrcode.eps(
                    file=response[0],
                    scale=self.scale,
                    module_color=self.fg_color,
                    background=self.bg_color
                )
            elif response[1] == 'png (*.png)':
                qrcode.png(
                    file=response[0],
                    scale=self.scale,
                    module_color=self.fg_color,
                    background=self.bg_color
                )
            elif response[1] == 'svg (*.svg)':
                qrcode.svg(
                    file=response[0],
                    scale=self.scale,
                    module_color=self.fg_color,
                    background=self.bg_color
                )
            self.open_dialog_success()

    def open_dialog_success(self):
        dialog_success = QFile('dialog_success.ui')
        dialog_success.open(QFile.ReadOnly)
        loader = QUiLoader()
        dialog = loader.load(dialog_success, parentWidget=self.window)
        ui_file.close()
        btn_ok = dialog.findChild(QPushButton, 'btn_ok')
        btn_ok.clicked.connect(dialog.close)
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui_file = QFile('app.ui')
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    win = loader.load(ui_file)
    ui_file.close()

    widget = GenerateQRCode(window=win)

    win.show()

    sys.exit(app.exec_())
