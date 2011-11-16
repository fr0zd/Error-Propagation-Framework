'''
This module contains a singleton for input data checking
Created on Jun 9, 2011
@author: andrey
'''


import epf_epm as epm
import epf_epg as epg


class data_checker (object):
    """Class for input checking"""
    
    #Singletone stuff
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(data_checker, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    
    def check_pr(self, val):
        f_val=float(val)
        if f_val>=0 and f_val<=1:
            return f_val
        else:
            raise TypeError('the probability value is out of [0,1]')
            return 0.0
    
    def check_edb(self, val):
        s_val=str(val)
        if s_val in self.EDB_list:
            return s_val
        else:
            raise TypeError('Wrong EDB value')
            return 'FS'
        
    def check_e(self, el):
        if isinstance(el,epm.element):
            return el
        else:
            raise TypeError('The element is not an element')
            return None
        
    def check_E(self, E):
        for e in E:
            if self.check_e(e)==None:
                return None
        return E
    
    def check_e_in_E(self,el,E):
        for ce in E:
            if ce.name == el.name:
                raise TypeError('An element with this name is already existed in E')
                return True
        return False    

        
    def check_s(self, st):
        if isinstance(st,epg.s):
            return st
        else:
            raise TypeError('state is not state')
            return None
                    
        
        
    def __init__(self):
        self.EDB_list = ['FS','EM','EC']