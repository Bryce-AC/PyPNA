import PyPNA
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

save_path=r"C:\Users\withawat-admin\Documents\PNA-Python-Repositories\sandbox\2021.09.22 - Edmond"

#temp
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

    #pyna.pna.write("CALC:PAR:DEL:ALL")

    return real+1j*imag

#setup pna
pm = PyPNA.PyPNA()

pm.connect()

pm.load_setup('D:/harrys_setup.csa')

pm.pna.timeout = 10000

pm.print_id()

f=np.arange(220,330,110/1001)
ts=1/110e9
t=np.arange(0,ts*1001,ts)

head="Frequency (GHz) s11_real s11_imag s21_real s21_imag"

t0=time.time()

#setup animated plot
fig, (ax1,ax2) = plt.subplots(1,2)
pos=np.array([0,0])
vec=np.array([1,1])
ln1, = ax1.plot([], [], 'r')
ln2, = ax1.plot([], [], 'b')
ln3, = ax2.plot([], [], 'r')
ln4, = ax2.plot([], [], 'b')

#take first measurment
s21=get_sparam(pm,'S21')
s11=get_sparam(pm,'S11')
s21_save=np.column_stack((f,np.real(s11),np.imag(s11),np.real(s21),np.imag(s21)))
filename="\paper_t=0.txt"
np.savetxt(save_path+filename,s21_save,header=head)
np.savetxt(save_path+r"\time.txt",np.array([t0]))

def init():
    ax1.set_xlim(220, 330)
    ax1.set_ylim(-50, 0)
    ax1.set_xlabel("Frequency (GHz)")
    ax1.set_ylabel("Amplitude (dB)")
    ax1.set_title("Frequency Domain")
    ax2.set_ylim(0, 0.06)
    ax2.set_xlim(0,ts*1001*1e9)
    ax2.set_xlim(0,5)
    ax2.set_xlabel("Time (ns)")
    ax2.set_ylabel("Amplitude (a.u.)")
    ax2.set_xticks(np.arange(0,5.5,0.5))
    ax2.set_title("Time Domain")
    ax2.legend(["S11","S21"])
    return ln1,ln2

def update(frame):
    s21=get_sparam(pm,'S21')
    s11=get_sparam(pm,'S11')

    #pna
    #ln1.set_data(f,20*np.log10(np.abs(s11)))
    #ln2.set_data(f,20*np.log10(np.abs(s21)))

    s21_save=np.column_stack((f,np.real(s11),np.imag(s11),np.real(s21),np.imag(s21)))

    t0=np.loadtxt(save_path+r"\time.txt")
    t1=time.time()
    print("Time Elapsed: "+str(t1-t0)+" s")
    if (t1-t0)%60 < 0.3:
        filename="\paper_t="+str(np.around(t1-t0,decimals=0))+".txt"
        np.savetxt(r"C:\Users\withawat-admin\Documents\PNA-Python-Repositories\sandbox\2021.09.22 - Edmond"+filename,s21_save,header=head)

    #ifft
    ln1.set_data(f,20*np.log10(np.abs((s11))))
    ln2.set_data(f,20*np.log10(np.abs((s21))))
    ln3.set_data(t*1e9,(np.abs(np.fft.ifft(s11))))
    ln4.set_data(t*1e9,(np.abs(np.fft.ifft(s21))))

    #time.sleep(1)

    return ln1,ln2,ln3,ln4

try:
    ani = FuncAnimation(fig, update, frames=None, init_func=init, blit=True)
except KeyboardInterrupt:
    plt.close('all')
plt.show()