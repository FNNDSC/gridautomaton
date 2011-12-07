#!/usr/bin/env python
# 
# NAME
#
#	Cgenome_drive.py
#
# DESCRIPTION
#
# 	A simple 'driver' for a C_genome class instance
#
# HISTORY
#
# 25 March 2011
# o Initial development implementation.
#

from    numpy           import *
from    C_ggrid         import *

Cglh    = C_ggrid('grids/pos-centroids-analyze-lh.K1.frontal.smoothwm.txt.grid')
Cgrh    = C_ggrid('grids/pos-centroids-analyze-rh.K1.frontal.smoothwm.txt.grid')

Cg1     = C_ggrid('grids/grid1.grid')
Cg2     = C_ggrid('grids/grid2.grid')


Cglhrh  = Cglh + Cgrh
Cg12    = Cg1 + Cg2 + Cg1 + Cg1

#print Cglh
#print Cgrh
#print Cglhrh

print Cg1
print Cg2
print Cg12

