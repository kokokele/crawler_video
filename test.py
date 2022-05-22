import time

start = time.time()
while 1:
    t = time.time()
    if (t - start) % 5 == 0 :
        print(t)
