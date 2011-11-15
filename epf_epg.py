'''
Contains class of error propagation graph - a state graph of the DTMC
Created on Jun 5, 2011
@author: andrey
'''

import epf_checker as edc
import epf_viz as viz
import numpy as np
import time

class arc(object):
    """Class-container for arc of an EPG"""
    def __init__(self, s1, s2, pr = 1.0, check = False):
        if check:
            self.checker = edc.data_checker()
            self.s1 = self.checker.check_s(s1)
            self.s2 = self.checker.check_s(s2)
            self.pr = self.checker.check_pr(pr)
        else:
            self.s1 = s1
            self.s2 = s2
            self.pr = pr
            
    def get_name(self):
        """name generator"""
        return self.s1.name + ' -' + str(self.pr)[:8] + '-> ' + self.s2.name
        
class state(object):
    """Class-container for state (node) of an EPG"""
    
    def __init__(self, name, e_next = 'none', EFA = set([]), EEP = set([]), EED = set([]), check=False):
        self.name = str(name)[0:128]
        if check:
            self.checker = edc.data_checker()
            if e_next=='none' or e_next=='FS':
                self.e_next=e_next
            else:
                self.e_next = self.checker.check_e(e_next)
            self.EFA = self.checker.check_E(EFA)
            self.EEP = self.checker.check_E(EEP)
            self.EED = self.checker.check_E(EED)
            self.visited = False
        else:
            self.e_next=e_next
            self.EFA = EFA
            self.EEP = EEP
            self.EED = EED
            self.visited = False

        self.I = []
        self.O = []
        self.pr = 0
        self.next_pr = 0

            
class EPG(object):
    """Main class of EPG description"""
    
    def __init__(self, name = 'EPG 1'):
            self.name = str(name)[0:128]
            self.S = []
            self.A = []
            self.LA = []
            self.checker = edc.data_checker()
            self.gen_hist = []
            self.unknown_state = 0
            self.EPM = 0 
    
    def add_state(self, name='', e_next = 'none', EFA = set([]), EEP = set([]), EED = set([])):
        for old_s in self.S:
            if old_s.e_next == e_next and old_s.EFA == EFA and old_s.EEP == EEP and old_s.EED == EED:
                    #raise TypeError('state is already in S')
                    return old_s
        if name == '':
            name = 's'+str(len(self.S))
            
        new_s = state(name, e_next, EFA, EEP, EED)
        self.S.append(new_s)
        if (len(self.S) % 500 == 0):
            print 'States generated: ' +str(len(self.S))
    
        return new_s

    def add_arc(self, s1, s2, pr = 1.0):
        if s1==None or s2 == None:
            return None
        else:
            a=self.get_arc(s1,s2)
            if a!= None:
                a.pr = a.pr + pr
                return a
            a = arc(s1, s2, pr)
            self.A.append(a)
            s1.O.append(a)
            s2.I.append(a)
            if s1 == s2:
                self.LA.append(a)
            return a
    
    def get_arc(self,s1,s2):
        for a in s1.O:
            if a.s2==s2:
                return a
        return None
    
    def remove_arc(self,a):
        a.s1.O.remove(a)
        a.s2.I.remove(a)
        if a.s1 == a.s2:
            self.LA.remove(a)
        self.A.remove(a)

    def remove_state(self,s):
        for ai in s.I:
            ai.s1.O.remove(ai)
            self.A.remove(ai)
        for ao in s.O:
            ao.s2.I.remove(ao)
            self.A.remove(ao)
        self.S.remove(s)
            
    def get_first_unvisited(self):
        for i in range(self.first_unvisied,len(self.S)):
            if self.S[i].visited == False:
                self.first_unvisied = i
                return self.S[i]
        return None
    
    def generate(self, S, stop_number = 0):
        self.EPM = S
        self.t1 = time.time()
        s = self.add_state(e_next = S.initial)
        self.initial = s
        self.first_unvisied=0
        while not (s==None):
            if stop_number > 0 and len(self.S) > stop_number:
                break
            s.visited = True
            if type(s.e_next) is str:
                #=='none' or s.e_next=='FS':
                s = self.get_first_unvisited()
                continue
            
            e_next = s.e_next
            fap = e_next.fap
            epp = e_next.epp
            edp = e_next.edp
            edb = e_next.edb
            EFA = s.EFA
            EEP = s.EEP
            EED = s.EED
            if S.name[0:3] == "RCS":
                if e_next.name == "RegStep":
                    EEP = EEP - set([S.e_by_name("CorrStep")])
                if e_next.name == "CorrStep":
                    EEP = EEP - set([S.e_by_name("RegStep")])
            EFA_plus = EFA | set([e_next])
            EEP_plus = EEP | set([e_next])
            EEP_minus = EEP - set([e_next])
            EED_plus = EED | set([e_next])
            
            

            err_input = False
            for ie in e_next.df_inputs:
                if ie.e1 in EEP:
                    err_input=True
                    break
            left_pr=1
            chh = []
            for ch in e_next.cf_outputs:
                left_pr = left_pr - ch.pr
                chh.append([ch.e2,ch.pr])
            if left_pr > 0:
                chh.append(['none',left_pr])    
            for ch in chh:
                if not err_input:             
                    #no err, no fa --------------------------------------------------
                    pr = ch[1]*(1-fap)
                    if pr>0:
                        new_s = self.add_state('', ch[0], EFA, EEP_minus, EED)
                        self.add_arc(s,new_s,pr)
                    #no err, fa --------------------------------------------------
                    pr = ch[1]*fap
                    if pr>0:
                        new_s = self.add_state('', ch[0], EFA_plus, EEP_plus, EED)
                        self.add_arc(s,new_s,pr)          
                else:
                    if edb == 'FS':
                        #err, fa, ed -1-------------------------------------------------
                        pr = ch[1]*edp
                        if pr>0:
                            new_s = self.add_state('', 'FS', EFA, EEP, EED_plus)
                            self.add_arc(s,new_s,pr)
                    else:
                        #err, fa, ed -1-------------------------------------------------
                        pr = ch[1]*fap*edp
                        if pr>0:
                            new_s = self.add_state('', ch[0], EFA_plus, EEP_plus, EED_plus)
                            self.add_arc(s,new_s,pr)
                        if edb == 'EM':
                            #err, no fa, no ep, ed -1-------------------------------------------------
                            pr = ch[1]*(1-fap)*(1-epp)*edp
                            if pr>0:
                                new_s = self.add_state('', ch[0], EFA, EEP_minus, EED_plus)
                                self.add_arc(s,new_s,pr)  
                            #err, no fa, ep, ed -1-------------------------------------------------
                            pr = ch[1]*(1-fap)*epp*edp
                            if pr>0:
                                new_s = self.add_state('', ch[0], EFA, EEP_plus, EED_plus)
                                self.add_arc(s,new_s,pr)    
                        if edb == 'EC':
                            #err, no fa, ed -1-------------------------------------------------
                            pr = ch[1]*(1-fap)*edp
                            if pr>0:
                                new_s = self.add_state('', ch[0], EFA, EEP_minus, EED_plus)
                                self.add_arc(s,new_s,pr)

                    #err, fa, no ed -3-------------------------------------------------
                    pr = ch[1]*fap*(1 - edp)
                    if pr>0:
                        new_s = self.add_state('', ch[0], EFA_plus, EEP_plus, EED)
                        self.add_arc(s,new_s,pr)
                    #err, no fa, no ep, no ed -1-------------------------------------------------
                    pr = ch[1]*(1-fap)*(1-epp)*(1-edp)
                    if pr>0:
                        new_s = self.add_state('', ch[0], EFA, EEP_minus, EED)
                        self.add_arc(s,new_s,pr)  

                    #err, no fa, ep, no ed -2-------------------------------------------------
                    pr = ch[1]*(1-fap)*epp*(1 - edp)
                    if pr>0:
                        new_s = self.add_state('', ch[0], EFA, EEP_plus, EED)
                        self.add_arc(s,new_s,pr) 

            s = self.get_first_unvisited()

        if stop_number > 0 and len(self.S) > stop_number:
            uk = self.add_state('UNKNOWN', 'UNKNOWN')
            self.unknown_state = uk
            for s in self.S:
                if len(s.O) == 0 and not (type(s.e_next) is str):
                    self.add_arc(s, uk)
        
    def get_absorbing_S_num(self):
        i = 0
        for s in self.S:
            if len(s.O)==0:
                i=i+1
        self.absorbing_num = i
        return i
    
        
    def get_final_S_num(self):
        i = 0
        for s in self.S:
            if type(s.e_next) is str:
                i=i+1
        self.final_num = i
        return i
    

    def direct_compute(self):
        l=len(self.S)
        P=np.zeros([l,l])
        pointers = []
        print "direct_compute started"
        print "Matrix creation, size:" + str(l)+'x'+str(l)
        for s in self.S:
            pointers.append(s)
        for a in self.A:
            for i in range(l):
                if (pointers[i] == a.s1):
                    break
            for j in range(l):
                if (pointers[j] == a.s2):
                    break
            P[i,j]=a.pr
        print "done"
        print "Computation"
        I=np.identity(l)
        N=np.linalg.solve(I-P,I)
        print "done"
        for i in range(l):
            if pointers[i] == self.initial:
                break
        for j in range(l):
            pointers[j].pr = N[i,j]
        print "direct_compute complete"    
    
    
    
    def iter_compute(self, acc):
        print 'iter_compute started'
        print 'given accuracy: '+str(acc)
        
        for s in self.S:
            s.pr = 0
            s.next_pr = 0
        self.initial.pr = 1
        cur_acc = 1
        
        iter = 0
        while cur_acc > acc:
            iter = iter+1
            cur_acc = 1
            for s in self.S:
                if s.pr>0:
                    if len(s.O)>0:
                        #transient
                        for a in s.O:
                            a.s2.next_pr = a.s2.next_pr + s.pr * a.pr
                    else:
                        #absorbing
                        s.next_pr = s.next_pr + s.pr
                        cur_acc = cur_acc - s.pr
                    
            for s in self.S:
                s.pr = s.next_pr
            for s in self.S:
                s.next_pr = 0.0

        print 'iter_compute complete'
        print 'iteration number: '+str(iter)
        print 'achieved accuracy: '+str(cur_acc)
    
    
    
    
    def show_results(self, num):
        V=viz.viz()
        res = []
        for s in self.S:
            if len(s.O)==0:
                res.append([s.pr,V.make_s_name(s)])
            
        res.sort(reverse=True)
        prr = 0
        for i in range(min(num,len(res))):
            print res[i]
            prr = prr + res[i][0]
        print 'check sum = ' + str(prr)         
    