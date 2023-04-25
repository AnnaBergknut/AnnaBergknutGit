import re
import os
import ast
import sys
import time
import logging
import inspect
import textwrap
import pylint.lint
try:
    from graph import Graph
except ImportError:
    print('Error importing Graph. '+
        'Please make sure the class Graph is available in the graph module.')
    sys.exit(1)

LOG_LEVEL = 'INFO'
LINT_THRESHOLD = 8.0
FUNCTION_NAMES =       ['add_vertex',
                        'add_edge',
                        'clear',
                        'read_graph_from_file',
                        'mst',
                        'get_edge',
                        'save_mst_to_file']
FUNCTION_DEFINITIONS = ['(self, vertex: str) -> None',
                        '(self, source: str, target: str, weight: int) -> None',
                        '(self) -> None',
                        '(self, filepath: str) -> None',
                        '(self) -> None',
                        '(self, source: str, target: str) -> int',
                        '(self, filepath: str) -> None']
FUNCTION_DEFINITIONS = ['(vertex: str) -> None',
                        '(source: str, target: str, weight: int) -> None',
                        '() -> None',
                        '(filepath: str) -> None',
                        '() -> None',
                        '(source: str, target: str) -> int',
                        '(filepath: str) -> None']
SCALE_LIMIT_SPARSE = (6,20)
SCALE_LIMIT_DENSE = (80,400)

version = sys.version_info
if version[0] < 3:
    print(f'Please install python 3, at least version 3.6. You have {version[0]}.{version[1]}.')
    sys.exit(1)
elif version[1] < 6:
    print(f'Please install python 3, at least version 3.6. You have {version[0]}.{version[1]}.')
    sys.exit(1)

# A wrapper to check if there is an explicit return statement in a function.
def contains_explicit_return(func):
    return any(isinstance(node, ast.Return)
        for node in ast.walk(ast.parse(textwrap.dedent(inspect.getsource(func)))))

def check_function_definitions():
     # Test if functions exist
    print('\nTesting if the required functions are implemented and correctly defined.')
    log.info('\nTesting if the required functions are implemented and correctly defined.')
    graph = Graph()
    g_funcs = dir(graph)
    class_functions = [getattr(graph, x) for x in dir(graph) if callable(getattr(graph, x))]

    for func_name in FUNCTION_NAMES:
        if func_name not in g_funcs or not callable(getattr(graph, func_name)):
            print(f'Test failed!\nThe function {func_name}() is missing.')
            log.info('Test failed!\nThe function %s() is missing.',func_name)
            sys.exit(1)

    class_functions = [graph.add_vertex,
                    graph.add_edge,
                    graph.clear,
                    graph.read_graph_from_file,
                    graph.mst,
                    graph.get_edge]

    # Test if functions have correct parameters
    for func, func_name, func_def in zip(class_functions, FUNCTION_NAMES, FUNCTION_DEFINITIONS):
        if str(inspect.signature(func)) != func_def:
            print('Please use the same signature as defined in the assignment. '+
                f'It should be:\n{func_name}{func_def}'+
                f'\nIt is:\n{func_name}{str(inspect.signature(func))}')
            log.info('Please use the same signature as defined in the assignment.'+
                ' It should be:\n%s%s', func_name, func_def)
            sys.exit(1)

    # Test if functions returns None
    for func, func_name in zip(class_functions[:-1], FUNCTION_NAMES[:-1]):
        if contains_explicit_return(func):
            print(f'{func_name} should not have any return statement. Remove it.')
            log.info('%s should not have any return statement. Remove it.', func_name)
            sys.exit(1)

    print('All functions OK!\n')
    log.info('All functions OK!\n')

def check_msts_initial():
    print('Performing initial tests for MST,'+
        ' investigating if basic functionality and formats are correct.')
    input_file = 'initial.txt'
    results_file = 'results.txt'
    answer_file = 'initial_answer.txt'
    graph = Graph()
    graph.read_graph_from_file(f'Testdata/{input_file}')
    graph.mst()
    graph.save_mst_to_file('Results/' + results_file)
    with open('Results/' + results_file,'r',encoding='UTF-8') as file, \
         open('Answers/' + answer_file,'r',encoding='UTF-8') as file2:
        student_answer = [line for line in file.readlines()]
        answers = [line for line in file2.readlines()]

        # Check mst cost first
        if int(student_answer[0]) != int(answers[0]):
            print(f'  Error: The MST cost is incorrect for the graph in {input_file}'+
                ' testfile. It should be {answers[0]}')
            log.info(f'Error: The MST cost is incorrect for the graph in {input_file}'+
                ' testfile. It should be {answers[0]}')
            sys.exit(1)

        # Check if correct number of edges have been chosen
        if len(student_answer) != len(answers):
            print('  Error: The MST does not have the correct amount of edges.\n'+
                f'  It should be {len(answers)-1}, but is is {len(student_answer)-1}')
            log.info('Error: The MST does not have the correct amount of edges.\n'+
                'It should be %d, but is is %d'%(len(answers)-1,len(student_answer)-1))
            sys.exit(1)

        # Check if correct edges have been chosen
        correct_edges = {}
        for line in answers[1:]:
            source, target, weight = re.split(' -> | : ',line)
            correct_edges[source] = {}
            correct_edges[source][target] = int(weight)
            correct_edges[target] = {}
            correct_edges[target][source] = int(weight)

        correct_edge_list = []
        incorrect_edge_list = []
        for line in student_answer[1:]:
            source, target, weight = re.split(' -> | : ',line)
            if (source in correct_edges and
                 target in correct_edges[source] and
                 correct_edges[source][target] == int(weight)):
                correct_edge_list.append(f'{source} -> {target} : {weight}')
            elif (target in correct_edges and
                 source in correct_edges[target] and
                 correct_edges[target][source] == int(weight)):
                correct_edge_list.append(f'{source} -> {target} : {weight}')
            else:
                incorrect_edge_list.append(f'{source} -> {target} : {weight}')

        if len(incorrect_edge_list) != 0:
            print(f'Error! There are incorrect edges in the MST.')
            print('  Correct edges are\n')
            for edge in correct_edge_list:
                print(f'    {edge}')
            print('  Incorrect edges are\n')
            for edge in incorrect_edge_list:
                print(f'    {edge}')
            sys.exit(1)

    print('Initial tests OK!')

def check_msts_thorough():
    print('\nTesting MST generation on tougher graphs.')
    log.info('Testing MST generation on tougher graphs.')

    input_files =  ['100_sparse.txt',
                    '1000_sparse.txt',
                    '10000_sparse.txt',
                    '100000_sparse.txt',
                    '100_dense.txt',
                    '1000_dense.txt']
    result_files = ['result_100_sparse.txt',
                    'result_1000_sparse.txt',
                    'result_10000_sparse.txt',
                    'result_100000_sparse.txt',
                    'result_100_dense.txt',
                    'result_1000_dense.txt']
    answers =      [(490,100),
                    (4141, 1000),
                    (41254,10000),
                    (409401,100000),
                    (199,100),
                    (1099,1000)]

    for input_file, result_file, answer in zip(input_files, result_files, answers):
        graph = Graph()
        graph.read_graph_from_file(f'Testdata/{input_file}')
        graph.mst()
        graph.save_mst_to_file('Results/' + result_file)

        print(f'  {input_file}... ', end="")
        with open('Results/' + result_file,'r',encoding='UTF-8') as file:
            student_answer = [line for line in file.readlines()]

            # Check mst cost first
            if int(student_answer[0]) != answer[0]:
                print(f'Error!\nThe MST cost is incorrect for the graph in {input_file}' +
                    f'testfile.\nIt should be {answer[0]} but is {student_answer[0]}.')
                log.info(f'Error: The MST cost is incorrect for the graph in {input_file}' +
                    f' testfile. It should be {answer[0]} but is {student_answer[0]}.')
                sys.exit(1)

            # Check if correct number of edges have been chosen
            if (len(student_answer)-1) != answer[1]:
                print(f'Error!\nThe MST does not have the correct amount of edges.\n'+
                    f'  It should be {answer[1]}, but is is {len(student_answer)-1}')
                log.info(f'Error: The MST does not have the correct amount of edges.\n'+
                    f'It should be {answer[1]}, but is is {len(student_answer)-1}')
                sys.exit(1)
        print('OK!')

    print('MST generations OK!')
    log.info('MST generations OK!')

def check_performance():
    print('\nTesting run time.')
    log.info('Testing run time.')

    filepaths = ['100_dense.txt', '100_sparse.txt', '1000_sparse.txt', '10000_sparse.txt']
    graph = Graph()
    for filepath in filepaths:
        print(f'  {filepath}... ', end="")
        graph.read_graph_from_file(f'Testdata/{filepath}')
        time_before = time.perf_counter()
        graph.mst()
        time_after = time.perf_counter()
        time_elapsed = time_after - time_before
        if time_elapsed > 0.5:
            print('Not OK!\n  Your algorithm is running too slow. All files should all run ' +
                f'below 0.5s.\n  {filepath} currently runs in {time_elapsed:.4f} seconds.')
            log.info('Not OK!\n  Your algorithm is running too slow. All files should all run' +
                ' below 0.5s.\n  %s currently runs in %.4f seconds.', filepath, time_elapsed)
            sys.exit(1)
        else:
            print('OK!')

    print('Run time tests OK!')

def check_complexity():
    print('\nEstimating time complexity.')
    log.info('Estimating time complexity.')

    time_elapsed = []
    filepaths = ['100_sparse.txt', '1000_sparse.txt', '10000_sparse.txt', '100000_sparse.txt']
    graph = Graph()
    for filepath in filepaths:
        graph.read_graph_from_file(f'Testdata/{filepath}')
        time_before = time.perf_counter()
        graph.mst()
        time_after = time.perf_counter()
        time_elapsed.append(time_after - time_before)

    for i in range(len(time_elapsed)-1):
        if SCALE_LIMIT_SPARSE[0] > (time_elapsed[i+1] / time_elapsed[i]):
            print(' Your time complexity estimation is faster than O(E log V).')
            print(f'  {time_elapsed[i+1] / time_elapsed[i]}')
            sys.exit(1)
        elif SCALE_LIMIT_SPARSE[1] < (time_elapsed[i+1] / time_elapsed[i]):
            print(' Your time complexity estimation is slower than O(E log V).')
            print(f'  {time_elapsed[i+1] / time_elapsed[i]}')
            sys.exit(1)


    print('  Your algorithms scales in a O(E log V) fashion.')
    print('Time complexity tests OK!')
    log.info('Time complexity tests OK!')

def check_code_quality():
    print(f'\nChecking code quality by pylint score, {LINT_THRESHOLD} is minimum to pass ...')
    log.info(f'Checking code quality by pylint score, {LINT_THRESHOLD} is minimum to pass')
    stdout = sys.stdout
    with open('pylint_report.txt', 'w', encoding='UTF-8') as outfile:
        sys.stdout = outfile
        run = pylint.lint.Run(
            ['graph.py'], exit=False)
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
    logging.basicConfig(filename=directory+'/graph_tests.log',
                        level=os.environ.get('LOGLEVEL', LOG_LEVEL),
                        filemode='w',
                        format='\n%(levelname)-4s [L:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S')
    check_function_definitions()
    check_msts_initial()
    check_performance()
    check_complexity()
    check_msts_thorough()
    check_code_quality()
    print('\nAll tests passed!')
