from ctypes.macholib.dyld import test_dyld_find

from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    # Add your forward checking logic here.
    X = state.get_current_variable()
    x = None
    if X is not None:
        x = X.get_assigned_value()
        constraints = state.get_constraints_by_name(X.get_name())
        for constraint in constraints:
            i = constraint.get_variable_i_name()
            j = constraint.get_variable_j_name()

            if X.get_name() == i:
                Y = state.get_variable_by_name(j)
            else:
                Y = state.get_variable_by_name(i)

            for y in Y.get_domain():
                current_assignments = {X.get_name(): x, Y.get_name(): y}

                if not constraint.check(state, current_assignments[i], current_assignments[j]):
                    Y.reduce_domain(y)

            if Y.domain_size() == 0:
                return False

        return True
    else:
        return True

# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False

    # Add your propagate singleton logic here.
    singleton_var_queue = [var for var in state.get_all_variables() if var.domain_size() == 1]
    visited_singletons = set()

    while singleton_var_queue :
        X = singleton_var_queue.pop(0)
        if X in visited_singletons:
            continue
        visited_singletons.add(X)

        x = X.get_domain()

        constraints = state.get_constraints_by_name(X.get_name())
        for constraint in constraints:
            i = constraint.get_variable_i_name()
            j = constraint.get_variable_j_name()

            if X.get_name() == i:
                Y = state.get_variable_by_name(j)
            else:
                Y = state.get_variable_by_name(i)

            if Y.is_assigned():
                continue

            for y in Y.get_domain():
                current_assignments = {X.get_name(): x, Y.get_name(): y}

                if not constraint.check(state, current_assignments[i], current_assignments[j]):
                    Y.reduce_domain(y)

            if Y.domain_size() == 0:
                return False

        for unvisited_singleton in state.get_all_variables():
            if not unvisited_singleton.is_assigned() and unvisited_singleton.domain_size() == 1:
                if unvisited_singleton not in visited_singletons and unvisited_singleton not in singleton_var_queue:
                    singleton_var_queue.append(unvisited_singleton)
    return True


## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    assert isinstance(list1, list)
    assert isinstance(list2, list)
    dist = 0

    for item1, item2 in zip(list1, list2):
        dist += (item1 - item2)**2

    return dist ** 0.5

#Once you have implemented euclidean_distance, you can check the results:
#evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(euclidean_distance, 5)
evaluate(my_classifier, senate_group1, senate_group2, verbose=0)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    def get_entropy(group):
        n_group = len(group)
        if n_group == 0:
            return 0

        counts = [
            group.count("Democrat"),
            group.count("Republican"),
            group.count("Independent")
        ]

        entropy = 0
        for count in counts:
            if count > 0:
                p = float(count) / n_group
                entropy -= p * (math.log(p) / math.log(2))
        return entropy

    n_tot = len(yes) + len(no)
    if n_tot == 0:
        return 0

    p_yes = float(len(yes)) / n_tot
    p_no = float(len(no)) / n_tot

    return p_yes * get_entropy(yes) + p_no * get_entropy(no)

#print CongressIDTree(senate_people, senate_votes, information_disorder)
#evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print
        
    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

                                   
## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 27
#rep_classified = limited_house_classifier(house_people, house_votes, N_1)

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 100
#senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 100
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)


## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

    
