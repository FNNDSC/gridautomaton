#!/usr/bin/env python

import systemMisc       as misc
import numpy            as np

misc.tic()
A1 = misc.neighbours_find(2,2, np.array((4,4)),
                              gridSize          = np.array((5,5)),
                              wrapGridEdges     = True,
                              returnUnion       = True)
misc.toc()
print A1

misc.tic()
A2 = misc.neighbours_findFast(2,2, np.array((4,4)),
                              gridSize          = np.array((5,5)),
                              wrapGridEdges     = True,
                              returnUnion       = True)
misc.toc()
print A2
