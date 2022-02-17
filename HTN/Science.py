
from pyhop_anytime import pyhop

from pyhop_anytime.pyhop import TaskList

stateOne = pyhop.State("stateOne")
stateOne.solutions = ['a','b','c','d']
stateOne.stations = ["hotplate", "stirrer", 'filter', 'table']
stateOne.machines = ['hotplate', 'stirrer', 'filter']
stateOne.located = {'a': "stirrer", 'b': 'hotplate', 'c': 'filter', 'd': 'table'}
stateOne.isOccupied = {'hotplate': True, 'Stirrer': True, "filter": True}
stateOne.boiled = {'a': False, 'b': False, 'c': False, 'd': False}
stateOne.stirred = {'a': False, 'b': False, 'c': False, 'd': False}
stateOne.filtered = {'a': False, 'b': False, 'c': True, 'd': False}


goalOne = pyhop.State("goalOne")
goalOne.solutions = ['a','b','c','d', 'bd']
goalOne.stations = ["hotplate", "stirrer", 'filter', 'table']
goalOne.machines = ['hotplate', 'stirrer', 'filter']
goalOne.located = {'a': "table", 'b': 'hotplate', 'c': 'table', 'd': 'table', 'bd': 'filter'}
goalOne.isOccupied = {'hotplate': True, 'Stirrer': False, "filter": True}
goalOne.boiled = {'a': True, 'b': False, 'c': True, 'd': False, 'bd': True}
goalOne.stirred = {'a': False, 'b': False, 'c': False, 'd': True, 'bd': False}
goalOne.filtered = {'a': True, 'b': False, 'c': True, 'd': True, 'bd': False}




stateTwo = pyhop.State("stateTwo")
stateTwo.solutions = ['a', 'b', 'c', 'd']
stateTwo.stations = ["hotplate", "stirrer", 'filter', 'table']
stateTwo.machines = ['hotplate', 'stirrer', 'filter']
stateTwo.located = {'a': "stirrer", 'b': 'hotplate', 'c': 'filter', 'd': 'table'}
stateTwo.isOccupied = {'hotplate': True, 'Stirrer': True, "filter": True}
stateTwo.boiled = {'a': False, 'b': False, 'c': False, 'd': False}
stateTwo.stirred = {'a': False, 'b': False, 'c': False, 'd': False}
stateTwo.filtered = {'a': False, 'b': False, 'c': True, 'd': False}


goalTwo = pyhop.State("goalTwo")
goalTwo.solutions = ['a', 'b', 'c', 'd', 'ab', 'abc']
goalTwo.stations = ["hotplate", "stirrer", 'filter', 'table']
goalTwo.machines = ['hotplate', 'stirrer', 'filter']
goalTwo.located = {'a': "table", 'b': 'hotplate', 'c': 'table', 'd': 'stirrer', 'ab': 'filter', 'abc': 'table'}
goalTwo.isOccupied = {'hotplate': True, 'Stirrer': True, "filter": True}
goalTwo.boiled = {'a': True, 'b': True, 'c': True, 'd': False, 'ab': True, 'abc': False}
goalTwo.stirred = {'a': True, 'b': True, 'c': False, 'd': True, 'ab': True, 'abc': True}
goalTwo.filtered = {'a': True, 'b': True, 'c': True, 'd': True, 'ab': False, 'abc': False}





#Operators

def Boil(state, solution):
    if solution in state.solutions and state.located[solution] == 'hotplate' and state.boiled[solution] == False:
        state.boiled[solution] = True
    return state

def Filter(state, solution):
    if solution in state.solutions and state.located[solution] == 'filter' and  state.filtered[solution] == False:
        state.filtered[solution] = True
    return state

def Stir(state, solution):
    if solution in state.solutions and state.located[solution] == 'stirrer' and state.stirred[solution] == False:
        state.stirred[solution] = True
    return state

def Mix(state, solution_one, solution_two):
    if solution_one in state.solutions and solution_two in state.solutions and solution_one != solution_two:
        if state.located[solution_one] == 'table' and state.located[solution_two] == 'table':
            if (solution_two + solution_one) not in state.solutions:
                new_solution = solution_one + solution_two
                state.solutions.append(new_solution)
                state.located[new_solution] = 'table'
                state.boiled[new_solution] = False
                state.filtered[new_solution] = False
                state.stirred[new_solution] = False
    return state

def Move(state, solution, location):

    if solution in state.solutions and location in state.stations and state.located[solution] != location:
        if (location != 'table' and state.isOccupied[location] == False):
            state.isOccupied[state.located[solution]] = False
            state.located[solution] = location
            state.isOccupied[location] = True

        elif location == 'table':
            state.isOccupied[state.located[solution]] = False
            state.located[solution] = location
    return state




#Helper function to see if state equals goal
def is_complete(state, goal, locationWorry):
    for solution in goal.solutions:
        if solution not in state.solutions:
            return False
        else:
            if locationWorry:
                if goal.located[solution] != state.located[solution]:
                    return False
            if goal.boiled[solution] != state.boiled[solution]:
                return False
            if goal.filtered[solution] != state.filtered[solution]:
                return False
            if goal.stirred[solution] != state.stirred[solution]:
                return False

    return True





# Methods

def start(state, goal):
    to_make = list(set(goal.solutions).difference(state.solutions))
    if is_complete(state, goal, True):
        return TaskList(completed=True)
    else:
        return TaskList([('make_solutions', to_make, goal), ('start', goal)])


def make_solutions(state, to_make, goal):
    if len(to_make) != 0:
        for solution in state.solutions:
            if state.located[solution] != 'table':
                return TaskList([('Move', solution, 'table')])
        return TaskList([('mixer', to_make)])
    else:

        return TaskList([[('doTask', solution, goal)] for solution in state.solutions])



def mixer(state, to_make):
    for i in range(len(state.solutions)):
        for j in range(len(state.solutions)):
            if state.solutions[i] + state.solutions[j] in to_make:
                return TaskList([('Mix', state.solutions[i], state.solutions[j])])




def doTask(state, solution, goal):

    if goal.boiled[solution]:
        if not state.boiled[solution]:
            return TaskList([('Move', solution, 'hotplate'), ('Boil', solution), ('Move', solution, 'table')])
    if goal.filtered[solution]:
        if not state.filtered[solution]:
            return TaskList([('Move', solution, 'filter'), ('Filter', solution), ('Move', solution, 'table')])
    if goal.stirred[solution]:
        if not state.stirred[solution]:
            return TaskList([('Move', solution, 'stirrer'), ('Stir', solution), ('Move', solution, 'table')])
    if is_complete(state, goal, False):
        if goal.located[solution] != state.located[solution]:
                return TaskList([('Move', solution, goal.located[solution])])



def make_solutions_planner():
    planner = pyhop.Planner()
    planner.declare_operators(Boil, Filter, Stir, Mix, Move)
    planner.declare_methods(doTask, mixer,make_solutions,start)
    choice = None
    while True:
        choice = input("StateOne or StateTwo? Enter '1' or '2'")
        if choice == '1' or choice == '2':
            break
    if choice == '1':
        print(planner.pyhop(stateOne, [('start', goalOne)], verbose = 3))
        print(planner.anyhop_stats(stateOne, [('start', goalOne)]))
    else:
        print(planner.pyhop(stateTwo, [('start', goalTwo)], verbose=3))
        print(planner.anyhop_stats(stateTwo, [('start', goalTwo)]))


if __name__ == '__main__':
    make_solutions_planner()














