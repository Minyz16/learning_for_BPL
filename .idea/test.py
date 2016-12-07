import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

cv = np.array([[ 50.,  25.],
   [ 59.,  12.],
   [ 50.,  10.],
   [ 57.,   2.],
   [ 40.,   4.],
   [ 40.,   14.]])

x=cv[:,0]
y=cv[:,1]
plt.plot(x, y, "o")

s=0

tck, t = interpolate.splprep([x, y], s=s)
xi, yi = interpolate.splev(np.linspace(t[0], t[-1], 200), tck)
plt.plot(xi, yi, lw=2, label=u"s=%g" % s)
xx=tck[1][0]
yy=tck[1][1]
plt.plot(xx,yy,'k-')
plt.legend();
plt.show()