# NAME
#
#	C_ggrid
#
# DESCRIPTION
#
#	'C_ggrid' is the atom class that process group-based
#        2D positional grids.
#
#
# HISTORY
#
# 31 March 2011
# o Initial development implementation.
#

# System imports
import 	os
import 	os.path
import 	sys
import	string
import	types
import	itertools

import	systemMisc	as misc
import 	numpy 		as np

import 	cPickle		as pickle

from 	C_spectrum	import *

class C_ggrid :
	# 
	# Class generic variables: shared across all instances
	# of this class:
	#
        mdictErr = {
	    'ReadGrid'          : {
	        'action'        : 'attempting to read grid file, ', 
	        'error'         : 'I could not access the file', 
	        'exitCode'      : 10},
	    'Operands'          : {
	        'action'        : 'checking operands, ',
	        'error'         : 'internal grids are not the same size',
	        'exitCode'      : 11},
	    'Save'              : {
	        'action'        : 'attempting to pickle save self, ',
	        'error'         : 'a PickleError occured',
	        'exitCode'      : 12},
	    'Load'              : {
	        'action'        : 'attempting to pickle load object, ',
	        'error'         : 'a PickleError occured',
	        'exitCode'      : 13}
	}
        
	#
	# Methods
	#
	# Core methods - construct, initialise, id
	
	def error_exit(		self,
				astr_key,
				ab_exitToOs = 1
				):
	    print "%s:: FATAL ERROR" % self.mstr_obj
	    print "\tSorry, some error seems to have occurred in <%s::%s>" \
	    		% (self.__name__, self.mstr_def)
	    print "\tWhile %s" 		% C_ggrid.mdictErr[astr_key]['action']
	    print "\t%s"		% C_ggrid.mdictErr[astr_key]['error']
	    print ""
	    if ab_exitToOs:
	    	print "Returning to system with error code %d" % \
	    				  C_ggrid.mdictErr[astr_key]['exitCode']
	        sys.exit(C_ggrid.mdictErr[astr_key]['exitCode'])
	    return C_ggrid.mdictErr[astr_key]['exitCode']

	def fatal(astr_key, astr_extraMsg=""):
	    if len(astr_extraMsg): print astr_extraMsg
	    self.error_exit( astr_key)
	
	def warn(astr_key, astr_extraMsg=""):
	    b_exitToOS  = 0
	    if len(astr_extraMsg): print astr_extraMsg
	    self.error_exit( astr_key, b_exitToOS)
	    
	def core_construct(	self,
				astr_obj	= 'C_ggrid',
				astr_name	= 'void',
				a_id		= -1,
				a_iter		= 0,
				a_verbosity	= 0,
				a_warnings	= 0) :
		self.mstr_obj		= astr_obj
		self.mstr_name		= astr_name
		self.m_id		= a_id
		self.m_iter		= a_iter
		self.m_verbosity	= a_verbosity
		self.m_warnings		= a_warnings
		
	def __init__(self, *args):
	    self.__name__ 	= "C_ggrid"
	    self.mstr_obj	= 'C_ggrid';	# name of object class
            self.mstr_name	= 'unnamed';	# name of object variable
	    self.mstr_def	= 'void';	# name of function being processed
            self.m_id		= -1; 		# int id
            self.m_iter		= 0;		# current iteration in an
                                		#+ arbitrary processing 
						#+ scheme
            self.m_verbosity	= 0;		# debug related value for 
						#+ object
            self.m_warnings	= 0;            # show warnings 
						#+ (and warnings level)
	    self.mstr_gridFileName = ""		# file containing numeric grid	
	    self.ma_grid       	= None		# array grid
	    self.macs_grid	= None		# grid of spectrum types
	    self.m_rows		= 0
	    self.m_cols		= 0
	    
	    if len(args):
		    c = args[0]
		    if type(c) is types.StringType:
		    	self.mstr_gridFileName = c
	                try:
	                   self.ma_grid = np.genfromtxt(self.mstr_gridFileName)
	                except IOError: self.fatal('ReadGrid')
	            if type(c).__name__ == 'ndarray':
	           	self.ma_grid = c
	            if type(c) is types.IntType:
	            	# If constructed with single int, create
	            	# zeroes grid of [c x c] 
	            	self.ma_grid = np.zeros( (c, c) )
	            self.internalsFromArr_init()
	            
        def rows_get(self):
            return self.m_rows
           
        def cols_get(self):
            return self.m_cols

        def spectrumDefaults_set(self, row, col):
            """
            	Sets some generic defaults for passed spectrum
            """
            self.macs_grid[row, col].name_set('(%d, %d)' % (row, col))
            self.macs_grid[row, col].printAsRow_set(True)
            self.macs_grid[row, col].printConcise_set(True)
            self.macs_grid[row, col].printColWidth_set(15)

	def internalsFromArr_init(self):
	    """
	    	(re)construct the internals of the class based
	    	on the internal ma_grid.
	    	
	    	PRECONDITIONS:
	    	o self.ma_grid MUST be valid <ndarray>
	    """
	    l_dim           = self.ma_grid.shape;
	    self.m_rows     = l_dim[0]
	    self.m_cols     = l_dim[1]
	    self.macs_grid  = np.zeros( (self.m_rows, self.m_cols), 
					dtype = 'object')
	    for row in np.arange(0, self.m_rows):
		for col in np.arange(0, self.m_cols):
		    spectrumComponent = int(self.ma_grid[row, col])
		    self.macs_grid[row, col] = \
			    C_spectrum_color(spectrumComponent)
		    self.spectrumDefaults_set(row, col)
	    self.core_construct()
                            
	def core_print(self):
		str = ""
		str+= 'mstr_sobj\t\t= %s\n' 	% self.mstr_obj
		str+= 'mstr_name\t\t= %s\n' 	% self.mstr_name
		str+= 'm_id\t\t\t= %d\n' 	% self.m_id
		str+= 'm_iter\t\t\t= %d\n'	% self.m_iter
		str+= 'm_verbosity\t\t= %d\n'	% self.m_verbosity
		str+= 'm_warnings\t\t= %d\n'	% self.m_warnings
		return str

	def __str__(self):
	    str = ""
	    str+= 'Raw grid:\n'
	    str+= '%s\n\n' % np.array_str(self.ma_grid)
	    for row in np.arange(0, self.m_rows):
	    	for col in np.arange(0, self.m_cols):
	    	    str += "%s" % self.macs_grid[row, col]
	    	str += "\n"   
	    return str

	def gridarr_get(self):
	    """
	    	Return the internal ma_grid
	    """
	    return self.ma_grid

    	def __add__(self, cg):
    	    """
    	    	Adds two grids together, returning the result as a new
    	    	grid. For each grid cell (which contains a spectrum)
    	    	a new spectrum is created which is the sum of the 
    	    	constituent spectra.
    	    """
    	    if self.ma_grid.shape != cg.ma_grid.shape: 
    	    	self.fatal('Operands')
    	    C_add = C_ggrid(self.m_rows)
    	    C_add.ma_grid = self.ma_grid + cg.ma_grid
	    for row in np.arange(0, self.m_rows):
		for col in np.arange(0, self.m_cols):
		    spectrum_self = self.macs_grid[row, col]
		    spectrum_cg   = cg.macs_grid[row, col]
		    C_add.macs_grid[row, col] = spectrum_self + spectrum_cg
		    C_add.spectrumDefaults_set(row, col)
    	    return C_add
	
	def save(self, astr_fileName):
	    """
	    	Saves the object to file using 'pickle'
	    """
	    try:
	    	pickle.dump(self, astr_fileName)
	    except PickleError: self.fatal('Save')
	    
	def load(self, astr_fileName):
	    """
	    	Load the object from file using 'pickle'. Overwrite
	    	current internals.
	    """
	    try:
	    	self = pickle.load(self, open(astr_fileName))
	    except PickleError: self.fatal('Load')
