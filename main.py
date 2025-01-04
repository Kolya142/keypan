import datetime
from hashlib import sha1
import json
import os
import random
import time
from evdev import InputDevice, categorize, ecodes

def log(tp: str, msg: str):
    with open("./log.txt", 'a') as f:
        f.write(f'{datetime.datetime.now().ctime()}:{tp}: {msg}\n')

log('INFO', "start")
dev = None
s = open("binds.json").read()
binds = json.loads(s)
shash = sha1(s.encode()).hexdigest()
name = binds["keyboard"]

key_map = {
    ecodes.KEY_A: 'a',
    ecodes.KEY_B: 'b',
    ecodes.KEY_C: 'c',
    ecodes.KEY_D: 'd',
    ecodes.KEY_E: 'e',
    ecodes.KEY_F: 'f',
    ecodes.KEY_G: 'g',
    ecodes.KEY_H: 'h',
    ecodes.KEY_I: 'i',
    ecodes.KEY_J: 'j',
    ecodes.KEY_K: 'k',
    ecodes.KEY_L: 'l',
    ecodes.KEY_M: 'm',
    ecodes.KEY_N: 'n',
    ecodes.KEY_O: 'o',
    ecodes.KEY_P: 'p',
    ecodes.KEY_Q: 'q',
    ecodes.KEY_R: 'r',
    ecodes.KEY_S: 's',
    ecodes.KEY_T: 't',
    ecodes.KEY_U: 'u',
    ecodes.KEY_V: 'v',
    ecodes.KEY_W: 'w',
    ecodes.KEY_X: 'x',
    ecodes.KEY_Y: 'y',
    ecodes.KEY_Z: 'z',
    ecodes.KEY_1: '1',
    ecodes.KEY_2: '2',
    ecodes.KEY_3: '3',
    ecodes.KEY_4: '4',
    ecodes.KEY_5: '5',
    ecodes.KEY_6: '6',
    ecodes.KEY_7: '7',
    ecodes.KEY_8: '8',
    ecodes.KEY_9: '9',
    ecodes.KEY_0: '0',
    ecodes.KEY_SPACE: ' ',
    ecodes.KEY_ENTER: '\\n',
    ecodes.KEY_DOT: '.',
    ecodes.KEY_COMMA: ',',
    ecodes.KEY_MINUS: '-',
    13: '=',
    ecodes.KEY_ESC: 'ESC'
}

f = []
for i in range(30):
    try:
        dev = InputDevice(f'/dev/input/event{i}')
        f.append(dev.name)
        if name != dev.name:
            continue
        break
    except Exception:
        continue
else:
    log("ERROR", f"cannot find keyboard \"{name}\"\nfinded:{f}")
    exit(1)

dev.grab()
log("INFO", f"Listening on '{dev.name}'...")
st = time.time()
a = False
while True:
    try:
        for event in dev.read_loop():
            t = time.time()-st
            if t % 10 < 1:
                if not a:
                    log("INFO", 'check config changes')
                    a = True
                    s = open("binds.json").read()
                    S = sha1(s.encode()).hexdigest()
                    if S != shash:
                        log("INFO", "detected changes, reload config")
                        binds = json.loads(s)
                        shash = S
            else:
                a = False
            if event.type == ecodes.EV_KEY and event.value == 1:
                if event.code not in key_map:
                    continue
                k = key_map[event.code]
                log("KEY", f"detected {k}")
                if k in binds:
                    f = os.fork()
                    if f <= 0:
                        acode = random.randint(0, 1000)
                        log("INFO", f"run program {binds[k]}, id {acode}")
                        ret = os.system(binds[k])
                        d = {256: "256 Command not found", 0: "0 Success", 1: "1 Exception"}
                        if ret in d:
                            ret = d[ret]
                        log("INFO", f"program {acode} returned code: {ret}")
                        exit(0)
    except Exception as e:
        log("ERROR", str(e))