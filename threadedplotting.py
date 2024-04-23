import os
import sys
import socket
from numpy import pi, array, single, zeros, nan, arange, roll, cos, sin, tan, size
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from datetime import datetime
import threading
import time

FTPort = 49152
SensorConnected = False
FTSocketAddress = "192.168.1.1"
CountsPerForceAndTorque = 1000000

FTData   = array(single(zeros((6,4,2))))

AveragingWeights = [1,0,0,0]

FTSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

Bias = b'\x12\x34\x00\x42\x00\x00\x00\x00'
FTSocket.sendto(Bias,(FTSocketAddress,FTPort))

# Mechanism to support both PyQt and PySide
# -----------------------------------------

PYQT5 = "PyQt5"
PYQT6 = "PyQt6"
PYSIDE2 = "PySide2"
PYSIDE6 = "PySide6"
QT_LIB_ORDER = [PYQT5, PYSIDE2, PYSIDE6, PYQT6]
QT_LIB = os.getenv("PYQTGRAPH_QT_LIB")

# Parse optional cli argument to enfore a QT_LIB
# cli example: python benchmark.py pyside6
if len(sys.argv) > 1:
    arg1 = str(sys.argv[1]).upper()
    for i, lib in enumerate(QT_LIB_ORDER):
        if arg1 == lib.upper():
            QT_LIB = lib
            break

if QT_LIB is None:
    for lib in QT_LIB_ORDER:
        if lib in sys.modules:
            QT_LIB = lib
            break

if QT_LIB is None:
    for lib in QT_LIB_ORDER:
        try:
            __import__(lib)
            QT_LIB = lib
            break
        except ImportError:
            pass

if QT_LIB is None:
    this_file = __file__.split(os.sep)[-1]
    raise Exception(
        f"{this_file} requires PyQt5, PyQt6, PySide2 or PySide6; "
        "none of these packages could be imported."
    )

# fmt: off
# pylint: disable=import-error, no-name-in-module
if QT_LIB == PYQT5:
    from PyQt5 import QtCore, QtWidgets as QtWid           # type: ignore
    from PyQt5.QtCore import pyqtSlot as Slot              # type: ignore
elif QT_LIB == PYQT6:
    from PyQt6 import QtCore, QtWidgets as QtWid           # type: ignore
    from PyQt6.QtCore import pyqtSlot as Slot              # type: ignore
elif QT_LIB == PYSIDE2:
    from PySide2 import QtCore, QtWidgets as QtWid         # type: ignore
    from PySide2.QtCore import Slot                        # type: ignore
elif QT_LIB == PYSIDE6:
    from PySide6 import QtCore, QtWidgets as QtWid         # type: ignore
    from PySide6.QtCore import Slot                        # type: ignore
# pylint: enable=import-error, no-name-in-module
# fmt: on

# pylint: disable=c-extension-no-member
QT_VERSION = (
    QtCore.QT_VERSION_STR if QT_LIB in (PYQT5, PYQT6) else QtCore.__version__
)
# pylint: enable=c-extension-no-member

# \end[Mechanism to support both PyQt and PySide]
# -----------------------------------------------

# print("-" * 23)
# print(f"{'Python':9s} | {sys.version}")
# print(f"{QT_LIB:9s} | {QT_VERSION}")
# print(f"{'PyQtGraph':9s} | {pg.__version__}", end="")

try:
    import dvg_monkeypatch_pyqtgraph  # pylint: disable=unused-import
except ImportError:
    pass
else:
    if pg.__version__ == "0.11.0":
        print(" + dvg_monkeypatch_pyqtgraph", end="")
print()

TRY_USING_OPENGL = True
if TRY_USING_OPENGL:
    try:
        import OpenGL.GL as gl  # pylint: disable=unused-import
    except ImportError:
        print("OpenGL acceleration: Disabled")
        print("To install: `conda install pyopengl` or `pip install pyopengl`")
    else:
        from OpenGL.version import __version__ as gl_version

        # print(f"{'PyOpenGL':9s} | {gl_version}")
        pg.setConfigOptions(useOpenGL=True)
        pg.setConfigOptions(antialias=True)
        pg.setConfigOptions(enableExperimental=True)

# print("-" * 23)

try:
    from dvg_qdeviceio import QDeviceIO
except ImportError:
    print("This demo requires `dvg-qdeviceio`. It can be installed with:")
    print("  pip install dvg-qdeviceio")
    sys.exit(0)

from dvg_pyqtgraph_threadsafe import (
    ThreadSafeCurve,
    HistoryChartCurve,
    BufferedPlotCurve,
    LegendSelect,
    PlotManager,
)

# Global pyqtgraph configuration
# pg.setConfigOptions(leftButtonPan=False)
pg.setConfigOption("foreground", "#EEE")

# Constants
SamplingRate_Hz = 100  # Sampling rate of the simulated data [Hz]
DAQInterval_ms = round(1000 / 100)  # [ms]
ChartDrawInterval_ms = round(1000 / 50)  # [ms]
ChartHistoryTime_s = 10  # 10 [s]

class FTWindow(QtWid.QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle("Demo: ATI Axia80")

        # Keep track of the obtained chart refresh rate
        self.obtained_chart_rate_Hz = nan
        self.qet_chart = QtCore.QElapsedTimer()
        self.chart_rate_accumulator = 0

        # Pause/unpause charts
        self.paused = False

        # GraphicsLayoutWidget
        self.gw = pg.GraphicsLayoutWidget()
        
        self.p = {"color": "#EEE", "font-size": "12pt"}
        
        #Row, Col, Bool_SetClipToView, showGridX, showGridY, Title, XLabel, YLabel, NegXRange, PosXRange, NegYRange, PosYRange, Bool_DisableAutoRange):
        self.ForcesPlot     = self.createhistorychart(0, 0, True, 1, 1, "Force History",       "History [s]", "Force [N]",          -1.04 * ChartHistoryTime_s, ChartHistoryTime_s * 0.04, -130, 130, True)
        self.TorquesPlot    = self.createhistorychart(0, 1, True, 1, 1, "Torque History",      "History [s]", "Torque [Nm]",        -1.04 * ChartHistoryTime_s, ChartHistoryTime_s * 0.04, -.3, .3,   True)
        self.ForcesPlot1D   = self.createhistorychart(1, 0, True, 1, 1, "Force Rate History",  "History [s]", "Force Rate [N/s]",   -1.04 * ChartHistoryTime_s, ChartHistoryTime_s * 0.04, -160e-6, 160e-6,   True)
        self.TorquesPlot1D  = self.createhistorychart(1, 1, True, 1, 1, "Torque Rate History", "History [s]", "Torque Rate [Nm/s]", -1.04 * ChartHistoryTime_s, ChartHistoryTime_s * 0.04, -500e-9, 500e-9, True)
        
        
        self.ForceResolutionTextPositive=pg.TextItem("Force Resolution = 0.04 N")
        self.ForceResolutionTextNegative=pg.TextItem("Force Resolution = -0.04 N")
        
        
        self.PositionPlot = self.gw.addPlot(row = 0, col = 2)
        # self.PositionPlot.setClipToView(True)  # Note: Do not enable clip for a Lissajous. Clip only works well on uniformly monotic x-data.
        self.PositionPlot.showGrid(x=1, y=1)
        self.PositionPlot.setTitle("Positon")
        self.PositionPlot.setLabel("bottom", text="TX [Nm]", **self.p)
        self.PositionPlot.setLabel("left", text="TY [Nm]", **self.p)
        self.PositionPlot.setRange(
            xRange=[-.3, .3],
            yRange=[-.3, .3],
            disableAutoRange=True,
        )
        
        self.PositionPlot1D = self.gw.addPlot(row = 1, col = 2)
        # self.PositionPlot.setClipToView(True)  # Note: Do not enable clip for a Lissajous. Clip only works well on uniformly monotic x-data.
        self.PositionPlot1D.showGrid(x=1, y=1)
        self.PositionPlot1D.setTitle("Positon Rate")
        self.PositionPlot1D.setLabel("bottom", text="TX Rate [Nm/s]", **self.p)
        self.PositionPlot1D.setLabel("left", text="TY Rate [Nm/s]", **self.p)
        self.PositionPlot1D.setRange(
            xRange=[-500e-9, 500e-9],
            yRange=[-500e-9, 500e-9],
            disableAutoRange=True,
        )

        capacity = round(ChartHistoryTime_s * SamplingRate_Hz)
        #capacity = 100000000
        
        #history chart curve creater
                                                        #capacity, Parent_Plot, Red, Green, Blue, Width
        self.FXCurve    = self.historychartcurve(capacity, self.ForcesPlot, 255, 0, 0, 3, "FX")
        self.FYCurve    = self.historychartcurve(capacity, self.ForcesPlot, 0, 255, 0, 3, "FY")
        self.FZCurve    = self.historychartcurve(capacity, self.ForcesPlot, 0, 0, 255, 3, "FZ")
        self.TXCurve    = self.historychartcurve(capacity, self.TorquesPlot, 255, 125, 125, 3, "TX")
        self.TYCurve    = self.historychartcurve(capacity, self.TorquesPlot, 125, 255, 125, 3, "TY")
        self.TZCurve    = self.historychartcurve(capacity, self.TorquesPlot, 125, 125, 255, 3, "TZ")
        
        self.FXCurve1D  = self.historychartcurve(capacity, self.ForcesPlot1D, 255, 0, 0, 3, "FX 1D")
        self.FYCurve1D  = self.historychartcurve(capacity, self.ForcesPlot1D, 0, 255, 0, 3, "FY 1D")
        self.FZCurve1D  = self.historychartcurve(capacity, self.ForcesPlot1D, 0, 0, 255, 3, "FZ 1D")
        self.TXCurve1D  = self.historychartcurve(capacity, self.TorquesPlot1D, 255, 125, 125, 3, "TX 1D")
        self.TYCurve1D  = self.historychartcurve(capacity, self.TorquesPlot1D, 125, 255, 125, 3, "TY 1D")
        self.TZCurve1D  = self.historychartcurve(capacity, self.TorquesPlot1D, 125, 125, 255, 3, "TZ 1D")
        
        self.XYCurve = BufferedPlotCurve(
            capacity=capacity,
            linked_curve=self.PositionPlot.plot(
                pen=pg.mkPen(color=[255, 255, 255], width=3), name="XY Position"
            ),
        )
        self.XYCurve1D = BufferedPlotCurve(
            capacity=capacity,
            linked_curve=self.PositionPlot1D.plot(
                pen=pg.mkPen(color=[255, 255, 255], width=3), name="XY Position 1D"
            ),
        )
        

        # Extra marker to indicate tracking position of Lissajous curve
        self.PositionMarker = self.PositionPlot.plot(
            pen=None,
            symbol="o",
            symbolPen=None,
            symbolBrush=pg.mkBrush([255, 255, 255]),
            symbolSize=16,
        )
        self.PositionMarker1D = self.PositionPlot1D.plot(
            pen=None,
            symbol="o",
            symbolPen=None,
            symbolBrush=pg.mkBrush([255, 255, 255]),
            symbolSize=16,
        )

        self.All_Plots = [
            self.ForcesPlot,
            self.TorquesPlot,
            self.ForcesPlot1D,
            self.TorquesPlot1D,
            self.PositionPlot,
            self.PositionPlot1D
            ]
        
        self.HistoryPlots = self.All_Plots[0:3]
        
        
        self.All_Curves = [
            self.FXCurve,
            self.FYCurve,
            self.FZCurve,
            self.TXCurve,
            self.TYCurve,
            self.TZCurve,
            
            self.FXCurve1D,
            self.FYCurve1D,
            self.FZCurve1D,
            self.TXCurve1D,
            self.TYCurve1D,
            self.TZCurve1D,
            
            self.XYCurve,
            self.XYCurve1D,
            self.PositionMarker
        ]
        
        self.HistoryCurves = self.All_Curves[0:12]


        # 'Obtained rates'
        self.qlbl_DAQ_rate = QtWid.QLabel("")
        self.qlbl_DAQ_rate.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.qlbl_DAQ_rate.setMinimumWidth(50)
        self.qlbl_chart_rate = QtWid.QLabel("")
        self.qlbl_chart_rate.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.qlbl_num_points = QtWid.QLabel("")
        self.qlbl_num_points.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        # fmt: off
        grid_rates = QtWid.QGridLayout()
        grid_rates.addWidget(QtWid.QLabel("DAQ:")  , 0, 0)
        grid_rates.addWidget(self.qlbl_DAQ_rate    , 0, 1)
        grid_rates.addWidget(QtWid.QLabel("Hz")    , 0, 2)
        grid_rates.addWidget(QtWid.QLabel("chart:"), 1, 0)
        grid_rates.addWidget(self.qlbl_chart_rate  , 1, 1)
        grid_rates.addWidget(QtWid.QLabel("Hz")    , 1, 2)
        grid_rates.addWidget(QtWid.QLabel("drawn:"), 2, 0)
        grid_rates.addWidget(self.qlbl_num_points  , 2, 1)
        grid_rates.addWidget(QtWid.QLabel("pnts")  , 2, 2)
        grid_rates.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        # fmt: on

        # 'Legend'
        legend = LegendSelect(linked_curves=self.All_Curves)
        qgrp_legend = QtWid.QGroupBox("LegendSelect")
        qgrp_legend.setLayout(legend.grid)

        # Update `number of points drawn` at each click `show/hide curve`
        for chkb in legend.chkbs:
            chkb.clicked.connect(self.update_num_points_drawn)

        # `PlotManager`
        self.qpbt_pause_chart = QtWid.QPushButton("Pause", checkable=True)
        self.qpbt_pause_chart.clicked.connect(self.process_qpbt_pause_chart)

        self.plot_manager = PlotManager(parent=self)
        self.plot_manager.grid.addWidget(self.qpbt_pause_chart, 0, 0, 1, 2)
        self.plot_manager.grid.addItem(QtWid.QSpacerItem(0, 10), 1, 0)
        self.plot_manager.add_autorange_buttons(
            linked_plots=[self.All_Plots]
        )
        self.plot_manager.add_preset_buttons(
            linked_plots=self.HistoryPlots,
            linked_curves=self.HistoryCurves,
            presets=[
                {
                    "button_label": "0.100",
                    "x_axis_label": "History [ms]",
                    "x_axis_divisor": 1e-3,
                    "x_axis_range": (-101, 0),
                },
                {
                    "button_label": "0:05",
                    "x_axis_label": "History [s]",
                    "x_axis_divisor": 1,
                    "x_axis_range": (-5.05, 0),
                },
                {
                    "button_label": "0:10",
                    "x_axis_label": "History [s]",
                    "x_axis_divisor": 1,
                    "x_axis_range": (-10.1, 0),
                },
            ],
        )

        qgrp_plotmgr = QtWid.QGroupBox("PlotManager")
        qgrp_plotmgr.setLayout(self.plot_manager.grid)

        self.Bias = QtWid.QPushButton("Bias", checkable=True)
        self.Bias.clicked.connect(self.biascommand)
        
        self.Quit = QtWid.QPushButton("Quit", checkable=True)
        self.Quit.clicked.connect(self.quitcommand)
        
        # Round up right panel
        vbox = QtWid.QVBoxLayout()
        vbox.addLayout(grid_rates)
        vbox.addWidget(qgrp_legend)
        vbox.addWidget(qgrp_plotmgr, stretch=0)
        vbox.addWidget(self.Bias)
        vbox.addWidget(self.Quit)
        vbox.addStretch()

        # Round up frame
        hbox = QtWid.QHBoxLayout()
        hbox.addWidget(self.gw, 1)
        hbox.addLayout(vbox, 0)

        # -------------------------
        #   Round up full window
        # -------------------------

        vbox = QtWid.QVBoxLayout(self)
        vbox.addLayout(hbox, stretch=1)

    # --------------------------------------------------------------------------
    #   Handle controls
    # --------------------------------------------------------------------------

    @Slot()
    #History Chart Creater
    def createhistorychart(self, Row, Col, Bool_SetClipToView, showGridX, 
                           showGridY, Title, XLabel, YLabel, NegXRange, 
                           PosXRange, NegYRange, PosYRange, 
                           Bool_DisableAutoRange
                           ):
        History_Chart = self.gw.addPlot(row = Row, col = Col)
        History_Chart.setClipToView(Bool_SetClipToView)
        History_Chart.showGrid(x=showGridX, y=showGridY)
        History_Chart.setTitle(Title)
        History_Chart.setLabel("bottom", text=XLabel, **self.p)
        History_Chart.setLabel("left", text=YLabel, **self.p)
        History_Chart.setRange(
            xRange=[NegXRange, PosXRange],
            yRange=[NegYRange, PosYRange],
            disableAutoRange=Bool_DisableAutoRange,)
        
        return History_Chart
    
    
    #history chart curve creater
    def historychartcurve(self, capacity, Parent_Plot, Red, Green, Blue, Width,
                          Name):
        return HistoryChartCurve(
            capacity=capacity,
            linked_curve=Parent_Plot.plot(
                pen=pg.mkPen(color=[Red, Green, Blue], width=Width), name=Name
            ),
        )
    def process_qpbt_pause_chart(self):
        if self.paused:
            self.qpbt_pause_chart.setText("Pause")
            self.paused = False
        else:
            self.qpbt_pause_chart.setText("Paused")
            self.paused = True
    def biascommand(self):
        Bias = b'\x12\x34\x00\x42\x00\x00\x00\x00'
        FTSocket.sendto(Bias,(FTSocketAddress,FTPort))
        
    def quitcommand(self):
        QtGui.QApplication.closeAllWindows()
        
    def update_num_points_drawn(self):
        # Keep track of the number of drawn points
        num_points = 0
        for tscurve in self.All_Curves:
            if tscurve.isVisible():
                num_points += (
                    0
                    if tscurve.curve.xData is None
                    else len(tscurve.curve.xData)
                )

        self.qlbl_num_points.setText("%s" % f"{(num_points):,}")

    @Slot()
    def update_curves(self):
        for tscurve in self.All_Curves:
            tscurve.update()

        if self.FXCurve.curve.xData is not None:
            if len(self.FXCurve.curve.xData) > 0:
                self.PositionMarker.setData(
                    [self.TXCurve.curve.yData[-1]],
                    [self.TYCurve.curve.yData[-1]],
                )
                self.PositionMarker1D.setData(
                    [self.TXCurve1D.curve.yData[-1]],
                    [self.TYCurve1D.curve.yData[-1]],
                )

    @Slot()
    def update_charts(self):
        # Keep track of the obtained chart rate
        if not self.qet_chart.isValid():
            self.qet_chart.start()
        else:
            self.chart_rate_accumulator += 1
            dT = self.qet_chart.elapsed()

            if dT >= 1000:  # Evaluate every N elapsed milliseconds
                self.qet_chart.restart()
                try:
                    self.obtained_chart_rate_Hz = (
                        self.chart_rate_accumulator / dT * 1e3
                    )
                except ZeroDivisionError:
                    self.obtained_chart_rate_Hz = nan

                self.chart_rate_accumulator = 0

        # Update curves
        if not self.paused:
            self.qlbl_chart_rate.setText("%.1f" % self.obtained_chart_rate_Hz)
            self.update_num_points_drawn()
            self.update_curves()

    @Slot()
    def update_GUI(self):
        self.qlbl_DAQ_rate.setText("%.1f"% Sensor_QDevice.obtained_DAQ_rate_Hz)


# @Slot()
# def about_to_quit():
#     Sensor_QDevice.quit()
#     timer_chart.stop()


class Sensor_Read:
    """Simulates a data acquisition (DAQ) device that will generate data at a
    fixed sample rate. It will push the data into the passed `ThreadSaveCurve`
    instances.
    """
    def __init__(
        self,
        FXCurve_: ThreadSafeCurve,
        FYCurve_: ThreadSafeCurve,
        FZCurve_: ThreadSafeCurve,
        TXCurve_: ThreadSafeCurve,
        TYCurve_: ThreadSafeCurve,
        TZCurve_: ThreadSafeCurve,
        
        FXCurve1D_: ThreadSafeCurve,
        FYCurve1D_: ThreadSafeCurve,
        FZCurve1D_: ThreadSafeCurve,
        TXCurve1D_: ThreadSafeCurve,
        TYCurve1D_: ThreadSafeCurve,
        TZCurve1D_: ThreadSafeCurve,
        
        XYCurve_: ThreadSafeCurve,
        XYCurve1D_: ThreadSafeCurve,
    ):
        self.name = "Sensor_Read"
        self.is_alive = True
        
        self.FXCurve = FXCurve_
        self.FYCurve = FYCurve_
        self.FZCurve = FZCurve_
        self.TXCurve = TXCurve_
        self.TYCurve = TYCurve_
        self.TZCurve = TZCurve_
        
        self.FXCurve1D = FXCurve1D_
        self.FYCurve1D = FYCurve1D_
        self.FZCurve1D = FZCurve1D_
        self.TXCurve1D = TXCurve1D_
        self.TYCurve1D = TYCurve1D_
        self.TZCurve1D = TZCurve1D_
        self.XYCurve1D = XYCurve1D_
        
        self.XYCurve = XYCurve_
        
        self.Sensor_All_Curves = [
            self.FXCurve,
            self.FYCurve,
            self.FZCurve,
            self.TXCurve,
            self.TYCurve,
            self.TZCurve,
            
            self.FXCurve1D,
            self.FYCurve1D,
            self.FZCurve1D,
            self.TXCurve1D,
            self.TYCurve1D,
            self.TZCurve1D,
            
            self.XYCurve,
            self.XYCurve1D
            ]

    def generate_data(self):
        
        if self.FXCurve.size[0] == 0:
            x_0 = 0
        else:
            # Pick up the previously last phase of the sine
            # fmt: off
            x_0 = self.FXCurve._buffer_x[-1]  # pylint: disable=protected-access
            # fmt: on
        
        x = (1 + arange(DAQInterval_ms * SamplingRate_Hz / 1e3)
             ) / SamplingRate_Hz + x_0
        
        if SensorConnected:
            request = b'\x12\x34\x00\x02\x00\x00\x00\x01'
    
            FTSocket.sendto(request,(FTSocketAddress,FTPort))
            data, addr = FTSocket.recvfrom(36)
        
            
            
        FTData[:,:,:] = roll(FTData, 1, axis = 1)    
        FTData_Averaged = array(single(zeros((6,1,2))))
        for i in range(0,6,1):
            if SensorConnected:
                FTData[i,0,0] = int.from_bytes(data[12+i*4:15+i*4],
                                               'big',signed=True
                                               )/CountsPerForceAndTorque*256
            else:
                FX = cos(datetime.now().second/60*2*pi)
                FY = sin(datetime.now().second/60*2*pi)
                FZ = tan(datetime.now().second/60*2*pi)
                TX = -cos(datetime.now().second/60*2*pi)
                TY = -sin(datetime.now().second/60*2*pi)
                TZ = -tan(datetime.now().second/60*2*pi)
                FTData[i,0,0] = array([FX, FY, FZ, TX, TY, TZ])[i]
            
            #first derivative
            FTData[i,0,1]= (FTData[i,0,0]-FTData[i,1,0]) /(DAQInterval_ms*1000) 
            for j in range(0,4,1):
                FTData_Averaged[i,0,0] = FTData_Averaged[i,0,0] + AveragingWeights[j] * FTData[i,0,0]
                FTData_Averaged[i,0,1] = FTData_Averaged[i,0,1] + AveragingWeights[j] * FTData[i,0,1]
          
        for i in range(0,size(self.Sensor_All_Curves)):
            if i < 6: #0th derivative
                self.Sensor_All_Curves[i].extendData(x,[FTData_Averaged[i,0,0].tolist()])
            elif i >= 6 and i < 12: #1st derivative
                self.Sensor_All_Curves[i].extendData(x,[FTData_Averaged[i-6,0,1].tolist()])
            elif i == 12: #positional
                self.XYCurve.extendData([FTData_Averaged[3,0,0].tolist()], [FTData_Averaged[4,0,0].tolist()])
            elif i == 13: #1st derivative positional
                self.XYCurve1D.extendData([FTData_Averaged[3,0,1].tolist()], [FTData_Averaged[4,0,1].tolist()])
        
        return True

def showFT(window):
    window.show()

if __name__ == "__main__":
    app = QtWid.QApplication(sys.argv)
    # app.aboutToQuit.connect(about_to_quit)

    window = FTWindow()

    # Sensor_Read:
    #   Simulates a data acquisition (DAQ) device that will generate data at a
    #   fixed sample rate. It will push the data into the passed
    #   `ThreadSaveCurve` instances.
    # QDeviceIO:
    #   Creates and manages a new thread for `Sensor_Device`. A worker will
    #   perdiocally activate `Sensor_Device` from out of this new thread.
    Sensor_Device = Sensor_Read(window.FXCurve, 
                          window.FYCurve, 
                          window.FZCurve,
                          window.TXCurve,
                          window.TYCurve,
                          window.TZCurve,
                          window.FXCurve1D,
                          window.FYCurve1D,
                          window.FZCurve1D,
                          window.TXCurve1D,
                          window.TYCurve1D,
                          window.TZCurve1D,
                          window.XYCurve,
                          window.XYCurve1D)
    Sensor_QDevice = QDeviceIO(Sensor_Device)
    Sensor_QDevice.create_worker_DAQ(
        DAQ_interval_ms=DAQInterval_ms,
        DAQ_function=Sensor_Device.generate_data,
    )
    Sensor_QDevice.signal_DAQ_updated.connect(window.update_GUI)
    Sensor_QDevice.start()

    # Chart refresh timer
    timer_chart = QtCore.QTimer(timerType=QtCore.Qt.TimerType.PreciseTimer)
    timer_chart.timeout.connect(window.update_charts)
    timer_chart.start(ChartDrawInterval_ms)
    window.show()
    # app.exec()
    i = 0
    while i < 100000:
        window.update_charts
        # window.update_GUI
        print(i)
        time.sleep(1)
        i = i+1
    
    # FTWindowThread = threading.Thread(target = showFT(window))
    # FTWindowThread.start()
    # FTWindowThread.join()
    # if QT_LIB in (PYQT5, PYSIDE2):
    #     sys.exit(app.exec_())
    # else:
    #     sys.exit(app.exec())
        
    sys.exit(0)