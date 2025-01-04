import os
import time

while True:
    r = ''
    with open("tmp") as f:
        r = f.read()
    if r:
        f = os.fork()
        if f > 0:
            os.system(r)
        with open("tmp", 'w') as f:
            f.write('')
    time.sleep(0.1)