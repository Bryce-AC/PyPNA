###########################################################
# This file benchmarks the read rate of the PyPNA Library #
#                  Harry Lees - Dec 2021                  #
###########################################################

import PyPNA
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

save_path=r"C:\Users\withawat-admin\Documents\PNA-Python-Repositories\sandbox"

t0=time.time()

#temp
def load_setup(pyna,csa_path):
    pyna.pna.write(f"MMEM:LOAD '{csa_path}'")
    pyna.pna.write(f"CALC:PAR:DEL:ALL")

def get_sparam(pyna, s_param):
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

#setup pna
pm = PyPNA.PyPNA()

pm.connect()

# pm.load_setup('D:/harrys_setup.csa')
#pm.load_setup('D:/pypna.csa')
load_setup(pm,'D:/pypna.csa')

pm.pna.write("SENS:AVER ON")
# pm.pna.write("SENS:AVER OFF")

factor = 1
pm.pna.write(f"SENS:AVER:COUN {factor}")

pm.pna.write(f"CALC:PAR:EXT 'ch1_1', 'S11'")
pm.pna.write(f"DISP:WIND:TRAC1:FEED 'ch1_1'")
pm.pna.write(f"CALC:PAR:EXT 'ch1_2', 'S21'")
pm.pna.write(f"DISP:WIND:TRAC2:FEED 'ch1_2'")

pm.pna.timeout = 10000

pm.print_id()

t00=time.time()
t0=time.time()
ns=1000
for n in np.arange(0,ns):
    s21=get_sparam(pm,'2')
    s11=get_sparam(pm,'1')
    t1=time.time()
    print("#"+str(n)+" = "+str(t1-t0)+" s"+" ("+str(1/(t1-t0))+" samples/s)")
    t0=time.time()

print("Total time for "+str(ns)+" samples = "+str(t1-t00))
print("Average time per sample = " +str((t1-t00)/ns)+" s")
print(f"Average sample rate = {1/((t1-t00)/ns)} per second")