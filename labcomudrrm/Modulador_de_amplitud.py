#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Modulador de amplitud
# GNU Radio version: v3.10.11.0-89-ga17f69e7

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
import numpy
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import math
import threading



class Modulador_de_amplitud(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Modulador de amplitud", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Modulador de amplitud")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Modulador_de_amplitud")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 125e5/8
        self.n = n = 2
        self.fm = fm = 1e3
        self.Ka = Ka = 1
        self.GTX = GTX = 0
        self.Fc = Fc = 50e6
        self.B = B = 10
        self.Am = Am = 1
        self.Ac = Ac = 125e-3

        ##################################################
        # Blocks
        ##################################################

        self._B_range = qtgui.Range(1, 20, 1, 10, 200)
        self._B_win = qtgui.RangeWidget(self._B_range, self.set_B, "# muestras por simbolo", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._B_win)
        self._fm_range = qtgui.Range(300, samp_rate/4, 100, 1e3, 200)
        self._fm_win = qtgui.RangeWidget(self._fm_range, self.set_fm, "Frecuencia del mensaje", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._fm_win)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, B)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((1/math.pow(2,n)))
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-(math.pow(2,n)-1)/2))
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, int(math.pow(2,n)), 1000))), True)
        self._Ka_range = qtgui.Range(0, 4, 0.05, 1, 200)
        self._Ka_win = qtgui.RangeWidget(self._Ka_range, self.set_Ka, "coeficiente Ka", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Ka_win)
        self._GTX_range = qtgui.Range(0, 30, 1, 0, 200)
        self._GTX_win = qtgui.RangeWidget(self._GTX_range, self.set_GTX, "ganancia transmisor", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._GTX_win)
        self._Fc_range = qtgui.Range(50e6, 2.2e9, 1e6, 50e6, 200)
        self._Fc_win = qtgui.RangeWidget(self._Fc_range, self.set_Fc, "frecuencia de la portadora", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Fc_win)
        self._Am_range = qtgui.Range(0, 4, 100e-3, 1, 200)
        self._Am_win = qtgui.RangeWidget(self._Am_range, self.set_Am, "Amplitud del mensaje", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Am_win)
        self._Ac_range = qtgui.Range(0, 1, 1e-3, 125e-3, 200)
        self._Ac_win = qtgui.RangeWidget(self._Ac_range, self.set_Ac, "Amplitud de la portadora", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Ac_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_repeat_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Modulador_de_amplitud")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_n(self):
        return self.n

    def set_n(self, n):
        self.n = n
        self.blocks_add_const_vxx_0.set_k((-(math.pow(2,self.n)-1)/2))
        self.blocks_multiply_const_vxx_0.set_k((1/math.pow(2,self.n)))

    def get_fm(self):
        return self.fm

    def set_fm(self, fm):
        self.fm = fm

    def get_Ka(self):
        return self.Ka

    def set_Ka(self, Ka):
        self.Ka = Ka

    def get_GTX(self):
        return self.GTX

    def set_GTX(self, GTX):
        self.GTX = GTX

    def get_Fc(self):
        return self.Fc

    def set_Fc(self, Fc):
        self.Fc = Fc

    def get_B(self):
        return self.B

    def set_B(self, B):
        self.B = B
        self.blocks_repeat_0.set_interpolation(self.B)

    def get_Am(self):
        return self.Am

    def set_Am(self, Am):
        self.Am = Am

    def get_Ac(self):
        return self.Ac

    def set_Ac(self, Ac):
        self.Ac = Ac




def main(top_block_cls=Modulador_de_amplitud, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
