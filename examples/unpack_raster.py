import numpy as np
import matplotlib.pyplot as plt
import time

def generate_raster_scan(xlim,ylim,xstep,ystep):
    pos=np.array([xlim[0],ylim[0]])
    vec=np.array([xstep,0])
    scan_coord=np.array([xlim[0],ylim[0]])
    while pos[1]<=ylim[1]:
        if scan_coord.size>2:
            if np.any(pos!=scan_coord[-1,:]):
                scan_coord=np.vstack((scan_coord,pos))
        pos+=vec
        scan_coord=np.vstack((scan_coord,pos))
        if pos[0]==xlim[1]:
            pos[1]+=ystep
            vec*=-1
        elif pos[0]==xlim[0]:
            pos[1]+=ystep
            vec*=-1

    scan_index=np.empty(scan_coord.shape)
    scan_index[:,0]=(scan_coord[:,0]/xstep)-xlim[0]/xstep
    scan_index[:,1]=(scan_coord[:,1]/ystep)-ylim[0]/ystep

    return scan_coord,scan_index

xlim=np.array([10,40])
ylim=np.array([10,40])
step=1
sc,ind=generate_raster_scan(xlim,ylim,step,step)
res=np.zeros([int(np.max(ind[:,0])-np.min(ind[:,0]))+1,int(np.max(ind[:,1])-np.min(ind[:,1]))+1])

x=np.arange(xlim[0],xlim[1]+step,step)
y=np.arange(ylim[0],ylim[1]+step,step)

xm,ym=np.meshgrid(x,y)

print(ind)

plt.ion()
fig=plt.figure()
ax=fig.add_subplot(111)
ax.set_xlim([xlim[0],xlim[1]])
ax.set_ylim([ylim[0],ylim[1]])
ax.set_xlabel("x (mm)")
ax.set_ylabel("y (mm)")
cmesh=ax.pcolormesh(xm,ym,res,shading="auto")
t=time.time()
for i,pos in enumerate(sc):
    try:
        res[int(ind[i,1]),int(ind[i,0])]=1
        cmesh=ax.pcolormesh(xm,ym,res,vmin=0,shading="auto")
        ax.set_title("Pixel "+str(i)+"/"+str(ind.shape[0])+" ("+str(np.around(100*i/ind.shape[0],decimals=2))+"% Complete) - Elapsed Time = "+str(np.around(time.time()-t,decimals=2))+" s")
        plt.pause(0.01)
    except KeyboardInterrupt:
        plt.close('all')
        break

plt.ioff()
cmesh=ax.pcolormesh(xm,ym,res,vmin=0,shading="auto")
plt.show()