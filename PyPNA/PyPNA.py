import pyvisa
import numpy as np

class PyPNA:
    def __init__(self):
        # creates pyvisa object, this has a list of all the visa devices connected to computer
        # inputs: None
        # returns: PyPNA object

        self.rm = pyvisa.ResourceManager()
        self.channels_open=np.array([])
        self.pna = None

    def connect(self,device=0):
        # sets the vna to the visa device a position 'device' in the resource list
        # inputs: device, int (default=0)
        # returns: None

        self.pna = self.rm.open_resource(self.rm.list_resources()[device])
        self.pna.timeout = 10000

    def load_setup(self, csa_path):
        # writes "Load this calibration file" to pna
        # inputs: csa_path = string
        # returns: None

        self.pna.write(f"MMEM:LOAD '{csa_path}'")
        self.pna.write(f"CALC:PAR:DEL:ALL")

    def add_sparam(self, s_param):
        # creates and displays s-spar measurment on pna
        # inputs: s_sparam, int s11->1, s21->2

        self.pna.write(f"CALC:PAR:EXT 'ch1_{s_param}', 'S{s_param}1'")
        self.pna.write(f"DISP:WIND:TRAC1:FEED 'ch1_{s_param}'")

        self.channels_open=np.append(self.channels_open,np.array(s_param))

    def clear_measurements(self):
        # erases all measurement objects from pna
        # inputs: None
        # returns: None

        self.pna.write(f"CALC:PAR:DEL:ALL")
        self.channels_open=np.array([])

    def print_id(self):
        # Asks the current self.pna object (visa device connected to object) to identify, prints the ID
        # inputs: None
        # returns: None

        self.pna.write("*IDN?")
        print(self.pna.read())

    def get_sparam(self, s_param):
        # Used to query s-par data from pna - 
        # inputs: s_param - string (s11, s21)
        # returns: complex np array same length as s-par data

        if np.any(np.isin(self.channels_open,s_param)):
            self.pna.write(f"CALC:PAR:SEL 'ch1_{s_param}'")
            self.pna.write("FORM:DATA ASCII")
            self.pna.write("CALC:DATA? SDATA")
            data = self.pna.read()
            data = data.split(',')
            real = []
            imag = []
            for point in range(len(data)):
                if point % 2 == 0:
                    real.append(float(data[point]))
                else:
                    imag.append(float(data[point]))
        
            real=np.array(real)
            imag=np.array(imag)

            return real+1j*imag
        else:
            print("S-param requested hasn't been added, use add_sparam(s_param) to open add it")
            print(f"List: {self.channels_open}")
            print(f"Requested: {s_param}")

    def set_averaging(self, toggle):
        # turn averaging on/off with toggle boolean
        # inputs: boolean
        # returns: None

        if isinstance(toggle, bool):
            if toggle:
                self.pna.write("SENS:AVER ON")
            else:
                self.pna.write("SENS:AVER OFF")
        else:
            raise TypeError("set_averaging requires boolean toggle")

    def set_averaging_factor(self, factor):
        # sets how many samples to average
        # inputs: factor, int in range [0,65537]
        # returns: None

        if isinstance(factor, int) and factor > 0 and factor < 65537:
            self.pna.write(f"SENS:AVER:COUN {factor}")
            print(f"Averaging factor set to {factor}")
        else:
            raise TypeError("Averaging factor must be int and within [1,65536].")
