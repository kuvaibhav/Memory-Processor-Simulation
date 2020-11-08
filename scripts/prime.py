import multiprocessing
import sys
import time
from sys import argv
import threading
from multiprocessing import Process
import math


def is_prime(n):
    root = int(math.sqrt(n))
    for i in range(2,root+1):
        if n%i == 0:
            return False
    return True

def my_fun(lock, arg):
    while True:
        lock.acquire()
        t = arg.value
        arg.value = arg.value + 1
        lock.release()
        # print("I am trying to find if this is prime:", t)
        if (is_prime(t)):
            print("prime:", t)

        if arg.value > 4000000:
            break


if __name__ == "__main__":
    start = time.time()
    a = sys.argv[0]
    processes = []
    glob_var = [0]
    vaal = multiprocessing.Value('i', 1)
    lock = multiprocessing.Lock()
    is_prime(7)
    if len(argv) < 5:
                print("""USAGE: python primes.py max met t verb
        max     : Maximum number to scan primes on.
        met     : Method: Single thread = 's'   
                          Multi thread  = 'm'
        t       : Number of threads to use (Ignored when met=s)
        verb    : 0=prints only execution time.
                  1=prints also the numbers.""")
    else:
        maxi = argv[1]
        met = argv[2]
        t = argv[3]
        verb = argv[4]
        if met == 's':
            for i in range(0,int(maxi)):
                if is_prime(i):
                    print("s:",i)
        # 100
        
        elif met == 'm':
            for i in range(0,int(t)):
                p = Process(target=my_fun, args=(lock,vaal))
                processes.append(p)
                p.start()


        for p in processes:
            p.join()
        end = time.time()

        print("Time = ", end-start)