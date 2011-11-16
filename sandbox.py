'''
Created on Nov 16, 2011

@author: andrey
'''

import epf_epm as epm
import epf_epg as epg
import epf_viz as viz

S = epm.system("ABC System")
S.add_element('A', 0.1, 0.8, 0.0)
S.add_element('B', 0.15, 0.9, 0.0)
S.add_element('C', 0.05, 1.0, 1.0)
S.add_cf_arc('A', 'B', 0.5)
S.add_cf_arc('A', 'C', 0.5)
S.add_cf_arc('B', 'A', 0.9)
S.add_cf_arc('B', 'C', 0.1)
S.add_df_arc('A', 'B')
S.add_cf_arc('B', 'C')

V = viz.viz()
V.draw_epm(S)

G = epg.EPG()
G.generate(S)

V.draw_epg(G)


