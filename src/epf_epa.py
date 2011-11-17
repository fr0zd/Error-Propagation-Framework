'''

Created on Jun 15, 2011
@author: andrey
'''

import numpy as np

class analyzer(object):
    def __init__(self):
        #Singletone stuff
        _instance = None
        def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = super(analyzer, cls).__new__(
                                    cls, *args, **kwargs)
            return cls._instanc


    def direct_compute(self,G):
        l=len(G.S)
        P=np.zeros([l,l])
        pointers = []
        print "direct_compute started"
        print "Matrix creation, size:" + str(l)+'x'+str(l)
        for s in G.S:
            pointers.append(s)
        for a in G.A:
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
            if pointers[i] == G.initial:
                break
        for j in range(l):
            pointers[j].pr = N[i,j]
        print "direct_compute complete"    
    
    
    
    def iter_compute(self, G, accuracy):
        print 'iter_compute started'
        print 'given accuracy: '+str(accuracy)
        
        for s in G.S:
            s.pr = 0
            s.next_pr = 0
        G.initial.pr = 1
        cur_acc = 1
        
        iter = 0
        while cur_acc > accuracy:
            iter = iter+1
            cur_acc = 1
            for s in G.S:
                if s.pr>0:
                    if len(s.O)>0:
                        #transient
                        for a in s.O:
                            a.s2.next_pr = a.s2.next_pr + s.pr * a.pr
                    else:
                        #absorbing
                        s.next_pr = s.next_pr + s.pr
                        cur_acc = cur_acc - s.pr
                    
            for s in G.S:
                s.pr = s.next_pr
            for s in G.S:
                s.next_pr = 0.0

        print 'iter_compute complete'
        print 'iteration number: '+str(iter)
        print 'achieved accuracy: '+str(cur_acc)
    
 
    
    def loop_reduce(self,G,s_num,prints=False):
        for loop_arc in G.LA:
            if len(G.S) > s_num:                   
                for ao in loop_arc.s1.O:
                    if ao!=loop_arc:
                        ao.pr=ao.pr/(1-loop_arc.pr)
                if prints:           
                    print loop_arc.get_name() + ' - deleted'
                G.remove_arc(loop_arc)  
                return True
        return False                       
    
    def state_reduce(self,G,s_num,initial,prints=False):
        for b in G.S:
            if len(G.S) > s_num:
                #check
                #only one input
                if len(b.I)!=1:
                    continue
                #not an absorption one
                if len(b.O)==0:
                    continue
                #not initial
                if b == initial:
                    continue
                #no self loops
                self_arc = False
                for i in b.I:
                    if i.s1 == i.s2:
                        self_arc = True
                        break
                if self_arc:
                    continue
    
                #TODO check semi absorptions
                #go
    
                a_cb = b.I[0]
                for a_bd in b.O:
                    a_cd = G.get_arc(a_cb.s1,a_bd.s2)
                    if a_cd == None:
                        a_cd=G.add_arc(a_cb.s1,a_bd.s2,0.0)
                    a_cd.pr = a_cb.pr*a_bd.pr+a_cd.pr
                if prints:               
                    print b.name + ' - deleted'       
                G.remove_state(b)
                return True
        return False
    
    def arc_reduce(self,G,s_num,initial,prints=False):
        profit = False
        for b in G.S:
            if len(b.O) == 0:
                continue
            if len(b.I) <= 1:
                continue        
            for a_ab in b.I:
                if len(G.S) > s_num:
                    if a_ab.s1 == initial:
                        continue
                    if a_ab.s1 == a_ab.s2:
                        continue
                    self_arc = False
                    for i in a_ab.s2.I:
                        if i.s1 == i.s2:
                            self_arc = True
                            break
                    if self_arc:
                        continue
                    
                    for a_bc in a_ab.s2.O:
                        if a_bc.s2 != a_ab.s2:
                            a_ac = G.get_arc(a_ab.s1,a_bc.s2)
                            if a_ac == None:
                                a_ac=G.add_arc(a_ab.s1,a_bc.s2,0.0)
                            a_ac.pr = a_ab.pr*a_bc.pr+a_ac.pr
                    if prints:
                        print a_ab.get_name() + ' - deleted'        
                    G.remove_arc(a_ab)
                    profit = True
            if profit:
                return True
        return False
            
    def reduce(self,G,s_num,prints=False):
        initial = G.initial
        print 'reduction started'
        print 'original state number:'+str(len(G.S))
        G.get_absorbing_S_num()
        while len(G.S) > s_num:
            p1 = self.state_reduce(G,s_num,initial,prints)
            if not p1:
                p2 = self.loop_reduce(G,s_num,prints)
                if not p2:
                    p3 = self.arc_reduce(G,s_num,initial,prints)
                    if not p3:
                        break
            else:
                to_del =len(G.S)-G.absorbing_num
                if (to_del % 100 == 0):
                    print 'States to be reduced < ' + str(to_del)              
        print 'reduction complete'
        print 'reduced state number:'+str(len(G.S))
        return G


        