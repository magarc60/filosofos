# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 10:20:50 2022

@author: Maria
"""

from multiprocessing import Condition, Lock,Value


class Table(object):
    def __init__(self,NPHIL,manager):
        self.fforks=manager.list([True]*NPHIL)
        self.mutex=Lock()
        self.free_fork=Condition(self.mutex)
        self.current_phil=None
        self.NPHIL=NPHIL
        
    def set_current_phil(self,phil):
        self.current_phil=phil
        
    def  get_current_phil(self): 
        return self.current_phil
    
    def are_free_fork(self):
        phil=self.current_phil
        return self.fforks[phil] and self.fforks[(phil+1) % self.NPHIL]
    
    def wants_eat(self,phil):
        self.mutex.acquire()
        self.free_fork.wait_for(self.are_free_fork)
        self.fforks[phil]=False
        self.fforks[(phil+1) % self.NPHIL]=False
        self.mutex.release()
            
    def wants_think(self,phil):
        self.mutex.acquire()
        self.fforks[phil]=True
        self.fforks[(phil+1) % self.NPHIL]=True
        self.free_fork.notify_all()
        self.mutex.release()
    

class CheatMonitor(object):
    def __init__(self):
        self.eating=Value('i',0)
        self.thinking=Value('i',0)
        self.mutex=Lock()
        self.other_eating=Condition(self.mutex)
        
        
    def wants_think(self, i):
        self.mutex.acquire()
        self.other_eating.wait_for(lambda:self.eating.value==2)
        self.eating.value -=1
        self.mutex.release()
    
    def is_eating(self, i):
        self.mutex.acquire()
        self.eating.value+=1
        self.other_eating.notify()
        self.mutex.release()
        
       
class AnticheatTable(object):  
    def __init__(self,NPHIL,manager):
        self.fforks=manager.list([True]*NPHIL)
        self.mutex=Lock()
        self.free_fork=Condition(self.mutex)
        self.current_phil=None
        self.NPHIL=NPHIL
        
    def set_current_phil(self,phil):
        self.current_phil=phil
        
    def  get_current_phil(self): 
        return self.current_phil
    
    def are_free_fork(self):
        phil=self.current_phil
        return self.fforks[phil] and self.fforks[(phil+1) % self.NPHIL]
    
    def wants_eat(self,phil):
        self.mutex.acquire()
        self.free_fork.wait_for(self.are_free_fork)
        self.fforks[phil]=False
        self.fforks[(phil+1) % self.NPHIL]=False
        self.mutex.release()
            
    def wants_think(self,phil):
        self.mutex.acquire()
        self.fforks[phil]=True
        self.fforks[(phil+1) % self.NPHIL]=True
        self.free_fork.notify_all()
        self.mutex.release()
    
    
    
    
    
    
    
    
    
    
  