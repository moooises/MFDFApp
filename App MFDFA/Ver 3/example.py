import matplotlib.pylab as plt
import numpy as np

fig = plt.figure()
closed = False

def handle_close(evt):
    global closed
    closed = True

def waitforbuttonpress():
    while plt.waitforbuttonpress(0.2) is None:
        if closed:
            return False
    return True

fig.canvas.mpl_connect('close_event', handle_close)
while True:
    plt.imshow(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
    plt.draw()
    if not waitforbuttonpress():
        break
    print('.')