import matplotlib.pyplot as plt
from math import sqrt

D = 0.4
truncate = 25

R = D/2.0
h =  truncate*D/100.0         # R/2.0  # Counts from the top
r = sqrt(2*R*h-h*h)
t = r/R

a = R - h

Y = 0.5
y = Y - a

circle1 = plt.Circle((0.5, Y), R, color='r')
#circle2 = plt.Circle((0.5, 0.5), r, color='g')
circle3 = plt.Circle((0.5, y), R/t, color='b')       # R*R/r

fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot

ax.add_artist(circle1)
#ax.add_artist(circle2)
ax.add_artist(circle3)

fig.savefig('plotcircles.png')

###

