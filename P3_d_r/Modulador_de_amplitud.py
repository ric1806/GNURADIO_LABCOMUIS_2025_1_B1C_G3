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
import os
import sys
import logging as log

def get_state_directory() -> str:
    oldpath = os.path.expanduser("~/.grc_gnuradio")
    try:
        from gnuradio.gr import paths
        newpath = paths.persistent()
        if os.path.exists(newpath):
            return newpath
        if os.path.exists(oldpath):
            log.warning(f"Found persistent state path '{newpath}', but file does not exist. " +
                     f"Old default persistent state path '{oldpath}' exists; using that. " +
                     "Please consider moving state to new location.")
            return oldpath
        # Default to the correct path if both are configured.
        # neither old, nor new path exist: create new path, return that
        os.makedirs(newpath, exist_ok=True)
        return newpath
    except (ImportError, NameError):
        log.warning("Could not retrieve GNU Radio persistent state directory from GNU Radio. " +
                 "Trying defaults.")
        xdgstate = os.getenv("XDG_STATE_HOME", os.path.expanduser("~/.local/state"))
        xdgcand = os.path.join(xdgstate, "gnuradio")
        if os.path.exists(xdgcand):
            return xdgcand
        if os.path.exists(oldpath):
            log.warning(f"Using legacy state path '{oldpath}'. Please consider moving state " +
                     f"files to '{xdgcand}'.")
            return oldpath
        # neither old, nor new path exist: create new path, return that
        os.makedirs(xdgcand, exist_ok=True)
        return xdgcand

sys.path.append(os.environ.get('GRC_HIER_PATH', get_state_directory()))

from ModuloAMG2 import ModuloAMG2  # grc-generated hier_block
from PyQt5 import QtCore
from gnuradio import blocks
import numpy
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import math
import sip
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
        self.samp_rate = samp_rate = 12500000/8
        self.n = n = 2
        self.Ka = Ka = 1
        self.GTX = GTX = 0
        self.Fc = Fc = 50e6
        self.FM = FM = 1e3
        self.B = B = 10
        self.Ac = Ac = 125e-3
        self.AM = AM = 1

        ##################################################
        # Blocks
        ##################################################

        self._Ka_range = qtgui.Range(0, 4, 0.1, 1, 200)
        self._Ka_win = qtgui.RangeWidget(self._Ka_range, self.set_Ka, "Coeficiente Ka", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Ka_win)
        self._GTX_range = qtgui.Range(0, 30, 1, 0, 200)
        self._GTX_win = qtgui.RangeWidget(self._GTX_range, self.set_GTX, "Ganacia transmisor", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._GTX_win)
        self._Fc_range = qtgui.Range(50e6, 02.2e9, 1e6, 50e6, 200)
        self._Fc_win = qtgui.RangeWidget(self._Fc_range, self.set_Fc, "Frecuencia portadora", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Fc_win)
        self._B_range = qtgui.Range(1, 20, 1, 10, 200)
        self._B_win = qtgui.RangeWidget(self._B_range, self.set_B, "# muestras por simbolo", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._B_win)
        self._Ac_range = qtgui.Range(0, 1, 1e-3, 125e-3, 200)
        self._Ac_win = qtgui.RangeWidget(self._Ac_range, self.set_Ac, "Amplitud portadora", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Ac_win)
        self.uhd_usrp_sink_1 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_1.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_1.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_1.set_center_freq(Fc, 0)
        self.uhd_usrp_sink_1.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_1.set_gain(GTX, 0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, B)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((1/math.pow(2,n)))
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-(math.pow(2,n)-1)/2))
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, int(math.pow(2,n)), 1000))), True)
        self.ModuloAMG2_0 = ModuloAMG2(
            Ac=Ac,
            ka=Ka,
        )
        self._FM_range = qtgui.Range(300, samp_rate/4, 100, 1e3, 200)
        self._FM_win = qtgui.RangeWidget(self._FM_range, self.set_FM, "Frecuencia de mensaje", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._FM_win)
        self._AM_range = qtgui.Range(0, 4, 100e-3, 1, 200)
        self._AM_win = qtgui.RangeWidget(self._AM_range, self.set_AM, "Amplitud mensaje", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._AM_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.ModuloAMG2_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.ModuloAMG2_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.ModuloAMG2_0, 0), (self.uhd_usrp_sink_1, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.ModuloAMG2_0, 0))
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
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_1.set_samp_rate(self.samp_rate)

    def get_n(self):
        return self.n

    def set_n(self, n):
        self.n = n
        self.blocks_add_const_vxx_0.set_k((-(math.pow(2,self.n)-1)/2))
        self.blocks_multiply_const_vxx_0.set_k((1/math.pow(2,self.n)))

    def get_Ka(self):
        return self.Ka

    def set_Ka(self, Ka):
        self.Ka = Ka
        self.ModuloAMG2_0.set_ka(self.Ka)

    def get_GTX(self):
        return self.GTX

    def set_GTX(self, GTX):
        self.GTX = GTX
        self.uhd_usrp_sink_1.set_gain(self.GTX, 0)

    def get_Fc(self):
        return self.Fc

    def set_Fc(self, Fc):
        self.Fc = Fc
        self.uhd_usrp_sink_1.set_center_freq(self.Fc, 0)

    def get_FM(self):
        return self.FM

    def set_FM(self, FM):
        self.FM = FM

    def get_B(self):
        return self.B

    def set_B(self, B):
        self.B = B
        self.blocks_repeat_0.set_interpolation(self.B)

    def get_Ac(self):
        return self.Ac

    def set_Ac(self, Ac):
        self.Ac = Ac
        self.ModuloAMG2_0.set_Ac(self.Ac)

    def get_AM(self):
        return self.AM

    def set_AM(self, AM):
        self.AM = AM




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
