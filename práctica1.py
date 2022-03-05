#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 10:14:56 2022

@author: hanjiezhu
"""

import random
from multiprocessing import Process, Manager
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import current_process
from multiprocessing import Value, Array
from time import sleep

N = 3
K = 5



def productor(storage, pid, empty, non_empty):
    print(f'productor {pid} starting')
    val = random.randint(0, 5)
    for i in range(K+1):
        val += random.randint(0, 5)
        empty.acquire()
        if i == K:
            storage[pid] = -1
            print(f"productor/{pid} finished")
        else:
            storage[pid] = val
            print(f"position {i}: productor/{pid} has produced {storage[pid]}")
        non_empty.release()  
    print(f"productor {pid} finished")

        
def consumidor(storage, empty, non_empty, lista):
    sleep(1)
    for i in range(len(non_empty)):
        non_empty[i].acquire()
    while True:
        mini, j = minimo(storage)
        if mini == -1:
            print("consumidor finished")
            break
        lista += [mini]
        print(list(storage))
        print(f"consume position {j} and save the value {mini}")
        if mini != -1:
            empty[j].release()
            non_empty[j].release()

            
 
def minimo(storage):
    mini, j = storage[0], 0
    for i in range(len(storage)):
        aux = storage[i]
        if mini < 0 and aux >= 0:
            mini = aux
            j = i
        elif aux < mini and aux >= 0:
            mini = aux
            j = i
    return mini, j
  
      
def main():
    storage = Array('i', N)
    non_empty = [Semaphore(0) for _ in range(N)]
    empty = [Semaphore(1) for _ in range(N)]
    prodlst = []
    resultado = Manager().list()
    
    cons = Process(target=consumidor,
                      args=(storage,empty, non_empty, resultado))
    for pid in range(N):
        prodlst.append(Process(target=productor, args=(storage, pid, empty[pid], non_empty[pid])) )
    for p in prodlst:
        p.start()
    cons.start()
    
    for p in prodlst:
        p.join()
    cons.join()
    
    print(resultado)
    
                
    
if __name__ == '__main__':
    main()


    
    




        
        
        
