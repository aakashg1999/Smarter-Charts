import urllib.request
import socket
import time
import re

def download_image(filename):
    filename= (filename + '.txt')
    t=1
    for line in open(filename):
        j=str(t)
        try:
            start=time.time()
            
            socket.setdefaulttimeout(5)
            urllib.request.urlretrieve(line,j+'.jpeg')
            end=time.time()
            print(t, -1*(start-end))
            t=t+1
        except:
            continue

download_image('pc')
