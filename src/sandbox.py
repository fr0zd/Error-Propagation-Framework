'''
Created on Nov 16, 2011

@author: andrey
'''

import epm

S = epm.system("ABC System")
S.add_element('A', 0.1, 1, 0.0)
S.add_element('B', 0.0, 1, 0.8, 'FS')
S.add_element('C', 0.0, 0.0, 0.0)
S.add_cf_arc('A', 'B', 0.5)
S.add_cf_arc('A', 'C', 0.5)
S.add_cf_arc('B', 'A', 0.9)
S.add_cf_arc('B', 'C', 0.1)
S.add_df_arc('A', 'B')
S.add_df_arc('B', 'C')

import viz

V = viz.viz()
V.draw_epm(S)

import epg
G = epg.graph()
G.generate(S)

import epa
A = epa.analyzer()
A.iter_compute(G,0.001)
G.print_results(100)
A.direct_compute(G)
G.print_results(100)
V.draw_epg(G)


A.reduce(G, 10)
V.draw_epg(G,'reduced_EPG')
