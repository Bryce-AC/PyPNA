import PyPNA
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#setup pna
pm = PyPNA.PyPNA()

pm.connect()

pm.load_setup('D:/harrys_setup.csa')

pm.print_id()

f=np.arange(220,330+110/1001,110/1001)

#setup animated plot
fig, ax = plt.subplots()
pos=np.array([0,0])
vec=np.array([1,1])
ln1, = plt.plot([], [], 'r')
ln2, = plt.plot([], [], 'b')

def init():
    ax.set_xlim(0, 1001)
    ax.set_ylim(-50, 0)
    return ln1,ln2

def update(frame,pm):
    s11=pm.get_sparam('s11')
    s21=pm.get_sparam('s21')

    ln1.set_data(f,np.abs(s11))
    ln2.set_data(f,np.abs(s21))
    return ln1,ln2

ani = FuncAnimation(fig, update, fargs=pm, frames=None,
                    init_func=init, blit=True)
plt.show()