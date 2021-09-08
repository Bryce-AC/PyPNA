import numpy as np
import matplotlib.pyplot as plt
import thorlabs_apt as apt

def generate_raster_scan(xlim,ylim,step):
    pos=np.array([xlim[0],ylim[0]])
    vec=np.array([step,0])
    scan_coord=np.array([xlim[0],ylim[0]])
    while pos[1]<=ylim[1]:
        if scan_coord.size>2:
            if np.any(pos!=scan_coord[-1,:]):
                scan_coord=np.vstack((scan_coord,pos))
        pos+=vec
        scan_coord=np.vstack((scan_coord,pos))
        if pos[0]==xlim[1]:
            pos[1]+=step
            vec*=-1
        elif pos[0]==xlim[0]:
            pos[1]+=step
            vec*=-1

    return scan_coord

def scan_2d(xlim,ylim,step):
    pass

### main code
xlim=np.array([0,10])
ylim=np.array([0,10])
step=1
sc=generate_raster_scan(xlim,ylim,step)
print(sc)
dif=np.diff(sc,axis=0)
plt.figure()
plt.subplot(211)
plt.plot(sc[:,0],sc[:,1])
plt.subplot(212)
plt.plot(dif[:,0])
plt.plot(dif[:,1])
plt.show()