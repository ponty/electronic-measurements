import matplotlib.pyplot as plt
from numpy.random import normal
y=gaussian_numbers = normal(size=100)
# gaussian_numbers=[4,5,6,7,8]*11
y=[10*x+32 for x in y]
y=map(int,y)
y=y+[x+67 for x in y]
print y
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylim([0,1000])
ax.hist(y, 33, normed=0, histtype='stepfilled')
# plt.title("Gaussian Histogram")
# plt.xlabel("Value")
# plt.ylabel("Frequency")
plt.show()