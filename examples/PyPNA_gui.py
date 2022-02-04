###########################################################
#     GUI for displaying real time s-par measurements     #
#           Harry Lees & Bryce Chung - Dec 2021           #
#       Install PyPNA: python3 -m pip install pypn        #
###########################################################

import sys
import time
import os

import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtCharts as qtch
import numpy as np
import PyPNA

def dark_pal():
    # creats the dark mode color palette for the gui

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
        #setup pna
        ## pna setup
        self.pm = PyPNA.PyPNA()

        self.pm.connect()

        ######### change this to config file used on pna #########
        config_path='D:/pypna.csa'
        self.pm.load_setup(config_path)

        # sets default averaging factor to 1, by default averaging is off
        factor = 1
        self.pm.pna.write(f"SENS:AVER:COUN {factor}")

        # initialises s11 and s21 measurements
        self.pm.add_sparam(1)
        self.pm.add_sparam(2)

        # print device id on startup to check connection is actually to pna
        self.pm.print_id()

        # setup window for gui
        super(Form,self).__init__(parent)
        self.setWindowTitle("")
        self.setWindowFlags(qtc.Qt.WindowMinMaxButtonsHint | qtc.Qt.WindowCloseButtonHint)
        rat=1920/1080
        hw=900
        self.resize(hw*rat,hw)

        #### default settings ####
        self.avg=0
        self.padding=0
        self.s11=1
        self.s21=1
        self.x_stream_fd=np.linspace(220,330,1001)
        self.x_stream_td=np.linspace(0,1001,1001)
        self.meas_fps=0

        #### interface - adding in all the buttons and inputs ####
        self.add_bt= qtw.QPushButton("Add Comparison (.npy or .txt)")
        self.norm_bt= qtw.QPushButton("Add Normalisation")
        self.norm_enable_check=qtw.QCheckBox()
        self.clear_bt= qtw.QPushButton("Clear Comparisons")
        self.save_bt= qtw.QPushButton("Save Raw Data")
        self.avg_bt= qtw.QPushButton("Toggle Avg")
        self.ylim_min_in_fd=qtw.QLineEdit("-50")
        self.ylim_max_in_fd=qtw.QLineEdit("0")
        self.ylim_min_in_td=qtw.QLineEdit("0")
        self.ylim_max_in_td=qtw.QLineEdit("0.2")
        self.xlim_min_in_fd=qtw.QLineEdit("220")
        self.xlim_max_in_fd=qtw.QLineEdit("330")
        self.xlim_min_in_td=qtw.QLineEdit("0")
        self.xlim_max_in_td=qtw.QLineEdit("200")
        self.avg_factor=qtw.QLineEdit("40")
        self.pad_bt=qtw.QPushButton("TD Padding")
        self.pad_factor=qtw.QLineEdit("0")

        self.s11_bt=qtw.QPushButton("S11")
        self.s21_bt=qtw.QPushButton("S21")
        self.s11_bt.setStyleSheet('background-color: green;')
        self.s21_bt.setStyleSheet('background-color: green;')

        self.bt_size=30
        self.ylim_min_in_fd.setMaximumWidth(self.bt_size)
        self.ylim_max_in_fd.setMaximumWidth(self.bt_size)
        self.ylim_min_in_td.setMaximumWidth(self.bt_size)
        self.ylim_max_in_td.setMaximumWidth(self.bt_size)
        self.xlim_min_in_fd.setMaximumWidth(self.bt_size)
        self.xlim_max_in_fd.setMaximumWidth(self.bt_size)
        self.xlim_min_in_td.setMaximumWidth(self.bt_size)
        self.xlim_max_in_td.setMaximumWidth(self.bt_size)
        self.avg_factor.setMaximumWidth(self.bt_size)
        self.pad_factor.setMaximumWidth(self.bt_size)
        self.s21_bt.setMaximumWidth(self.bt_size*1.5)
        self.s11_bt.setMaximumWidth(self.bt_size*1.5)


        # initialise frequency domain chart
        self.graph_fd = qtch.QChart()
        self.graph_fd.setTitle("Frequency Domain")
        self.chart_view_fd=qtch.QChartView(self.graph_fd)
        self.chart_view_fd.setRenderHint(qtg.QPainter.Antialiasing)
        self.chart_view_fd.chart().setTheme(qtch.QChart.ChartThemeDark)

        # initialise time domain chart
        self.graph_td = qtch.QChart()
        self.graph_td.setTitle("Time Domain")
        self.chart_view_td=qtch.QChartView(self.graph_td)
        self.chart_view_td.setRenderHint(qtg.QPainter.Antialiasing)
        self.chart_view_td.chart().setTheme(qtch.QChart.ChartThemeDark)
        
        # initialise update properties - time unit is ms - default fps is 5 for s11/s21 simulatenously
        self.timer=qtc.QTimer()
        self.fps=5
        self.timer.setInterval(1000/self.fps)
        self.timer.start()
        self.t0=time.time()

        #### layout GUI ####
        layout=qtw.QGridLayout(self)
        
        #charts
        layout.addWidget(self.chart_view_fd,0,3,20,8)
        layout.addWidget(self.chart_view_td,0,11,20,8)

        #data selection
        sel_start=1
        layout.addWidget(qtw.QLabel("<b>Data Selection</b>"),sel_start,0,1,3,qtc.Qt.AlignCenter)
        layout.addWidget(self.s11_bt,sel_start+1,0,1,1)
        layout.addWidget(self.s21_bt,sel_start+1,2,1,1)

        # fd buttons
        fd_start=3
        layout.addWidget(qtw.QLabel("<b>FD Plot Setting</b>"),fd_start,0,1,3,qtc.Qt.AlignCenter)
        layout.addWidget(qtw.QLabel("FD x-Lim"),fd_start+1,0)
        layout.addWidget(self.xlim_min_in_fd,fd_start+1,1)
        layout.addWidget(self.xlim_max_in_fd,fd_start+1,2)
        layout.addWidget(qtw.QLabel("FD y-Lim"),fd_start+2,0)
        layout.addWidget(self.ylim_min_in_fd,fd_start+2,1)
        layout.addWidget(self.ylim_max_in_fd,fd_start+2,2)
        layout.addWidget(self.add_bt,fd_start+3,0,1,3)
        layout.addWidget(self.clear_bt,fd_start+4,0,1,3)
        layout.addWidget(self.norm_bt,fd_start+5,0,1,2)
        layout.addWidget(self.norm_enable_check,fd_start+5,2)
        layout.addWidget(self.save_bt,fd_start+6,0,1,3)
        layout.addWidget(self.avg_bt,fd_start+7,0,1,2)
        layout.addWidget(self.avg_factor,fd_start+7,2)
        
        # td buttons
        td_start=(fd_start+7)+1
        layout.addWidget(qtw.QLabel("<b>TD Plot Setting</b>"),td_start,0,1,3,qtc.Qt.AlignCenter)
        layout.addWidget(qtw.QLabel("TD x-Lim"),td_start+1,0)
        layout.addWidget(self.xlim_min_in_td,td_start+1,1)
        layout.addWidget(self.xlim_max_in_td,td_start+1,2)
        layout.addWidget(qtw.QLabel("TD y-Lim"),td_start+2,0)
        layout.addWidget(self.ylim_min_in_td,td_start+2,1)
        layout.addWidget(self.ylim_max_in_td,td_start+2,2)
        layout.addWidget(self.pad_bt,td_start+3,0,1,2)
        layout.addWidget(self.pad_factor,td_start+3,2)
        
        self.fps_display=qtw.QLabel()
        layout.addWidget(self.fps_display,td_start+5,0,2,3,qtc.Qt.AlignCenter)

        layout.addWidget(qtw.QLabel("PyPNA by Harry Lees & Bryce Chung, December 2021 @ Terahertz Engineering Laboratory, University of Adelaide"),21,0,1,20,alignment=qtc.Qt.AlignCenter)

        self.setLayout(layout)

        #### slots and signals - each button needs to be connected to a function which activates on button press ####
        self.add_bt.clicked.connect(self.add_from_file)
        self.clear_bt.clicked.connect(self.clear)
        self.ylim_min_in_fd.textChanged.connect(self.change_lim)
        self.ylim_max_in_fd.textChanged.connect(self.change_lim)
        self.xlim_min_in_fd.textChanged.connect(self.change_lim)
        self.xlim_max_in_fd.textChanged.connect(self.change_lim)
        self.ylim_min_in_td.textChanged.connect(self.change_lim)
        self.ylim_max_in_td.textChanged.connect(self.change_lim)
        self.xlim_min_in_td.textChanged.connect(self.change_lim)
        self.xlim_max_in_td.textChanged.connect(self.change_lim)
        self.avg_factor.textChanged.connect(self.sense_avg_fac)
        self.pad_factor.textChanged.connect(self.sense_pad_fac)
        self.timer.timeout.connect(self.periodic_refresh)
        self.avg_bt.clicked.connect(self.avg_toggle)
        self.pad_bt.clicked.connect(self.pad_toggle)
        self.save_bt.clicked.connect(self.save_data)
        self.norm_bt.clicked.connect(self.add_norm)
        self.norm_enable_check.stateChanged.connect(self.norm_toggle)
        self.s11_bt.clicked.connect(self.s11_tog)
        self.s21_bt.clicked.connect(self.s21_tog)

        ### Configure Frequency Domain Plot Options ###
        self.axis_x = qtch.QValueAxis()
        self.axis_x.setTickCount(10)
        self.axis_x.setTitleText("Frequency (GHz)")
        self.axis_x.setMin(220)
        self.axis_x.setMax(330)
        self.graph_fd.addAxis(self.axis_x, qtc.Qt.AlignBottom)

        self.axis_y = qtch.QValueAxis()
        self.axis_y.setTickCount(10)
        self.axis_y.setTitleText("Magnitude (dB)")
        self.axis_y.setMin(-50)
        self.axis_y.setMax(0)
        self.graph_fd.addAxis(self.axis_y, qtc.Qt.AlignLeft)

        self.series=qtch.QLineSeries()
        self.data_stream_series_a=qtch.QLineSeries()
        self.data_stream_series_a.setName("S11")
        self.data_stream_series_a.setUseOpenGL(True)

        self.data_stream_series_b=qtch.QLineSeries()
        self.data_stream_series_b.setName("S21")
        self.data_stream_series_b.setUseOpenGL(True)
        
        self.series_list=[self.series]

        self.graph_fd.addSeries(self.data_stream_series_a)
        self.data_stream_series_a.attachAxis(self.axis_x)
        self.data_stream_series_a.attachAxis(self.axis_y)
        self.graph_fd.addSeries(self.data_stream_series_b)
        self.data_stream_series_b.attachAxis(self.axis_x)
        self.data_stream_series_b.attachAxis(self.axis_y)

        ### A few variables need to be initialised for normalisation
        self.norm_tog=0
        self.s11_ref=np.zeros(1001,dtype="complex")
        self.s21_ref=np.zeros(1001,dtype="complex")

        ### Configure Frequency Domain Plot Options ###
        self.axis_x_td = qtch.QValueAxis()
        self.axis_x_td.setTickCount(10)
        self.axis_x_td.setTitleText("Time Sample")
        self.axis_x_td.setMin(0)
        self.axis_x_td.setMax(200)
        self.graph_td.addAxis(self.axis_x_td, qtc.Qt.AlignBottom)

        self.axis_y_td = qtch.QValueAxis()
        self.axis_y_td.setTickCount(10)
        self.axis_y_td.setTitleText("Magnitude (a.u)")
        self.axis_y_td.setMin(0)
        self.axis_y_td.setMax(0.2)
        self.graph_td.addAxis(self.axis_y_td, qtc.Qt.AlignLeft)

        self.data_stream_series_c=qtch.QLineSeries()
        self.data_stream_series_c.setName("S11")
        self.data_stream_series_c.setUseOpenGL(True)

        self.data_stream_series_d=qtch.QLineSeries()
        self.data_stream_series_d.setName("S21")
        self.data_stream_series_d.setUseOpenGL(True)

        self.graph_td.addSeries(self.data_stream_series_c)
        self.data_stream_series_c.attachAxis(self.axis_x_td)
        self.data_stream_series_c.attachAxis(self.axis_y_td)
        self.graph_td.addSeries(self.data_stream_series_d)
        self.data_stream_series_d.attachAxis(self.axis_x_td)
        self.data_stream_series_c.attachAxis(self.axis_y_td)

    def add_from_file(self):
        # this function adds s-parameters to the chart
        # inputs: none
        # returns: none


        #opens a query window for a path
        self.plot_path,_=qtw.QFileDialog.getOpenFileName(self, "Select File")
        
        # check path is entered
        if self.plot_path != '':

            # I save data commonly as npy so that is supported
            if self.plot_path.endswith(".npy"):
                #numpy case
                data=np.load(self.plot_path)
                self.xdata_=np.abs(data[:,0])
                self.ydata_=20*np.log10(np.abs(data[:,1]))
                self.series=qtch.QLineSeries()
                self.series_list.append(self.series)
                self.series.setName(self.plot_path)
                print(f"Updated plot path: {self.plot_path}")
                for i,xi in enumerate(self.xdata_):
                    self.series.append(xi,self.ydata_[i])

                self.graph_fd.addSeries(self.series)
                # Setting X-axis 
                self.series.attachAxis(self.axis_x)
                # Setting Y-axis
                self.series.attachAxis(self.axis_y)

                self.ydata_=np.fft.ifft((data[:,1]))
                self.series=qtch.QLineSeries()
                self.series_list.append(self.series)
                self.series.setName(self.plot_path)
                print(f"Updated plot path: {self.plot_path}")
                for i,xi in enumerate(self.x_stream_td):
                    self.series.append(xi,self.ydata_[i])

                self.graph_td.addSeries(self.series)
                # Setting X-axis 
                self.series.attachAxis(self.axis_x)
                # Setting Y-axis
                self.series.attachAxis(self.axis_y)

            if self.plot_path.endswith(".txt"):
                # this handles the loading of .txt data (data saved by this gui is .txt data)

                data=np.loadtxt(self.plot_path,skiprows=1)
                self.xdata_=np.abs(data[:,0])
                self.ydata_=20*np.log10(np.abs(data[:,1]+1j*data[:,2]))
                self.series=qtch.QLineSeries()
                self.series_list.append(self.series)
                self.series.setName(os.path.basename(self.plot_path)+" Set 1")
                print(f"Updated plot path: {self.plot_path}")
                for i,xi in enumerate(self.xdata_):
                    self.series.append(xi,self.ydata_[i])

                self.graph_fd.addSeries(self.series)
                # Setting X-axis 
                self.series.attachAxis(self.axis_x)
                # Setting Y-axis
                self.series.attachAxis(self.axis_y)
                if data.shape[1]>3:
                    self.ydata_=20*np.log10(np.abs(data[:,3]+1j*data[:,4]))
                    self.series=qtch.QLineSeries()
                    self.series_list.append(self.series)
                    self.series.setName(os.path.basename(self.plot_path)+" Set 2")
                    print(f"Updated plot path: {self.plot_path}")
                    for i,xi in enumerate(self.xdata_):
                        self.series.append(xi,self.ydata_[i])

                    self.graph_fd.addSeries(self.series)
                    # Setting X-axis 
                    self.series.attachAxis(self.axis_x)
                    # Setting Y-axis
                    self.series.attachAxis(self.axis_y)
                    pass

                ###TD PLOTS###
                self.ydata_=np.abs(np.fft.ifft(data[:,1]+1j*data[:,2]))
                self.series=qtch.QLineSeries()
                self.series_list.append(self.series)
                self.series.setName(os.path.basename(self.plot_path)+" Set 1")
                print(f"Updated plot path: {self.plot_path}")
                for i,xi in enumerate(self.x_stream_td):
                    self.series.append(xi,self.ydata_[i])

                self.graph_td.addSeries(self.series)
                # Setting X-axis 
                self.series.attachAxis(self.axis_x_td)
                # Setting Y-axis
                self.series.attachAxis(self.axis_y_td)
                if data.shape[1]>3:
                    self.ydata_=np.abs(np.fft.ifft(data[:,3]+1j*data[:,4]))
                    self.series=qtch.QLineSeries()
                    self.series_list.append(self.series)
                    self.series.setName(os.path.basename(self.plot_path)+" Set 2")
                    print(f"Updated plot path: {self.plot_path}")
                    for i,xi in enumerate(self.x_stream_td):
                        self.series.append(xi,self.ydata_[i])

                    self.graph_td.addSeries(self.series)
                    # Setting X-axis 
                    self.series.attachAxis(self.axis_x_td)
                    # Setting Y-axis
                    self.series.attachAxis(self.axis_y_td)
                    pass
             
    def clear(self):
        # removes all plots from the gui leaving an empty chart, 
        # until next refresh when data is loaded from pna

        for si in self.series_list:
            self.graph_fd.removeSeries(si)
            self.graph_td.removeSeries(si)
            si.clear()
        pass

    def change_lim(self):
        #updates the graph limits

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
        # this 'updates' the plot when the timer runs out
        # re-queries pna for data, updates a few other things

        self.t0=time.time()

        #s11
        if self.s11==1:
            s11=self.pm.get_sparam(1)
            if self.norm_tog==1:
                y_stream_a=20*np.log10(np.abs(s11))-20*np.log10(np.abs(self.s11_ref))
            else:
                y_stream_a=20*np.log10(np.abs(s11))
            y_stream_c=(np.abs(np.fft.ifft(s11)))

        #s21
        if self.s21==1:
            s21=self.pm.get_sparam(2)
            if self.norm_tog==1:
                y_stream_b=20*np.log10(np.abs(s21))-20*np.log10(np.abs(self.s21_ref))
            else:
                y_stream_b=20*np.log10(np.abs(s21))
            y_stream_d=(np.abs(np.fft.ifft(s21)))
        
        #plot everything
        self.data_stream_series_a.clear()
        self.data_stream_series_b.clear()
        self.data_stream_series_c.clear()
        self.data_stream_series_d.clear()
        #fd
        for i,xi in enumerate(self.x_stream_fd):
            if self.s11==1:
                self.data_stream_series_a.append(xi,y_stream_a[i])
                self.data_stream_series_c.append(self.x_stream_td[i],y_stream_c[i])
            if self.s21==1:
                self.data_stream_series_b.append(xi,y_stream_b[i])
                self.data_stream_series_d.append(self.x_stream_td[i],y_stream_d[i])

        self.meas_fps=(self.meas_fps+(1/(time.time()-self.t0)))/2
        self.fps_display.setText(f"Figure Refresh Rate: {np.around(self.fps)} fps \nMeasurement Refresh Rate: {np.around(self.meas_fps)} fps")

        pass

    def avg_toggle(self):
        # turns averaging on and off - writes command to pna

        if self.avg==0:
            self.avg=1
            if self.avg_factor.text().isnumeric:
                self.pm.pna.write(f"SENS:AVER:COUN {self.avg_factor.text()}")
            self.pm.pna.write("SENS:AVER ON")
            self.avg_bt.setStyleSheet('background-color: green;')
        else:
            self.avg=0
            self.pm.pna.write("SENS:AVER OFF")
            self.avg_bt.setStyleSheet('background-color: 0x82B39;')

    def norm_toggle(self):
        # implememnt basic binary toggling functionality

        if self.norm_tog==1:
            self.norm_tog=0
        elif self.norm_tog==0:
            self.norm_tog=1

    def add_norm(self):
        # adds a normalisation measurment - this measurement is subtracted from data queried from pna

        self.norm_path,_=qtw.QFileDialog.getOpenFileName(self, "Select File")
        if self.norm_path != '':
            data=np.loadtxt(self.norm_path,skiprows=1)
            self.s11_ref=data[:,1]+1j*data[:,2]
            self.s21_ref=data[:,3]+1j*data[:,4]
            
    def sense_avg_fac(self):
        # writes new averaging factor to pna

        if self.avg_factor.text().isnumeric():
            self.pm.pna.write(f"SENS:AVER:COUN {self.avg_factor.text()}")
    
    def save_data(self):
        # saves pna data to text file

        s11=self.pm.get_sparam(1)
        s21=self.pm.get_sparam(2)
        f=np.linspace(220,330,1001)
        s11_re=np.real(s11)
        s11_im=np.imag(s11)
        s21_re=np.real(s21)
        s21_im=np.imag(s21)

        data_out=np.column_stack((f,s11_re,s11_im,s21_re,s21_im))

        save_path,_=qtw.QFileDialog.getSaveFileName(self, "Save As")
        head="Frequency (GHz) | real(S11) | imag(S11) | real(S21) | imag(S21)"
        if not save_path.endswith(".txt"):
            np.savetxt(save_path+".txt",data_out,header=head)
        else:
            np.savetxt(save_path,data_out,header=head)

    def pad_toggle(self):
        # turns frequency domain padding on and off

        if self.padding==0:
            self.padding=1
            self.pad_bt.setStyleSheet('background-color: green;')
        else:
            self.padding=0
            self.pad_bt.setStyleSheet('background-color: 0x82B39;')

    def sense_pad_fac(self):
        # when padding factor is updated change values

        if self.pad_factor.text().isnumeric():
            self.padding=float(self.pad_factor.text())

    def s11_tog(self):
        # turns s11 display on/off - updates fps to reflect this

        if self.s11==0:
            self.s11=1
            self.s11_bt.setStyleSheet('background-color: green;')
        else:
            self.s11=0
            self.s11_bt.setStyleSheet('background-color: 0x82B39;')
        
        #adjust refresh rate
        if self.s11+self.s21==2:
            self.fps=5
        else:
            self.fps=30
        self.timer.setInterval(1000/self.fps)

    def s21_tog(self):
        # turns s21 display on/off - updates fps to reflect this

        if self.s21==0:
            self.s21=1
            self.s21_bt.setStyleSheet('background-color: green;')
        else:
            self.s21=0
            self.s21_bt.setStyleSheet('background-color: 0x82B39;')

        #adjust refresh rate
        if self.s11+self.s21==2:
            self.fps=5
        else:
            self.fps=30
        self.timer.setInterval(1000/self.fps)

if __name__ == "__main__":

    ## application
    app = qtw.QApplication(sys.argv)

    style=1
    if style==1:
        app.setStyle('Fusion')

        dark_palette = dark_pal()

        app.setPalette(dark_palette)
        app.setApplicationDisplayName("PyPNA")

        icon=qtg.QIcon()
        icon.addFile(r"examples\icon.png")
        app.setWindowIcon(icon)

    form=Form()
    form.show()

    app.exec()
