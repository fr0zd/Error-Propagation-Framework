'''
This module contains a group of classes for storage of the dual-graph system representation.
epm_system - container for an entire system
epm_element - container for a system element
epm_cf_arc - container for a control flow arc
epm_df_arc - container for a data flow arc

Created on Jun 15, 2011
@author: andrey
'''

import epf_checker as edc


class element(object):
    """Class-contains for a system element"""
    
    def __init__(self, name, fap = 0.0, epp = 0.0, edp = 0.0, edb = 'FS'):
        """Constructor"""
        self.checker = edc.data_checker()
        self.name = str(name)[0:128]
        self.fap = self.checker.check_pr(fap)
        self.epp = self.checker.check_pr(epp)
        self.edp = self.checker.check_pr(edp)
        self.edb = self.checker.check_edb(edb)
        self.DI=set([])
        self.DO=set([])
        self.CI=set([])
        self.CO=set([])  
            
class cf_arc(object):
    """Class-container for a CF arc"""
    
    def __init__(self, e1, e2, pr = 1.0):
        self.checker = edc.data_checker()
        self.e1 = self.checker.check_e(e1)
        self.e2 = self.checker.check_e(e2)
        self.pr = self.checker.check_pr(pr)
        self.name = e1.name + ' -' + str(pr) + '-> ' + e2.name
        
class df_arc(object):
    """Class-container for a DF arc"""
    
    def __init__(self, e1, e2):
        self.checker = edc.data_checker()
        self.e1 = self.checker.check_e(e1)
        self.e2 = self.checker.check_e(e2)
        self.name = e1.name + ' -DF-> ' + e2.name
        
class system(object):
    """Class-container for the dual graph representation of a system"""
    
    def __init__(self, name = 'A system'):
        """Constructor"""
        self.name = name[0:127]
        self.checker = edc.data_checker()
        self.E=set([])
        self.ACF = []
        self.ADF = []
        self.initial=None
    
    def add_element(self, name = '', fap = 0.0, epp = 0.0, edp = 0.0, edb = 'FS', is_initial = False):
        """Add new element"""
        if name == '':
            name = 'e'+str(len(self.E))
        el = element(name, fap, epp, edp, edb)
        if self.checker.check_e_in_E(el,self.E):
            return False
        else:
            if is_initial == True:
                self.initial = el
            else:
                if len(self.E) == 0:
                    self.initial = el
            self.E.add(el)
            return el

    def add_cf_arc(self, e1, e2, pr = 1.0):
        """Add a CF arc"""
        if isinstance(e1, str):
            e1 = self.get_element_by_name(e1)
        if isinstance(e2, str):
            e2 = self.get_element_by_name(e2)           
        a = cf_arc(e1, e2, pr)
        e1.CO.add(a)
        e2.CI.add(a)
        self.ACF.append(a)            

    def add_df_arc(self, e1, e2):
        """Add a DF arc"""
        if isinstance(e1, str):
            e1 = self.get_element_by_name(e1)
        if isinstance(e2, str):
            e2 = self.get_element_by_name(e2)   
        a = df_arc(e1, e2)
        e1.DO.add(a)
        e2.DI.add(a)
        self.ADF.append(a) 
        
    def get_element_by_name(self, name):
        """Return an element by its name"""
        for e in self.E:
            if e.name == name:
                return e