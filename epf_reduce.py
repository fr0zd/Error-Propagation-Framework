'''
Created on Jun 15, 2011

@author: admin
'''


import epf_epg as epg

class reducer(object):
    def __init__(self):
        #Singletone stuff
        _instance = None
        def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = super(reducer, cls).__new__(
                                    cls, *args, **kwargs)
            return cls._instance    
    
    def loop_reduce(self,G,prints=False):
        for loop_arc in G.LA:                    
                for ao in loop_arc.s1.O:
                    if ao!=loop_arc:
                        ao.pr=ao.pr/(1-loop_arc.pr)
                if prints:           
                    print loop_arc.get_name() + ' - deleted'
                G.remove_arc(loop_arc)  
                return True
        return False                       
    
    def state_reduce(self,G,initial,prints=False):
        for b in G.S:
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
    
    def arc_reduce(self,G,initial,prints=False):
        profit = False
        for b in G.S:
            if len(b.O) == 0:
                continue
            if len(b.I) <= 1:
                continue        
            for a_ab in b.I:
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
            p1 = self.state_reduce(G,initial,prints)
            if not p1:
                p2 = self.loop_reduce(G,prints)
                if not p2:
                    p3 = self.arc_reduce(G, initial,prints)
                    if not p3:
                        break
            else:
                to_del =len(G.S)-G.absorbing_num
                if (to_del % 100 == 0):
                    print 'States to be reduced < ' + str(to_del)              
        print 'reduction complete'
        print 'reduced state number:'+str(len(G.S))
        return G


        