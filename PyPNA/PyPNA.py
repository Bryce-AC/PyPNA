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

    def get_sparam(self, s_param):
        self.pna.write(f"CALC:PAR:EXT 'ch1_{s_param}', '{s_param}'")
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