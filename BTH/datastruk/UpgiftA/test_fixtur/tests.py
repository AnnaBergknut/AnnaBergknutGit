"""
Written by Christian Nordahl, October 2022, cno@bth.se
Inspired by version of Carina Nilsson, March 2022, cnl@bth.se
"""

try:
    from sorting import insertionsort
except:
    print("Error importing insertionsort. Please make sure the function insertionsort(lst: list) is available in the sorting module.")
try:
    from sorting import quicksort
except:
    print("Error importing quicksort. Please make sure the function quicksort(lst: list) is available in the sorting module.")
try:
    from sorting import mergesort
except:
    print("Error importing mergesort. Please make sure the function mergesort(lst: list) is available in the sorting module.")
try:
    from sorting import quicksort_hybrid
except:
    print("Error importing quicksort_hybrid. Please make sure the function quicksort_hybrid(lst: list) is available in the sorting module.")
try:
    from sorting import mergesort_hybrid
except:
    print("Error importing mergesort_hybrid. Please make sure the function mergesort_hybrid(lst: list) is available in the sorting module.")



import os
import sys
import ast
import time
import inspect
import logging
import pylint.lint
import numpy as np
from inspect import signature


LOG_LEVEL = 'INFO' 
LINT_THRESHOLD = 8.0
TEST_DATA = ['100_random.txt', '1000_random.txt']
INITIAL_TIME_LIMIT = 0.5

FUNCTION_NAMES = ['insertionsort','quicksort', 'mergesort']
FUNCTIONS = [insertionsort, quicksort, mergesort]
LIMITS = [(40,400),(6,20),(6,20)]

FUNCTION_NAMES = ['insertionsort','quicksort', 'mergesort', 'quicksort_hybrid', 'mergesort_hybrid'] # Comment out this if you only want to test the first three algorithms.
FUNCTIONS = [insertionsort, quicksort, mergesort, quicksort_hybrid, mergesort_hybrid]               # Comment out this if you only want to test the first three algorithms.
LIMITS = [(40,400),(6,20),(6,20),(6,20),(6,20)]


version = sys.version_info
if version[0] < 3 :
    print(f'Please install python 3, at least version 3.6. You have {version[0]}.{version[1]}.')
    sys.exit(1)
elif version[1] < 6:
    print(f'Please install python 3, at least version 3.6. You have {version[0]}.{version[1]}.')
    sys.exit(1)

# A wrapper to check if there is an explicit return statement in a function.
def contains_explicit_return(f):
    return any(isinstance(node, ast.Return) for node in ast.walk(ast.parse(inspect.getsource(f))))

def check_function_definitions():
    # Test if functions exist
    print(f'\nTesting if the required functions are implemented and correctly defined.')
    log.info(f'\nTesting if the required functions are implemented and correctly defined.')
    for func_name in FUNCTION_NAMES:
        if func_name not in globals():
            print(f'Test failed!\nThe function {func_name}() is missing.')
            log.info(f'Test failed!\nThe function {func_name}() is missing.')
            sys.exit(1)
    print('All functions OK!\n')
    log.info('All functions OK!\n')
    
    # Test if functions have correct parameters
    for func, func_name in zip(FUNCTIONS, FUNCTION_NAMES):
        if str(signature(func)) != "(lst: list) -> None":
            print(f'Please use the same signature as defined in the assignment.It should be:\n{func_name}(lst: list) -> None')
            log.info(f'Please use the same signature as defined in the assignment.It should be:\n{func_name}(lst: list) -> None')
            sys.exit(1)

    # Test if functions returns None
    lst = [1]
    for func, func_name in zip(FUNCTIONS, FUNCTION_NAMES):
        if contains_explicit_return(func):
            print(f'{func_name} should not have any return statement. Remove it.')
            log.info(f'{func_name} should not have any return statement. Remove it.')
            sys.exit(1)

def check_sorting_function(func, func_name):
    empty = []
    func(empty)
    if empty:
        print(f'Error: \nEmpty list is not handled correctly.')
        log.info(f'Error: \nEmpty list is not handled correctly.')
        sys.exit()
    
    one = [1]
    func(one)
    if one != [1]:
        print(f'Error: \n Lists with only one element is not handled correctly.')
        log.info(f'Error: \n Lists with only one element is not handled correctly.')
        sys.exit(1)

    input_list = np.random.randint(-1000, 1000, size=1000).tolist()
    input_copy = input_list[:]
    func(input_list)
    for i in range(0, len(input_list)-1):
        if input_list[i+1] < input_list[i]:
            print('Test failed! Sortorder corrupt.')
            log.info('Test failed! Sortorder corrupt.')
            sys.exit(1)
    for item in input_copy:
        if (input_list.count(item) != input_copy.count(item)) or len(input_list) != len(input_copy):
            print('Test failed! ELements are missing and/or duplicated.')
            log.info('Test failed! ELements are missing and/or duplicated.')
            sys.exit(1)

def check_sorting_functionality():
    print('Testing basic sorting functionality.')
    for func, func_name in zip(FUNCTIONS, FUNCTION_NAMES):
        print(f'  {func_name}...', end="")
        log.info(f'  {func_name}...')
        check_sorting_function(func, func_name)

        tabs = (len(func_name)-1)//4
        for i in range(tabs, 4):
            print('\t', end="")
        print('OK!')
    print('Basic sorting testing OK!\n')
    log.info('Basic sorting testing OK!\n')

def check_sorting_performance():
    print('Testing run time.')
    log.info('Testing run time.')
    for func, func_name in zip(FUNCTIONS, FUNCTION_NAMES):
        print(f'  {func_name}... ', end="")
        log.info(f'  {func_name}... ')
        for test_file in TEST_DATA:
            with open('Testdata/'+test_file, 'r', encoding='UTF-8') as file:
                num_list = list(map(int, file.readlines()))
                timestamp_before = time.perf_counter()
                func(num_list)
                timestamp_after = time.perf_counter()
                runtime = timestamp_after - timestamp_before
                print(runtime)

                if runtime > INITIAL_TIME_LIMIT:
                    tabs = (len(func_name)-1)//4
                    for i in range(tabs, 4):
                        print('\t', end="")
                    print(' FAILED! Algorithm sorts too slow.')
                    log.info(' FAILED! Algorithm sorts too slow.')
                    sys.exit(1)

        tabs = (len(func_name)-1)//4
        for i in range(tabs, 4):
            print('\t', end="")
        print('OK!')
    print('Run time tests OK!\n')
    log.info('Run time tests OK!')

def check_sorting_complexity():
    TEST_DATA.append('10000_random.txt')

    print('Testing time complexity.')
    log.info('Testing time complexity.')
    for func, func_name,limit in zip(FUNCTIONS, FUNCTION_NAMES, LIMITS):
        print(f'  {func_name}... ', end="")
        log.info(f'  {func_name}... ')
        runtimes = []
        for test_file in TEST_DATA:
            with open('Testdata/'+test_file, 'r', encoding='UTF-8') as file:
                num_list = list(map(int, file.readlines()))
                timestamp_before = time.perf_counter()
                func(num_list)
                timestamp_after = time.perf_counter()
                runtimes.append(timestamp_after - timestamp_before)

        for i in range(len(runtimes)-1):
            tabs = (len(func_name)-1)//4
            scaling = runtimes[i+1]/runtimes[i]
            if not (limit[0] < scaling < limit[1]):
                for i in range(tabs, 4):
                    print('\t', end="")
                print(f' FAILED! Algorithm does not follow its defined time complexity. {scaling}')
                log.info(' FAILED! Algorithm does not follow its defined time complexity.')
                sys.exit(1)

        tabs = (len(func_name)-1)//4
        for i in range(tabs, 4):
            print('\t', end="")
        print('OK!')
    print('Time complexity tests OK!\n')
    log.info('Time complexity tests OK!')

def check_code_quality():
    print(f'\nChecking code quality by pylint score, {LINT_THRESHOLD} is minimum to pass ...')
    log.info(f'Checking code quality by pylint score, {LINT_THRESHOLD} is minimum to pass')
    stdout = sys.stdout
    outfile = open('pylint_report.txt', 'w')

    sys.stdout = outfile
    run = pylint.lint.Run(
        ['sorting.py'], exit=False)
    try:    # Linting for Codegrades python version (3.6)
        score = run.linter.stats['global_note']
    except: # Linting for my python version (3.10)
        score = run.linter.stats.global_note
    if score < LINT_THRESHOLD:
        log.info(f'  The pylint score is only {score:.2f}, at least {LINT_THRESHOLD} required')
        sys.stdout = stdout
        outfile.close()
        print(
            f'  Test failed!\nThe pylint score is only {score:.2f}, ' +
            f'  at least {LINT_THRESHOLD} required')
        print('Detailed report can be viewed in pylint_report.txt\n')
        log.info('Detailed report can be viewed in pylint_report.txt\n')
        sys.exit(1)
    else:
        sys.stdout = stdout
        print(f'  Lint score is {score:.2f}')
        log.info(f'  Lint score is {score:.2f}')
    print('Lint score OK!\nDetailed lint report can be viewed in pylint_report.txt\n')
    log.info('Lint score OK!\nDetailed lint report can be viewed in pylint_report.txt')

if __name__ == '__main__':
    directory = os.path.dirname(os.path.abspath(__file__))
    log = logging.getLogger(__name__)
    logging.basicConfig(filename=directory+'/test.log',
                        level=os.environ.get('LOGLEVEL', LOG_LEVEL),
                        filemode='w',
                        format='\n%(levelname)-4s [L:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S')
    sys.setrecursionlimit(10000)
    check_function_definitions()
    check_sorting_functionality()
    check_sorting_performance()
    check_sorting_complexity()
    check_code_quality()

    print('All tests passed successfully.')
    log.info('All tests passed successfully.')





def insert(self, data):
            self._root = self.insert_recursive(self._root, data)

def insert_recursive(self, current, data):
    current = self.Node()
    if current is None:
        return self.Node(data)

    if data < current.data:
        current.left = self.insert_recursive(current.left, data)
    else:
        current.right = self.insert_recursive(current.right, data)

    current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))

    balance = self.get_balance(current)

    # Left Left Case
    if balance > 1 and data < current.left.data:
        return self.rotate_right(current)

    # Right Right Case
    if balance < -1 and data > current.right.data:
        return self.rotate_left(current)

    # Left Right Case
    if balance > 1 and data > current.left.data:
        current.left = self.rotate_left(current.left)
        return self.rotate_right(current)

    # Right Left Case
    if balance < -1 and data < current.right.data:
        current.right = self.rotate_right(current.right)
        return self.rotate_left(current)

    return current

def get_height(self, current):
    if current is None:
        return 0
    return current.height

def get_balance(self, current):
    if current is None:
        return 0
    return self.get_height(current.left) - self.get_height(current.right)

def rotate_left(self, parent):
    child = parent.right
    grandchild = child.left

    child.left = parent
    parent.right = grandchild

    parent.height = 1 + max(self.get_height(parent.left), self.get_height(parent.right))
    child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))

    return child

def rotate_right(self, parent):
    child = parent.left
    grandchild = child.right

    child.right = parent
    parent.left = grandchild

    parent.height = 1 + max(self.get_height(parent.left), self.get_height(parent.right))
    child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))

    return child