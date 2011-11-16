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
            os.mkdir(S.name)
        except:
            pass
        CFG = pgv.AGraph(directed=True)
        for a in S.ACF:
            if no_pr:
                CFG.add_edge(self.make_e_name(a.e1,no_el_data), self.make_e_name(a.e2,no_el_data))
            else:
                CFG.add_edge(self.make_e_name(a.e1,no_el_data), self.make_e_name(a.e2,no_el_data), label=str(a.pr))
        CFG.draw(S.name+'/CFG.pdf',prog='dot')
        DFG = pgv.AGraph(directed=True)
        for a in S.ADF:
            DFG.add_edge(self.make_e_name(a.e1,no_el_data), self.make_e_name(a.e2,no_el_data))
        DFG.draw(S.name+'/DFG.pdf',prog='dot')
        



    def make_s_name(self, s):
        NXT = ''
        if isinstance(s.e_next, str):
            NXT = s.e_next
        else:
            NXT = str(s.e_next.name)
        EFA = ''
        EEP = ''
        EED = ''
        for e in s.EFA:
            EFA = EFA + e.name + ' '
        for e in s.EEP:
            EEP = EEP + e.name + ' '
        for e in s.EED:
            EED = EED + e.name + ' '
        st = s.name + '\\n' + 'nxt:' + NXT + '\\n' + 'FA:' + EFA + '\\n' + 'EP:' + EEP + '\\n' + 'ED:' + EED
        #st = 'nxt:' + NXT + '\\n' + 'FA:' + EFA + '\\n' + 'EP:' + EEP + '\\n' + 'ED:' + EED
        return st    
    
    def make_s_name(self, s):
        NXT = ''
        if isinstance(s.e_next, str):
            NXT = s.e_next
        else:
            NXT = str(s.e_next.name)
        st = s.name + '\\n' + 'nxt:' + NXT
        EFA = ''
        EEP = ''
        EED = ''
        for e in s.EFA:
            EFA = EFA + e.name + ' '
        if EFA!='':
            st = st + '\\n' + 'FA:' + EFA
        for e in s.EEP:
            EEP = EEP + e.name + ' '
        if EEP!='':
            st = st + '\\n' + 'EP:' + EEP
        for e in s.EED:
            EED = EED + e.name + ' '
        if EED!='':
            st = st + '\\n' + 'ED:' + EED
        return st      
    
    def draw_epg(self, G):
        try:
            os.mkdir(G.EPM.name)
        except:
            pass
        EPG = pgv.AGraph(directed=True)
        for a in G.A:
            EPG.add_edge(self.make_s_name(a.s1), self.make_s_name(a.s2), label=str(a.pr))
        EPG.draw(G.EPM.name+'/EPG.pdf',prog='dot')




        
    def __init__(self):
        '''
        Constructor
        '''
        pass
        