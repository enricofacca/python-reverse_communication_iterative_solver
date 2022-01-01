"""
Python module defining a template for iterative algorithm,
which means algorithm that incrementaly approach the 
solution of a problem. In this project this
increment is called "update".

We decompose this kind of algorithms into 4 main steps
where the user has a specific task:
1 - set the solver controls ( and eventuality problem inputs)
    before the next update. 
2 - reset the solver controls (and eventuality reset problem inputs)
    after a solver failure 
3 - study any quantity defined by the problem, unknows, and solver
4 - set when the solver has finished its job.

This decomposition is done via a Reverse Communication (RC) 
approach, an old style of programming (used for 
example in the ARPACK library). While Python is so flexible 
that other approaches could have been used, we adopt it
because it let the user work "manually" on the structures
describing its problem instead of having to define in advance 
the procedure to handle the steps 1,2,3,4.

This is particularly convient in early step of
the algorithm development. A nicer and clenear 
function hiding the RC cycle to an user who 
wants a block-box solver can be easily build.

Algorithm and problem descricing are separate 
with Object Orientied programming style 
introducing 3 (+1) classes:

Problem: A class that should describe the problem we want to solve
Unknows: A class describing the solution of the problem

These two class are left empty, see simple_example.py to have a
concrete example.

Solver: An abstract class containg the abstact procedure "update"
acticing on unknows with the class problem

ConstrainedSolver: An abstract class extending the Solver class (so
also the procudure "update" is included) with a procudere "syncronize"
to transform the unknows so that some problem constraints are
satissfied.


"""
from abc import ABC, abstractmethod
import time as cputiming


class Solver(ABC): 
    """
    Abstract procedure describing the update action of the 
    solver on the unknows.

    Args:
    problem : class describing problem setup
    unknows : class describing problem solution

    Return:
    unknows : update solution after one update
    ierr    : integer ==0 if no error occurred.
              Values different from 0 are used to
              identifity the error occured
    self    : solver class. We return the solver
              to read statistic of the last update.
    """
    @abstractmethod
    def update(self, problem, unknows):
        return unknows, ierr, self  


class ConstrainedSolver(ABC): 
    """
    Abstract procedure describing the solver syncronizing i.e.,
    action of the solver on the problem unknows so they fit 
    into potential problem constraints. 
    
    Args:
    problem : class describing problem setup
    unknows : class describing problem solution

    Return:
    unknows : update solution after one update
    ierr    : integer ==0 if no error occurred.
              Values different from 0 are used to
              identifity the error occured
    self    : solver class. We return the solver
              to read statistic.
    """
    @abstractmethod
    def syncronize(self, problem, unknows):
        return unknows, ierr, self  


# Two (empty) abstact classes that will contain
# respectively problem unknows and inputs.
# They will both contain only pure data (like integer, real,complex).
# Unknows will store for example the coefficient of the
# solution of a PDE.
# Inputs will contain the coefficient of the forcing term in a PDE.
class Unknows(ABC):
    """
    Empty class used to fixed the name of unknows class
    """
    NumberOfUnknows = 0

    
class Problem(ABC):
    """
    Empty class used ot fixed the name
    """
    NumberOfInputs = 0
    
    
class CycleControls():
    """
    Reverse communication controls and info.
    (Here we keep controls and info togheter for having just one class)
    """
    def __init__(self,
                 max_iterations=100,
                 max_restart_update=10,
                 verbose=0):
        # State variable of iteration
        # Order comunication flag 
        self.flag = 0
        # State comunication flag
        self.info = 0
        # Update counter
        self.iterations = 0
        # Restart counter
        self.nrestart_update = 0
                
        # Controls of iterative algorithm
        # maximum number of updates
        self.max_iterations = max_iterations
        # maximum number of restart
        self.max_restart_update = max_restart_update
        # verbose
        self.verbose = verbose
        
        # Statistics of iterative algorithm
        # Cpu conter
        self.cpu_time = 0
        
    def reverse_communication_solver(self, solver, problem, unknows):
        """ 
        Subroutine to run reverse communition approach 
        of iterative solver.
        
        Args:
        solver(inout): class(Solver) with method syncronize and update
        ctrls (in   ): Solver controls
        dmkin (in   ): class(Problem) containg current realization of problem
        unknows (inout): Problem unknows
        """
    
        if (self.flag == 0):
            # study system
            self.flag = 3
            self.ierr = 0                
            return self, unknows, solver
    
        if (self.flag == 2):
            # user has settled problem inputs and controls
            # now we update
            self.ierr = 0
            
            # Update cycle. 
            # If it succees goes to the evaluation of
            # system varaition (flag ==4 ).
            # In case of failure, reset controls
            # and ask new problem inputs or ask the user to
            # reset controls (flag == 2 + ierr=-1 ).
            if (self.nrestart_update == 0):
                if (self.verbose == 1):
                    print(' ')
                    print('UPDATE ' + str(self.iterations))
                cpu_update = 0.0
            else:
                if (self.verbose >= 1):
                    print(
                        'UPDATE ' +
                        str(self.time_iterations + 1) +
                        ' | RESTART = ' +
                        str(self.nrestart_update)
                    )
            #
            # update unknows
            #
            start_time = cputiming.time()
            [unknows, ierr, solver] = solver.update(problem, unknows)
            cpu_update += cputiming.time() - start_time
        
            #
            # check for successfulls update
            #
            if (ierr == 0):
                # info for succesfull update
                self.iterations += 1
                self.cpu_time += cputiming.time() - start_time
                if (self.verbose >= 1):
                    if (self.nrestart_update == 0):
                        print(
                            'UPDATE SUCCEED CPU =' + 
                            '{:.2f}'.format(cpu_update)
                        )
                    else:
                        print('UPDATE SUCCEED ' +
                              str(self.nrestart_update) +
                              ' RESTARTS CPU =' +
                              '{:.2f}'.format(cpu_update))
                        print(' ')
                #
                # Ask to the user to evalute if stop cycling 
                # 
                # 
                self.flag = 4 
                self.ierr = 0 
            else:
                #
                # update failed
                #
                if (self.verbose >= 1):
                    print('UPDATE FAILURE')
            
                # try one restart more
                self.nrestart_update += 1
            
                # stop if number max restart update is passed 
                if (self.nrestart_update >= self.max_restart_update):
                    self.flag = -1   # breaks cycle
                    self.ierr = -1   # signal error
                else:
                    # ask the user to reset controls and problem inputs
                    self.flag = 2
                    self.ierr = -1
            return self, unknows, solver
       
        if (self.flag == 3):
            # check if maximum number iterations was achieded 
            if (self.iterations >= self.max_iterations):
                self.flag = -1
                self.ierr = -1
                if (self.verbose >= 1):
                    print(' Update Number exceed limits' +
                          str(self.max_iterations))
                # break cycle
                return self, unknows, solver

            # New update is required thus
            # ask for new controls
            unknows.nrestart_update = 0  # we reset the count of restart
            self.flag = 2
            self.ierr = 0
            return self, unknows, solver

        if (self.flag == 4):
            # ask user new problem inputs in order to update 
            self.flag = 3
            self.ierr = 0
            return self, unknows, solver
       
    def reverse_communication_constrained_solver(self,
                                                 solver,
                                                 problem,
                                                 unknows):
        """
        Subroutine to run reverse communition approach 
        of constrained solver.
        
        Args:
        solver(inout): class(Solver) with method syncronize and update
        ctrls (in   ): Solver controls
        dmkin (in   ): class(Problem) containg current realization of problem
        unknows (inout): Problem unknows
        infos (inout): Solver statistics and info
        """
    
        if (self.flag == 0):
            # syncronize
            start_time = cputiming.time()            
            [unknows, ierr, solver] = solver.syncronize(problem, unknows)
            syncr_time = cputiming.time() - start_time
            self.cpu_time += syncr_time

            if (self.verbose >= 1):
                print('SYNCRONIZE AT TIME: CPU' +
                      '{:.2f}'.format(syncr_time))
            if (ierr == 0):
                # study system
                self.flag = 3
                self.ierr = 0
            else:
                self.flag = -2
                self.ierr = 0
                
            return self, unknows, solver
    
        if (self.flag == 2):
            # user has settled problem inputs and controls
            # now we update
            self.ierr = 0
            
            # Update cycle. 
            # If it succees goes to the evaluation of
            # system varaition (flag ==4 ).
            # In case of failure, reset controls
            # and ask new problem inputs or ask the user to
            # reset controls (flag == 2 + ierr=-1 ).
        
            if (self.nrestart_update == 0):
                if (self.verbose >= 1):
                    print(' ')
                    print('UPDATE ' + str(self.iterations))
                cpu_update = 0.0
            else:
                print('UPDATE ' +
                      str(self.time_iterations + 1) +
                      ' | RESTART = ' +
                      str(self.nrestart_update))
            #
            # update unknows
            #
            start_time = cputiming.time()
            [unknows, ierr, solver] = solver.update(problem, unknows)
            cpu_update += cputiming.time() - start_time
        
            #
            # check for successfulls update
            #
            if (ierr == 0):
                # info for succesfull update
                self.iterations += 1
                self.cpu_time += cputiming.time() - start_time
                if (self.verbose >= 1):                    
                    if (self.nrestart_update == 0):
                        print(
                            'UPDATE SUCCEED CPU = ' + 
                            '{:.2f}'.format(cpu_update)
                        )
                    else:
                        print(
                            'UPDATE SUCCEED ' +
                            str(self.nrestart_update) +
                            ' RESTARTS CPU =' +
                            '{:.2f}'.format(cpu_update)
                        )
                        print(' ')
                #
                # Ask to the user to evalute if stop cycling 
                # 
                # 
                self.flag = 4 
                self.ierr = 0 
            else:
                #
                # update failed
                #
                print('UPDATE FAILURE')
            
                # try one restart more
                self.nrestart_update += 1
            
                # stop if number max restart update is passed 
                if (self.nrestart_update >= self.max_restart_update):
                    self.flag = -1  # breaking cycle
                    self.ierr = -1 
                else:
                    # ask the user to reset controls and problem inputs
                    self.flag = 2
                    self.ierr = -1
            return self, unknows, solver
       
        if (self.flag == 3):
            # check if maximum number iterations was achieded 
            if (self.iterations >= self.max_iterations):
                self.flag = -1
                self.ierr = -1
                if (self.verbose >= 1):
                    print(
                        'Update Number exceed limits' + 
                        str(self.max_iterations)
                    )
                # break cycle
                return self, unknows, solver

            # New update is required thus
            # ask for new controls
            unknows.nrestart_update = 0  # we reset the count of restart
            self.flag = 2
            self.ierr = 0
            return self, unknows, solver

        if (self.flag == 4):
            # ask user new problem inputs in order to update 
            self.flag = 3
            self.ierr = 0
            return self, unknows, solver

        
        
