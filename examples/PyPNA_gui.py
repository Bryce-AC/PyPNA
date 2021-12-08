
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtCharts as qtch
import numpy as np

import sys
import random
import time

def dark_pal():
    dark_palette = qtg.QPalette()

    dark_palette.setColor(qtg.QPalette.Window, qtg.QColor(53, 53, 53))
    dark_palette.setColor(qtg.QPalette.WindowText, qtc.Qt.white)
    dark_palette.setColor(qtg.QPalette.Base, qtg.QColor(25, 25, 25))
    dark_palette.setColor(qtg.QPalette.AlternateBase, qtg.QColor(53, 53, 53))
    dark_palette.setColor(qtg.QPalette.ToolTipBase, qtc.Qt.white)
    dark_palette.setColor(qtg.QPalette.ToolTipText, qtc.Qt.white)
    dark_palette.setColor(qtg.QPalette.Text, qtc.Qt.white)
    dark_palette.setColor(qtg.QPalette.Button, qtg.QColor(53, 53, 53))
    dark_palette.setColor(qtg.QPalette.ButtonText, qtc.Qt.white)
    dark_palette.setColor(qtg.QPalette.BrightText, qtc.Qt.red)
    dark_palette.setColor(qtg.QPalette.Link, qtg.QColor(42, 130, 218))
    dark_palette.setColor(qtg.QPalette.Highlight, qtg.QColor(42, 130, 218))
    dark_palette.setColor(qtg.QPalette.HighlightedText, qtc.Qt.black)

    return dark_palette

class Form(qtw.QDialog):

    def __init__(self,parent=None):
        super(Form,self).__init__(parent)
        self.setWindowTitle("")
        self.resize(1280,720)

        #interface
        self.add_bt= qtw.QPushButton("Add Sim (.npy)")
        self.norm_bt= qtw.QPushButton("Add Normalisation")
        self.norm_enable_check=qtw.QCheckBox()
        self.clear_bt= qtw.QPushButton("Clear Sim Traces")
        self.save_bt= qtw.QPushButton("Save Raw Data")
        self.ylim_min_in_fd=qtw.QLineEdit("-50")
        self.ylim_max_in_fd=qtw.QLineEdit("0")
        self.ylim_min_in_td=qtw.QLineEdit("-50")
        self.ylim_max_in_td=qtw.QLineEdit("0")
        self.xlim_min_in_fd=qtw.QLineEdit("220")
        self.xlim_max_in_fd=qtw.QLineEdit("330")
        self.xlim_min_in_td=qtw.QLineEdit("220")
        self.xlim_max_in_td=qtw.QLineEdit("330")

        self.bt_size=30
        self.ylim_min_in_fd.setMaximumWidth(self.bt_size)
        self.ylim_max_in_fd.setMaximumWidth(self.bt_size)
        self.ylim_min_in_td.setMaximumWidth(self.bt_size)
        self.ylim_max_in_td.setMaximumWidth(self.bt_size)
        self.xlim_min_in_fd.setMaximumWidth(self.bt_size)
        self.xlim_max_in_fd.setMaximumWidth(self.bt_size)
        self.xlim_min_in_td.setMaximumWidth(self.bt_size)
        self.xlim_max_in_td.setMaximumWidth(self.bt_size)

        self.graph_fd = qtch.QChart()
        self.graph_fd.setTitle("Frequency Domain")
        self.graph_fd.setAnimationOptions(qtch.QChart.AllAnimations)
        self.chart_view_fd=qtch.QChartView(self.graph_fd)
        self.chart_view_fd.setRenderHint(qtg.QPainter.Antialiasing)
        self.chart_view_fd.chart().setTheme(qtch.QChart.ChartThemeDark)

        self.graph_td = qtch.QChart()
        self.graph_td.setTitle("Time Domain")
        self.graph_td.setAnimationOptions(qtch.QChart.AllAnimations)
        self.chart_view_td=qtch.QChartView(self.graph_td)
        self.chart_view_td.setRenderHint(qtg.QPainter.Antialiasing)
        self.chart_view_td.chart().setTheme(qtch.QChart.ChartThemeDark)
        
        #timer
        self.timer=qtc.QTimer()
        self.timer.setInterval(200)
        self.timer.start()

        #old
        #layout= qtw.QVBoxLayout(self)
        #layout.addWidget(self.add_bt)
        #layout.addWidget(self.chart_view_fd)
        #layout.addWidget(self.chart_view_td)
        #layout.addWidget(self.clear_bt)
        #layout.addWidget(self.ylim_min_in_fd)
        #layout.addWidget(self.ylim_max_in_fd)

        #new
        layout=qtw.QGridLayout(self)
        
        #charts
        layout.addWidget(self.chart_view_fd,0,3,8,8)
        layout.addWidget(self.chart_view_td,0,11,8,8)

        #fd buttons
        layout.addWidget(qtw.QLabel("FD x-Lim"),0,0)
        layout.addWidget(self.xlim_min_in_fd,0,1)
        layout.addWidget(self.xlim_max_in_fd,0,2)
        layout.addWidget(qtw.QLabel("FD y-Lim"),1,0)
        layout.addWidget(self.ylim_min_in_fd,1,1)
        layout.addWidget(self.ylim_max_in_fd,1,2)
        layout.addWidget(self.add_bt,2,0,1,3)
        layout.addWidget(self.clear_bt,3,0,1,3)
        layout.addWidget(self.norm_bt,4,0,1,2)
        layout.addWidget(self.norm_enable_check,4,2)
        layout.addWidget(self.save_bt,5,0,1,3)
        
        #td buttons
        layout.addWidget(qtw.QLabel("TD x-Lim"),0,22)
        layout.addWidget(self.xlim_min_in_td,0,20)
        layout.addWidget(self.xlim_max_in_td,0,21)
        layout.addWidget(qtw.QLabel("TD y-Lim"),1,22)
        layout.addWidget(self.ylim_min_in_td,1,20)
        layout.addWidget(self.ylim_max_in_td,1,21)
        
        self.setLayout(layout)

        #slots and signals
        self.add_bt.clicked.connect(self.confirm)
        self.clear_bt.clicked.connect(self.clear)
        self.ylim_min_in_fd.textChanged.connect(self.change_lim)
        self.ylim_max_in_fd.textChanged.connect(self.change_lim)
        self.xlim_min_in_fd.textChanged.connect(self.change_lim)
        self.xlim_max_in_fd.textChanged.connect(self.change_lim)
        self.ylim_min_in_td.textChanged.connect(self.change_lim)
        self.ylim_max_in_td.textChanged.connect(self.change_lim)
        self.xlim_min_in_td.textChanged.connect(self.change_lim)
        self.xlim_max_in_td.textChanged.connect(self.change_lim)
        self.timer.timeout.connect(self.periodic_refresh)

        #TO-DO
        #norm add norm
        #norm checkbox
        #save button
        
        ### Frequency Domain Plot
        self.axis_x = qtch.QValueAxis()
        self.axis_x.setTickCount(10)
        self.axis_x.setTitleText("Frequency (GHz)")
        self.axis_x.setMin(220)
        self.axis_x.setMax(330)
        self.graph_fd.addAxis(self.axis_x, qtc.Qt.AlignBottom)

        self.axis_y = qtch.QValueAxis()
        self.axis_y.setTickCount(10)
        self.axis_y.setTitleText("Magnitude")
        self.axis_y.setMin(-50)
        self.axis_y.setMax(0)
        self.graph_fd.addAxis(self.axis_y, qtc.Qt.AlignLeft)

        self.series=qtch.QLineSeries()
        self.data_stream_series_a=qtch.QLineSeries()
        self.data_stream_series_a.setName("S11")

        self.data_stream_series_b=qtch.QLineSeries()
        self.data_stream_series_b.setName("S21")

        
        self.series_list=[self.series]

        self.graph_fd.addSeries(self.data_stream_series_a)
        self.data_stream_series_a.attachAxis(self.axis_x)
        self.data_stream_series_a.attachAxis(self.axis_y)
        self.graph_fd.addSeries(self.data_stream_series_b)
        self.data_stream_series_b.attachAxis(self.axis_x)
        self.data_stream_series_b.attachAxis(self.axis_y)

        ### Time Domain Plot

        self.axis_x_td = qtch.QValueAxis()
        self.axis_x_td.setTickCount(10)
        self.axis_x_td.setTitleText("Frequency (GHz)")
        self.axis_x_td.setMin(220)
        self.axis_x_td.setMax(330)
        self.graph_td.addAxis(self.axis_x_td, qtc.Qt.AlignBottom)

        self.axis_y_td = qtch.QValueAxis()
        self.axis_y_td.setTickCount(10)
        self.axis_y_td.setTitleText("Magnitude")
        self.axis_y_td.setMin(-50)
        self.axis_y_td.setMax(0)
        self.graph_td.addAxis(self.axis_y_td, qtc.Qt.AlignLeft)

        self.data_stream_series_c=qtch.QLineSeries()
        self.data_stream_series_c.setName("S11")

        self.data_stream_series_d=qtch.QLineSeries()
        self.data_stream_series_d.setName("S21")

        self.graph_td.addSeries(self.data_stream_series_c)
        self.data_stream_series_c.attachAxis(self.axis_x_td)
        self.data_stream_series_c.attachAxis(self.axis_y_td)
        self.graph_td.addSeries(self.data_stream_series_d)
        self.data_stream_series_d.attachAxis(self.axis_x_td)
        self.data_stream_series_c.attachAxis(self.axis_y_td)

    def confirm(self):
        self.plot_path,_=qtw.QFileDialog.getOpenFileName(self, "Select File")
        #self.graph.setTitle(self.plot_path)
        if self.plot_path != '':
            self.series=qtch.QLineSeries()
            self.series_list.append(self.series)
            self.series.setName(self.plot_path)
            print(f"Updated plot path: {self.plot_path}")
            if self.plot_path.endswith(".npy"):
                data=np.load(self.plot_path)
                self.xdata_=np.abs(data[:,0])
                self.ydata_=20*np.log10(np.abs(data[:,1]))

            for i,xi in enumerate(self.xdata_):
                self.series.append(xi,self.ydata_[i])

            self.graph_fd.addSeries(self.series)
            # Setting X-axis 
            self.series.attachAxis(self.axis_x)
            # Setting Y-axis
            self.series.attachAxis(self.axis_y)
            
    def clear(self):
        for si in self.series_list:
            #self.graph.removeSeries(si)
            si.clear()
        pass

    def change_lim(self):
        print("Updated Limits")
        #graph 1
        if self.xlim_min_in_fd.text()!='-' and self.xlim_min_in_td.text()!='':
            self.axis_x.setMin(float(self.xlim_min_in_fd.text()))
        if self.xlim_max_in_fd.text()!='-' and self.xlim_max_in_td.text()!='':
            self.axis_x.setMax(float(self.xlim_max_in_fd.text()))
        if self.ylim_min_in_fd.text()!='-' and self.ylim_min_in_td.text()!='':
            self.axis_y.setMin(float(self.ylim_min_in_fd.text()))
        if self.ylim_max_in_fd.text()!='-' and self.ylim_max_in_td.text()!='':
            self.axis_y.setMax(float(self.ylim_max_in_fd.text()))

        #graph 2
        if self.xlim_min_in_td.text()!='-' and self.xlim_min_in_td.text()!='':
            self.axis_x_td.setMin(float(self.xlim_min_in_td.text()))
        if self.xlim_max_in_td.text()!='-' and self.xlim_max_in_td.text()!='':
            self.axis_x_td.setMax(float(self.xlim_max_in_td.text()))
        if self.ylim_min_in_td.text()!='-' and self.ylim_min_in_td.text()!='':
            self.axis_y_td.setMin(float(self.ylim_min_in_td.text()))
        if self.ylim_max_in_td.text()!='-' and self.ylim_max_in_td.text()!='':
            self.axis_y_td.setMax(float(self.ylim_max_in_td.text()))

    def periodic_refresh(self):
        x_stream=np.linspace(220,330,1001)
        y_stream_a=-50*np.random.rand(1001)
        y_stream_b=-50*np.random.rand(1001)
        y_stream_c=-50*np.random.rand(1001)
        y_stream_d=-50*np.random.rand(1001)
        self.data_stream_series_a.clear()
        self.data_stream_series_b.clear()
        self.data_stream_series_c.clear()
        self.data_stream_series_d.clear()
        for i,xi in enumerate(x_stream):
            self.data_stream_series_a.append(xi,y_stream_a[i])
            self.data_stream_series_b.append(xi,y_stream_b[i])
            self.data_stream_series_c.append(xi,y_stream_c[i])
            self.data_stream_series_d.append(xi,y_stream_d[i])

        pass

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    style=1
    if style==1:
        app.setStyle('Fusion')

        dark_palette = qtg.QPalette()

        dark_palette.setColor(qtg.QPalette.Window, qtg.QColor(53, 53, 53))
        dark_palette.setColor(qtg.QPalette.WindowText, qtc.Qt.white)
        dark_palette.setColor(qtg.QPalette.Base, qtg.QColor(25, 25, 25))
        dark_palette.setColor(qtg.QPalette.AlternateBase, qtg.QColor(53, 53, 53))
        dark_palette.setColor(qtg.QPalette.ToolTipBase, qtc.Qt.white)
        dark_palette.setColor(qtg.QPalette.ToolTipText, qtc.Qt.white)
        dark_palette.setColor(qtg.QPalette.Text, qtc.Qt.white)
        dark_palette.setColor(qtg.QPalette.Button, qtg.QColor(53, 53, 53))
        dark_palette.setColor(qtg.QPalette.ButtonText, qtc.Qt.white)
        dark_palette.setColor(qtg.QPalette.BrightText, qtc.Qt.red)
        dark_palette.setColor(qtg.QPalette.Link, qtg.QColor(42, 130, 218))
        dark_palette.setColor(qtg.QPalette.Highlight, qtg.QColor(42, 130, 218))
        dark_palette.setColor(qtg.QPalette.HighlightedText, qtc.Qt.black)

        app.setPalette(dark_palette)
        app.setApplicationDisplayName("PyPNA")

        icon=qtg.QIcon()
        icon.addFile(r"D:\Visual Studio Code Workspace\PyQT Gui\icon.png")
        app.setWindowIcon(icon)

    form=Form()
    form.show()

    app.exec()
