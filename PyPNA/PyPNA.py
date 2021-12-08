import pyvisa
import numpy as np
class PyPNA:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.pna = None

    def connect(self):
        self.pna = self.rm.open_resource(self.rm.list_resources()[0])

    def load_setup(self, csa_path):
        self.pna.write(f"MMEM:LOAD '{csa_path}'")

    def clear_measurements(self):
        self.pna.write(f"CALC:PAR:DEL:ALL")

    def print_id(self):
        self.pna.write("*IDN?")
        print(self.pna.read())

    def get_sparam(pyna, s_param):
        pyna.pna.write(f"CALC:PAR:EXT 'ch1_{s_param}', '{s_param}'")
        pyna.pna.write(f"CALC:PAR:SEL 'ch1_{s_param}'")
        pyna.pna.write("FORM:DATA ASCII")
        pyna.pna.write("CALC:DATA? SDATA")
        data = pyna.pna.read()
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

    # turn averaging on/off with toggle boolean
    def set_averaging(self, toggle):
        if isinstance(toggle, bool):
            if toggle:
                self.pna.write("SENS:AVER ON")
            else:
                self.pna.write("SENS:AVER OFF")
        else:
            raise TypeError("set_averaging requires boolean toggle")

    def set_averaging_factor(self, factor):
        if isinstance(factor, int) and factor > 0 and factor < 65537:
            self.pna.write(f"SENS:AVER:COUN {factor}")
            print(f"Averaging factor set to {factor}")
        else:
            raise TypeError("Averaging factor must be int and within [1,65536].")
