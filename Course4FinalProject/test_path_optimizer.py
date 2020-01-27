import numpy as np
import path_optimizer
import matplotlib.pyplot as plt

po = path_optimizer.PathOptimizer()

path = po.optimize_spiral([9.185], [-4.499], 4.261)
# path = po.optimize_spiral(0.0, 0.0, 10.22874134679308) # NAN result

for x,y,t in np.stack(arrays=path, axis=1):
    print("{:5.2f} {:5.2f} {:5.2f}".format(x, y, t))

fig = plt.figure()
ax = fig.add_subplot(1,2,1)
ax.plot(path[0],path[1])
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")

ax = fig.add_subplot(1,2,2)
ax.plot(path[0],path[2])
ax.set_xlabel("x [m]")
ax.set_ylabel("theta [rad]")
plt.show()