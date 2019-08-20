from threading import Thread
from Detector import detect
from Sensors import sense

if __name__ == '__main__':
    Thread(target = detect).start()
    Thread(target = sesne).start()