# NAME
#
#        C_CAE
#
# DESCRIPTION
#
#        The 'C_CAE' is the main definition class that creates 
#        a cellular automaton environment.
#
# HISTORY
#
# 16 December 2011
# o Initial development implementation.
#

from C_ggrid import *

class C_CAE:
        # 
        # Class member variables -- if declared here are shared
        # across all instances of this class
        #
        mdictErr = {
            'Keys'          : {
                'action'        : 'initializing base class, ', 
                'error'         : 'it seems that no member keys are defined.', 
                'exitCode'      : 10},
            'Save'              : {
                'action'        : 'attempting to pickle save self, ',
                'error'         : 'a PickleError occured',
                'exitCode'      : 12},
            'SaveMat'           : {
                'action'        : 'attempting to save MatLAB friendly spectrum, ',
                'error'         : 'an IOerror occured',
                'exitCode'      : 13},
            'Load'              : {
                'action'        : 'attempting to pickle load object, ',
                'error'         : 'a PickleError occured',
                'exitCode'      : 14}
        }
        
        #
        # Methods
        #
        # Core methods - construct, initialise, id
        
        def error_exit(         self,
                                astr_key,
                                ab_exitToOs = 1
                                ):
            print "%s:: FATAL ERROR" % self.mstr_obj
            print "\tSorry, some error seems to have occurred in <%s::%s>" \
                            % (self.__name__, self.mstr_def)
            print "\tWhile %s"  % C_spectrum.mdictErr[astr_key]['action']
            print "\t%s"        % C_spectrum.mdictErr[astr_key]['error']
            print ""
            if ab_exitToOs:
                    print "Returning to system with error code %d" % \
                                C_spectrum.mdictErr[astr_key]['exitCode']
                sys.exit(C_spectrum.mdictErr[astr_key]['exitCode'])
            return C_spectrum.mdictErr[astr_key]['exitCode']

        def fatal(self, astr_key, astr_extraMsg=""):
            if len(astr_extraMsg): print astr_extraMsg
            self.error_exit( astr_key)
        
        def warn(self, astr_key, astr_extraMsg=""):
            b_exitToOS  = 0
            if len(astr_extraMsg): print astr_extraMsg
            self.error_exit( astr_key, b_exitToOS)
            
        def __init__(self, *args):
            self.__name__       = 'C_CAE'
            self.mstr_obj       = 'C_CAE';      # name of object class
            self.mstr_name      = 'unnamed';    # name of object variable
            self.mstr_def       = 'void';       # name of function being processed
            self.m_id           = -1;           # int id
            self.m_iter         = 0;            # current iteration in an
                                                #+ arbitrary processing 
                                                #+ scheme
            self.m_verbosity    = 0;            # debug related value for 
                                                #+ object
            self.m_warnings     = 0;            # show warnings 
                                                #+ (and warnings level)

            # The core data containers are grids of cellular automata 
            # machines
            self.mgg_current    = None          # Currentt grid
            self.mgg_next       = None          # Next iteration grid
            
            
            # For the most part, the CAE accepts the same constuctor
            # pattern as the C_ggrid:
            if len(args) == 2:
                    self.mgg_current    = C_ggrid(args[0], args[1])
                    self.mgg_next       = C_ggrid(args[0], args[1])

            self.m_rows = self.mgg_current.rows_get()
            self.m_cols = self.mgg_current.cols_get()
                    
        def nextState_process(self):
            """
            The main control loop of the CAE. For each element in the
            current grid, determine a dictionary of neighbors, and
            send this dictionary to each CAM element. 
            
            Process the updates passed back from the CAM element.
            
            Primitive support for multithreaded/parallelization is also
            included.
            """
            for row in np.arange(0, self.m_rows):
                for col in np.arange(0, self.m_cols):
                    neighbors_dict(row, col)

