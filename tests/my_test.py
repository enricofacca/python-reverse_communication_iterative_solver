import sys
import os
from copy import deepcopy as cp

from reverse_communication_iterative_solver.rcis import *

#sys.path.append(os.path.abspath(
#    '../src/reverse_communication_iterative_solver/'))
    
#from rcis import *



class Real(Unknows):
    """
    We extend the Unknows class.
    We add a method for saving the data to file. 
    """
    def __init__(self,x0):
        """
        Constructor setting initial solution
        """
        self.NumberOfUnknows=1
        self.x=x0
        self.time=0.0
        self.iteration=0
    def Save(self,file):
        """
        Procedure for saving to file
        """        
        f.open(file,'w')
        f.write(self.x)
        f.close()
        return info;

class Parabola(Problem):
    """
    Problem inputs with the coefficient of the parabola
    y=a*x^2/2
    """
    def __init__(self,a,lb=-1e30,up=1e30):
        self.a=a
        self.lower_bound=lb
        self.upper_bound=up


class GradientDescentControls:
    """
    Class with gradient decent controls. 
    
    """
    def __init__(self,
                 step0=0.1,
                 verbose=0):
        """
        Step Length
        """
        # step length
        self.step=step0

        # info solver application
        self.verbose=0

class InfoDescent:
    def __init__(self):
        self.cpu_gradient=0.0

class ParabolaDescent(ConstrainedSolver): 
    """
    We extend the class "Solver"
    ovverriding the "syncronize" and the "update"
    procedure. 
    """
    def __init__(self, ctrl=None):
        """
        Initialize solver with passed controls (or default)
        and initialize structure to store info on solver application
        """
        # init controls
        if ( ctrl==None):
            self.ctrl=GradientDescentControls(0.1)
        else:
            self.ctrl=cp(ctrl)
        # init infos
        self.infos=InfoDescent()
            
    def syncronize(self, problem, unknows):
        """
        Since the there are no constrain
        the first procedure does nothing.
        """

        # example of how the setup of our problem
        # can influence solver execution
        if ( unknows.x>=problem.lower_bound and unknows.x<=problem.upper_bound) :
            ierr=0
        else:
            ierr=-1
            
        return unknows,ierr,self;

    def update(self, problem, unknows):
        """
        The update is one step of gradient descent.
        Currently with explicit euler.
        """
        start_time = cputiming.time() 
        gradient_direction=-problem.a*unknows.x
        self.infos.cpu_gradient=cputiming.time()-start_time+unknows.iteration
        
        unknows.x=unknows.x+self.ctrl.step*gradient_direction
        unknows.time+=self.ctrl.step
        
        # example of how the setup of our problem
        # can influence solver execution
        if ( unknows.x>=problem.lower_bound and unknows.x<=problem.upper_bound) :
            ierr=0
        else:
            ierr=-1

        self.test=unknows.x
        
        return unknows,ierr,self;

def test_main():
    # init solution container and copy it
    sol=Real(1)


    # init inputs data
    data=Parabola(0.5)


    # init solver
    ctrl=GradientDescentControls(0.5)
    gradient_descent=ParabolaDescent(ctrl)

    # init update cycle controls
    flags=CycleControls(100,verbose=0)

    # list to store 
    sol_old=cp(sol)
    hystory=[]
    while(flags.flag >=0):
        ###################################################
        # Call reverse communication.
        # Then select action according to flag.flag and flag.info
        ######################################################
        flags, sol, gradient_descent=flags.reverse_communication_constrained_solver(
            gradient_descent,
            data,
            sol)
    
        # set problem inputs and controls before update 
        if (flags.flag == 2) and (flags.info==0) :
            #print('time to fix inputs and controls '+
            #      'for next update')
            
            # copy data before update
            sol_old.x=cp(sol.x)
            
        ###################################################
        # set inputs and reset controls due to failure
        ###################################################
        if (flags.flag == 2) and not (flags.info==0) :
            #########################################################
            # Do what ever you want of with the data
            # without modyfyng them
            ########################################################
            pass
        if ( flags.flag == 3):
            #print('time study the system')
            #print('sol=', sol.x,'energy=',data.a*sol.x**2/2.0)
            #print('iter=',flags.iterations)
            sol.iteration=cp(flags.iterations)
            hystory.append([sol.time,cp(gradient_descent.infos)])
        
        
        #######################################################
        # Define you stop criteria and set flags.flag=-1
        # to exit from the cycle. Set flags.info=0
        # if you reached your scope. 
        ########################################################
        if ( flags.flag == 4):
            # evalute system variation
            var=abs(sol.x-sol_old.x)/gradient_descent.ctrl.step
            #print( 'var=',var,'old=',sol_old.x,'new',sol.x)
            # break cycle if convergence is achieved 
            if ( var < 1e-4):
                flags.flag=-1
                flags.info=0
        
    assert (abs(sol.x)<1e-3) 

if __name__ == "__main__":
    sys.exit(test_main())
