'''
Visualization of the error propagation model

Created on Jun 5, 2011
@author: andrey
'''

import os
import pygraphviz as pgv
import epf_epm as epm

class viz(object):
    """Class for EPF visualization"""
    
    def make_e_name(self, e, no_el_data = False):
        """
        Create an output name for an element of an EPM,
        no_el_data = True - name only
        no_el_data = False - name plus element properties: FAP, EPP, EDP, EDB
        """
        if no_el_data:
            return e.name
        else:
            s = e.name + '\\n' + 'FAP: ' + str(e.fap) + '  EPP: ' + str(e.epp) + '\\n' + 'EDP: ' + str(e.edp) + '  EDB: ' + str(e.edb)
            return s
        
    def draw_epm(self, S, no_el_data = False, no_pr = False):
        """
        Draw CFG and DFG of the EPM as .pdf files to the folder with the name of the EPM
        no_el_data - do not show element properties
        no_pr - do not show transition probabilities of the CFG
        """
        try:
            os.mkdir(S.name+'_pics')
        except:
            pass
        CFG = pgv.AGraph(directed=True)
        for a in S.ACF:
            if no_pr:
                CFG.add_edge(self.make_e_name(a.e1,no_el_data), self.make_e_name(a.e2,no_el_data))
            else:
                CFG.add_edge(self.make_e_name(a.e1,no_el_data), self.make_e_name(a.e2,no_el_data), label=str(a.pr))
        CFG.draw(S.name+'_pics/CFG.pdf',prog='dot')
        DFG = pgv.AGraph(directed=True)
        for a in S.ADF:
            DFG.add_edge(self.make_e_name(a.e1,no_el_data), self.make_e_name(a.e2,no_el_data))
        DFG.draw(S.name+'_pics/DFG.pdf',prog='dot')
        
        
    def __init__(self):
        '''
        Constructor
        '''
        pass
        