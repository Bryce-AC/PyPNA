import pyvisa


class PyPNA:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.pna = None

    def connect(self):
        self.pna = self.rm.open_resource(self.rm.list_resources()[0])

    def load_setup(self, csa_path):
        self.pna.write("MMEM:LOAD '" + csa_path + "'")

    def print_id(self):
        self.pna.write("*IDN?")
        print(self.pna.read())
