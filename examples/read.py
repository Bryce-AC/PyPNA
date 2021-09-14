import pyvisa
import os
import matplotlib.pyplot as plt
import numpy as np
import time

rm = pyvisa.ResourceManager()

vna = rm.open_resource(rm.list_resources()[0])

vna.timeout = 10000

# vna.write("SYST:PRES; *OPC?")
# print(vna.read())

vna.write("CALC:PAR:DEL:ALL")

vna.write("*CLS")

vna.write("MMEM:LOAD 'D:/harrys_setup.csa'")

time.sleep(1)

# check the error queue
vna.write("SYST:ERR?")
print(vna.read())

vna.write("CALC:PAR:EXT 'ch1_S11', 'S11'")
#vna.write("CALC:PAR:EXT 'ch1_S21', 'S21'")

# Set data transfer format to ASCII
vna.write("FORM:DATA ASCII")

#vna.write("SENS:SWE:POIN 1001;*OPC?")
#vna.read()

# vna.write("CALC:MATH:MEM")
vna.write("CALC:DATA? SDATA")

data = vna.read()
data = data.split(',')

print(len(data))
print(data)
real = []
imag = []

for point in range(len(data)):
    if point % 2 == 0:
        real.append(float(data[point]))
    else:
        imag.append(float(data[point]))

real=np.array(real)
imag=np.array(imag)
s11_cpx=real+1j*imag
mag=20*np.log10(np.abs(s11_cpx))
phase=np.unwrap(np.angle(s11_cpx))

plt.figure()
plt.plot(mag)


#vna.write("CALC:PAR:EXT 'ch1_S11', 'S11'")
vna.write("CALC:PAR:EXT 'ch1_S21', 'S21'")

# Set data transfer format to ASCII
vna.write("FORM:DATA ASCII")

#vna.write("SENS:SWE:POIN 1001;*OPC?")
#vna.read()

# vna.write("CALC:MATH:MEM")
vna.write("CALC:DATA? SDATA")

data = vna.read()
data = data.split(',')

print(len(data))
print(data)
real = []
imag = []

for point in range(len(data)):
    if point % 2 == 0:
        real.append(float(data[point]))
    else:
        imag.append(float(data[point]))

real=np.array(real)
imag=np.array(imag)
s11_cpx=real+1j*imag
mag=20*np.log10(np.abs(s11_cpx))
phase=np.unwrap(np.angle(s11_cpx))

plt.plot(mag)
plt.ylim([-50,0])
plt.show()

# print(vna.query("*IDN?"))

