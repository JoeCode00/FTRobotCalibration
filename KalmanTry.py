import os
import sys
import socket
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from pykalman import KalmanFilter



Port = 49152
Command = 2
Num_Samples = 1
sockaddr_in = "192.168.1.1"
cpft = 1000000

FTData   = np.array(np.single(np.zeros((6,10,2))))
FTData_Entries = 0


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

bias = b'\x12\x34\x00\x42\x00\x00\x00\x00'
sock.sendto(bias,(sockaddr_in,Port))

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

print("-" * 23)
print(f"{'Python':9s} | {sys.version}")
print(f"{QT_LIB:9s} | {QT_VERSION}")
print(f"{'PyQtGraph':9s} | {pg.__version__}", end="")

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

        print(f"{'PyOpenGL':9s} | {gl_version}")
        pg.setConfigOptions(useOpenGL=True)
        pg.setConfigOptions(antialias=True)
        pg.setConfigOptions(enableExperimental=True)

print("-" * 23)

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
Fs = 100  # Sampling rate of the simulated data [Hz]
WORKER_DAQ_INTERVAL_MS = round(1000 / 100)  # [ms]
CHART_DRAW_INTERVAL_MS = round(1000 / 50)  # [ms]
CHART_HISTORY_TIME = 10  # 10 [s]

# ------------------------------------------------------------------------------
#   MainWindow
# ------------------------------------------------------------------------------

class MainWindow(QtWid.QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.setGeometry(350, 50, 1200, 660)
        self.setWindowTitle("Demo: dvg_pyqtgraph_threadsafe")

        # Keep track of the obtained chart refresh rate
        self.obtained_chart_rate_Hz = np.nan
        self.qet_chart = QtCore.QElapsedTimer()
        self.chart_rate_accumulator = 0

        # Pause/unpause charts
        self.paused = False

        # GraphicsLayoutWidget
        self.gw = pg.GraphicsLayoutWidget()
        
        self.p = {"color": "#EEE", "font-size": "12pt"}
        
        #                                                 Row, Col, Bool_SetClipToView, showGridX, showGridY, Title, XLabel,      YLabel,                     NegXRange,     PosXRange, NegYRange, PosYRange, Bool_DisableAutoRange):
        self.Forces_Plot                    = self.Create_History_Chart(0, 0, True, 1, 1, "Force History",       "History [s]", "Force [N]",          -1.04 * CHART_HISTORY_TIME, CHART_HISTORY_TIME * 0.04, -130, 130, True)
        self.Torques_Plot                   = self.Create_History_Chart(0, 1, True, 1, 1, "Torque History",      "History [s]", "Torque [Nm]",        -1.04 * CHART_HISTORY_TIME, CHART_HISTORY_TIME * 0.04, -.3, .3,   True)
        self.Forces_Plot_1st_Derivative     = self.Create_History_Chart(1, 0, True, 1, 1, "Force Rate History",  "History [s]", "Force Rate [N/s]",   -1.04 * CHART_HISTORY_TIME, CHART_HISTORY_TIME * 0.04, -160e-6, 160e-6,   True)
        self.Torques_Plot_1st_Derivative    = self.Create_History_Chart(1, 1, True, 1, 1, "Torque Rate History", "History [s]", "Torque Rate [Nm/s]", -1.04 * CHART_HISTORY_TIME, CHART_HISTORY_TIME * 0.04, -500e-9, 500e-9, True)
        
        
        
        self.Position_Plot = self.gw.addPlot(row = 0, col = 2)
        # self.Position_Plot.setClipToView(True)  # Note: Do not enable clip for a Lissajous. Clip only works well on uniformly monotic x-data.
        self.Position_Plot.showGrid(x=1, y=1)
        self.Position_Plot.setTitle("Positon")
        self.Position_Plot.setLabel("bottom", text="TX", **self.p)
        self.Position_Plot.setLabel("left", text="TY", **self.p)
        self.Position_Plot.setRange(
            xRange=[-.3, .3],
            yRange=[-.3, .3],
            disableAutoRange=True,
        )
        
        self.Position_Plot_1st_Derivative = self.gw.addPlot(row = 1, col = 2)
        # self.Position_Plot.setClipToView(True)  # Note: Do not enable clip for a Lissajous. Clip only works well on uniformly monotic x-data.
        self.Position_Plot_1st_Derivative.showGrid(x=1, y=1)
        self.Position_Plot_1st_Derivative.setTitle("Positon Rate")
        self.Position_Plot_1st_Derivative.setLabel("bottom", text="TX 1D", **self.p)
        self.Position_Plot_1st_Derivative.setLabel("left", text="TY 1D", **self.p)
        self.Position_Plot_1st_Derivative.setRange(
            xRange=[-500e-9, 500e-9],
            yRange=[-500e-9, 500e-9],
            disableAutoRange=True,
        )

        capacity = round(CHART_HISTORY_TIME * Fs)
        #capacity = 100000000
        
        #history chart curve creater
                                                        #capacity, Parent_Plot, Red, Green, Blue, Width
        self.FX_Curve = self.Create_History_Chart_Curve(capacity, self.Forces_Plot, 255, 0, 0, 3, "FX")
        self.FY_Curve = self.Create_History_Chart_Curve(capacity, self.Forces_Plot, 0, 255, 0, 3, "FY")
        self.FZ_Curve = self.Create_History_Chart_Curve(capacity, self.Forces_Plot, 0, 0, 255, 3, "FZ")
        self.FZ_Curve_Filtered = self.Create_History_Chart_Curve(capacity, self.Forces_Plot, 255, 255, 255, 3, "FZ Filtered")
        self.TX_Curve = self.Create_History_Chart_Curve(capacity, self.Torques_Plot, 255, 125, 125, 3, "TX")
        self.TY_Curve = self.Create_History_Chart_Curve(capacity, self.Torques_Plot, 125, 255, 125, 3, "TY")
        self.TZ_Curve = self.Create_History_Chart_Curve(capacity, self.Torques_Plot, 125, 125, 255, 3, "TZ")
        
        self.FX_Curve_1st_Derivative = self.Create_History_Chart_Curve(capacity, self.Forces_Plot_1st_Derivative, 255, 0, 0, 3, "FX 1D")
        self.FY_Curve_1st_Derivative = self.Create_History_Chart_Curve(capacity, self.Forces_Plot_1st_Derivative, 0, 255, 0, 3, "FY 1D")
        self.FZ_Curve_1st_Derivative = self.Create_History_Chart_Curve(capacity, self.Forces_Plot_1st_Derivative, 0, 0, 255, 3, "FZ 1D")
        self.TX_Curve_1st_Derivative = self.Create_History_Chart_Curve(capacity, self.Torques_Plot_1st_Derivative, 255, 125, 125, 3, "TX 1D")
        self.TY_Curve_1st_Derivative = self.Create_History_Chart_Curve(capacity, self.Torques_Plot_1st_Derivative, 125, 255, 125, 3, "TY 1D")
        self.TZ_Curve_1st_Derivative = self.Create_History_Chart_Curve(capacity, self.Torques_Plot_1st_Derivative, 125, 125, 255, 3, "TZ 1D")
        
        self.XY_Curve = BufferedPlotCurve(
            capacity=capacity,
            linked_curve=self.Position_Plot.plot(
                pen=pg.mkPen(color=[255, 255, 255], width=3), name="XY Position"
            ),
        )
        self.XY_Curve_1st_Derivative = BufferedPlotCurve(
            capacity=capacity,
            linked_curve=self.Position_Plot_1st_Derivative.plot(
                pen=pg.mkPen(color=[255, 255, 255], width=3), name="XY Position 1D"
            ),
        )
        

        # Extra marker to indicate tracking position of Lissajous curve
        self.Position_Marker = self.Position_Plot.plot(
            pen=None,
            symbol="o",
            symbolPen=None,
            symbolBrush=pg.mkBrush([255, 255, 255]),
            symbolSize=16,
        )
        self.Position_Marker_1st_Derivative = self.Position_Plot_1st_Derivative.plot(
            pen=None,
            symbol="o",
            symbolPen=None,
            symbolBrush=pg.mkBrush([255, 255, 255]),
            symbolSize=16,
        )

        self.All_Plots = [
            self.Forces_Plot,
            self.Torques_Plot,
            self.Forces_Plot_1st_Derivative,
            self.Torques_Plot_1st_Derivative,
            self.Position_Plot,
            self.Position_Plot_1st_Derivative
            ]
        
        self.History_Plots = self.All_Plots[0:3]
        
        
        self.All_Curves = [
            self.FX_Curve,
            self.FY_Curve,
            self.FZ_Curve,
            self.FZ_Curve_Filtered,
            self.TX_Curve,
            self.TY_Curve,
            self.TZ_Curve,
            
            self.FX_Curve_1st_Derivative,
            self.FY_Curve_1st_Derivative,
            self.FZ_Curve_1st_Derivative,
            self.TX_Curve_1st_Derivative,
            self.TY_Curve_1st_Derivative,
            self.TZ_Curve_1st_Derivative,
            
            self.XY_Curve,
            self.XY_Curve_1st_Derivative,
            self.Position_Marker
        ]
        
        self.History_Curves = self.All_Curves[0:13]


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
            linked_plots=self.History_Plots,
            linked_curves=self.History_Curves,
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
        self.Bias.clicked.connect(self.Bias_Command)
        
        self.Quit = QtWid.QPushButton("Quit", checkable=True)
        self.Quit.clicked.connect(self.Quit_Command)
        
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
    def Create_History_Chart(self, Row, Col, Bool_SetClipToView, showGridX, showGridY, Title, XLabel, YLabel, NegXRange, PosXRange, NegYRange, PosYRange, Bool_DisableAutoRange):
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
    def Create_History_Chart_Curve(self, capacity, Parent_Plot, Red, Green, Blue, Width, Name):
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
    def Bias_Command(self):
        bias = b'\x12\x34\x00\x42\x00\x00\x00\x00'
        sock.sendto(bias,(sockaddr_in,Port))
        global FTData_Entries
        FTData_Entries = 0
        
    def Quit_Command(self):
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

        if self.FX_Curve.curve.xData is not None:
            if len(self.FX_Curve.curve.xData) > 0:
                self.Position_Marker.setData(
                    [self.TX_Curve.curve.yData[-1]],
                    [self.TY_Curve.curve.yData[-1]],
                )
                self.Position_Marker_1st_Derivative.setData(
                    [self.TX_Curve_1st_Derivative.curve.yData[-1]],
                    [self.TY_Curve_1st_Derivative.curve.yData[-1]],
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
                    self.obtained_chart_rate_Hz = np.nan

                self.chart_rate_accumulator = 0

        # Update curves
        if not self.paused:
            self.qlbl_chart_rate.setText("%.1f" % self.obtained_chart_rate_Hz)
            self.update_num_points_drawn()
            self.update_curves()

    @Slot()
    def update_GUI(self):
        self.qlbl_DAQ_rate.setText("%.1f" % Sensor_QDevice.obtained_DAQ_rate_Hz)


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


@Slot()
#def about_to_quit():
    #Sensor_QDevice.quit()
    #timer_chart.stop()


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

class Sensor_Read:
    """Simulates a data acquisition (DAQ) device that will generate data at a
    fixed sample rate. It will push the data into the passed `ThreadSaveCurve`
    instances.
    """
    def __init__(
        self,
        FX_Curve_: ThreadSafeCurve,
        FY_Curve_: ThreadSafeCurve,
        FZ_Curve_: ThreadSafeCurve,
        FZ_Curve_Filtered_: ThreadSafeCurve,
        TX_Curve_: ThreadSafeCurve,
        TY_Curve_: ThreadSafeCurve,
        TZ_Curve_: ThreadSafeCurve,
        
        FX_Curve_1st_Derivative_: ThreadSafeCurve,
        FY_Curve_1st_Derivative_: ThreadSafeCurve,
        FZ_Curve_1st_Derivative_: ThreadSafeCurve,
        TX_Curve_1st_Derivative_: ThreadSafeCurve,
        TY_Curve_1st_Derivative_: ThreadSafeCurve,
        TZ_Curve_1st_Derivative_: ThreadSafeCurve,
        
        XY_Curve_: ThreadSafeCurve,
        XY_Curve_1st_Derivative_: ThreadSafeCurve,
    ):
        self.name = "Sensor_Read"
        self.is_alive = True
        
        self.FX_Curve = FX_Curve_
        self.FY_Curve = FY_Curve_
        self.FZ_Curve = FZ_Curve_
        self.FZ_Curve_Filtered = FZ_Curve_Filtered_
        self.TX_Curve = TX_Curve_
        self.TY_Curve = TY_Curve_
        self.TZ_Curve = TZ_Curve_
        
        self.FX_Curve_1st_Derivative = FX_Curve_1st_Derivative_
        self.FY_Curve_1st_Derivative = FY_Curve_1st_Derivative_
        self.FZ_Curve_1st_Derivative = FZ_Curve_1st_Derivative_
        self.TX_Curve_1st_Derivative = TX_Curve_1st_Derivative_
        self.TY_Curve_1st_Derivative = TY_Curve_1st_Derivative_
        self.TZ_Curve_1st_Derivative = TZ_Curve_1st_Derivative_
        self.XY_Curve_1st_Derivative = XY_Curve_1st_Derivative_
        
        self.XY_Curve = XY_Curve_
        
        self.Sensor_All_Curves = [
            self.FX_Curve,
            self.FY_Curve,
            self.FZ_Curve,
            self.FZ_Curve_Filtered,
            self.TX_Curve,
            self.TY_Curve,
            self.TZ_Curve,
            
            self.FX_Curve_1st_Derivative,
            self.FY_Curve_1st_Derivative,
            self.FZ_Curve_1st_Derivative,
            self.TX_Curve_1st_Derivative,
            self.TY_Curve_1st_Derivative,
            self.TZ_Curve_1st_Derivative,
            
            self.XY_Curve,
            self.XY_Curve_1st_Derivative
            ]

    def generate_data(self):
        
        if self.FX_Curve.size[0] == 0:
            x_0 = 0
        else:
            # Pick up the previously last phase of the sine
            # fmt: off
            x_0 = self.FX_Curve._buffer_x[-1]  # pylint: disable=protected-access
            # fmt: on
        
        x = (1 + np.arange(WORKER_DAQ_INTERVAL_MS * Fs / 1e3)) / Fs + x_0
        
        request = b'\x12\x34\x00\x02\x00\x00\x00\x01'

        sock.sendto(request,(sockaddr_in,Port))
        data, addr = sock.recvfrom(36)
        FTData[:,:,:] = np.roll(FTData, 1, axis = 1)
        FTData_Filtered = np.array(np.single(np.zeros((6,1,2))))
        for i in range(0,6,1):
            FTData[i,0,0] = int.from_bytes(data[12 + i * 4 : 15 + i * 4],'big',signed=True) / cpft * 256
            FTData[i,0,1] = (FTData[i,0,0]-FTData[i,1,0]) / (WORKER_DAQ_INTERVAL_MS * 1000) #first derivative
        
        for j in range(2):
            for i in range(6):
                FTData_Filtered[i,0,j]=FTData[i,0,j]

        global FTData_Entries
        FTData_Entries = FTData_Entries + 1
        
        if FTData_Entries >= 10:
            
            kf = KalmanFilter(
                transition_matrices=[1.],
                observation_matrices=np.reshape(FTData[2,:,0],(10,1,1)).tolist(),
                transition_covariance=[2.],
                observation_covariance=[2.],
                initial_state_mean=[0.],
                initial_state_covariance=[2.],
                em_vars=['transition_covariance', 'observation_covariance', 'initial_state_mean', 'initial_state_covariance']
            )
            
            #kf = kf.em(FTData['y'].values.astype(float))
            kf = kf.em(FTData[1,:,0].tolist(),n_iter = 10,em_vars='all')
            
            # filtered_state_estimates = kf.filter(FTData['y'].values.astype(float))[0]
            # smoothed_state_estimates = kf.smooth(FTData['y'].values.astype(float))[0]
            
            filtered_state_estimates = kf.filter(FTData[1,:,0].tolist())[0]
            smoothed_state_estimates = kf.smooth(FTData[1,:,0].tolist())[0]
            #breakpoint()
            self.FZ_Curve_Filtered.extendData(x,smoothed_state_estimates[9].tolist())
            

        self.FX_Curve.extendData(x,[FTData_Filtered[0,0,0].tolist()])
        self.FY_Curve.extendData(x,[FTData_Filtered[1,0,0].tolist()])
        self.FZ_Curve.extendData(x,[FTData_Filtered[2,0,0].tolist()])
        self.TX_Curve.extendData(x,[FTData_Filtered[3,0,0].tolist()])
        self.TY_Curve.extendData(x,[FTData_Filtered[4,0,0].tolist()])
        self.TZ_Curve.extendData(x,[FTData_Filtered[5,0,0].tolist()])
        
        self.FX_Curve_1st_Derivative.extendData(x,[FTData_Filtered[0,0,1].tolist()])
        self.FY_Curve_1st_Derivative.extendData(x,[FTData_Filtered[1,0,1].tolist()])
        self.FZ_Curve_1st_Derivative.extendData(x,[FTData_Filtered[2,0,1].tolist()])
        self.TX_Curve_1st_Derivative.extendData(x,[FTData_Filtered[3,0,1].tolist()])
        self.TY_Curve_1st_Derivative.extendData(x,[FTData_Filtered[4,0,1].tolist()])
        self.TZ_Curve_1st_Derivative.extendData(x,[FTData_Filtered[5,0,1].tolist()])
        
        self.XY_Curve.extendData([FTData_Filtered[3,0,0].tolist()], [FTData_Filtered[4,0,0].tolist()])
        self.XY_Curve_1st_Derivative.extendData([FTData_Filtered[3,0,1].tolist()], [FTData_Filtered[4,0,1].tolist()])
        # for i in range(0,np.size(self.Sensor_All_Curves)):
        #     if i < 6: #0th derivative
        #         self.Sensor_All_Curves[i].extendData(x,[FTData_Filtered[i,0,0].tolist()])
        #     elif i >= 6 and i < 12: #1st derivative
        #         self.Sensor_All_Curves[i].extendData(x,[FTData_Filtered[i-6,0,1].tolist()])
        #     elif i == 12: #positional
        #         self.XY_Curve.extendData([FTData_Filtered[3,0,0].tolist()], [FTData_Filtered[4,0,0].tolist()])
        #     elif i == 13: #1st derivative positional
        #         self.XY_Curve_1st_Derivative.extendData([FTData_Filtered[3,0,1].tolist()], [FTData_Filtered[4,0,1].tolist()])
        
        return True


# ------------------------------------------------------------------------------
#   Main
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QtWid.QApplication(sys.argv)
    #app.aboutToQuit.connect(about_to_quit)

    window = MainWindow()

    # Sensor_Read:
    #   Simulates a data acquisition (DAQ) device that will generate data at a
    #   fixed sample rate. It will push the data into the passed
    #   `ThreadSaveCurve` instances.
    # QDeviceIO:
    #   Creates and manages a new thread for `Sensor_Device`. A worker will
    #   perdiocally activate `Sensor_Device` from out of this new thread.
    Sensor_Device = Sensor_Read(window.FX_Curve, 
                          window.FY_Curve, 
                          window.FZ_Curve,
                          window.FZ_Curve_Filtered,
                          window.TX_Curve,
                          window.TY_Curve,
                          window.TZ_Curve,
                          window.FX_Curve_1st_Derivative,
                          window.FY_Curve_1st_Derivative,
                          window.FZ_Curve_1st_Derivative,
                          window.TX_Curve_1st_Derivative,
                          window.TY_Curve_1st_Derivative,
                          window.TZ_Curve_1st_Derivative,
                          window.XY_Curve,
                          window.XY_Curve_1st_Derivative)
    Sensor_QDevice = QDeviceIO(Sensor_Device)
    Sensor_QDevice.create_worker_DAQ(
        DAQ_interval_ms=WORKER_DAQ_INTERVAL_MS,
        DAQ_function=Sensor_Device.generate_data,
    )
    Sensor_QDevice.signal_DAQ_updated.connect(window.update_GUI)
    Sensor_QDevice.start()

    # Chart refresh timer
    timer_chart = QtCore.QTimer(timerType=QtCore.Qt.TimerType.PreciseTimer)
    timer_chart.timeout.connect(window.update_charts)
    timer_chart.start(CHART_DRAW_INTERVAL_MS)

    window.show()
    if QT_LIB in (PYQT5, PYSIDE2):
        sys.exit(app.exec_())
    else:
        sys.exit(app.exec())