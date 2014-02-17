from datetime import datetime
import random
import time

def check_sleep(amount):
    start = time.time() #datetime.now()
    time.sleep(amount)
    end = time.time() #datetime.now()
    delta = end-start
    return delta
#     return delta.seconds + delta.microseconds/1000000.

for i in range(1000):
    print random.random()
#     t=0.000001*i
#     print i,1000000*check_sleep(t)

# print "Average error is %0.2fms" % error