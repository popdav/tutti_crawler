import os, sys, gzip, tarfile
from datetime import datetime
from threading import Thread
from threading import Thread


def estimate():
    return 10

def start_crawler():
    os.system('docker run --rm -it --network=my_socket_ipc_network tutti_slave')

def main():

    for i in range(estimate()):
        p = Thread(target=start_crawler)
        p.start()
    
if __name__ == "__main__":
    main()