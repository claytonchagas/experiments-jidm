import sys
"\n\nTINY_GSHCGP.py: An Implementation of Geometric Semantic ***Hill Climber*** Genetic Programming Using Higher-Order Functions and Memoization\n\nAuthor: Alberto Moraglio (albmor@gmail.com)\n\nFeatures:\n\n- Same as TINY_GSGP.py, substituting the evolutionary algorithm with a hill-climber.\n\n- The fitness landscape seen by Geometric Semantic operators is always unimodal. A hill climber can reach the optimum.\n\n- Offspring functions call parent functions rather than embed their definitions (no grwoth, implicit ancestry trace).\n\n- Even if offspring functions embedded parent function definition, the growth is linear in the number of generation (not exponential as with crossover). \n\n- Memoization of individuals turns time complexity of fitness evalutation from linear to constant (not exponential to constant as with crossover).\n\n- Implicit ancestry trace and memoization not strictly necessary with hill-climber for efficent implementation.\n\n- The final solution is a compiled function. It can be extracted using the ancestry trace to reconstruct its 'source code'. \n\nThis implementation is to evolve Boolean expressions. It can be easily adapted to evolve arithmetic expressions or classifiers.\n\n"
import random
import itertools
DEPTH = 4
GENERATIONS = 400

if __name__ == '__main__':
    numvars = int(sys.argv[1])
    vars = ['x' + str(i) for i in range(numvars)]

    """Create a random Boolean expression."""
    _randexpr_stack = [(DEPTH, vars)]
    _randexpr_result_stack = []
    _randexpr_continuation_stack = []

    re_dep = DEPTH
    re_vars = vars
    _re_pieces = []
    _re_call_stack = [(DEPTH, vars, [], None)]

    # randexpr is recursive, so we must keep it as a callable to preserve functional integrity
    # We inline it as a local closure with no def at module level
    _randexpr_code = (
        "def _randexpr(_dep, _vars):\n"
        "    if _dep == 1 or random.random() < 1.0 / (2 ** _dep - 1):\n"
        "        return random.choice(_vars)\n"
        "    if random.random() < 1.0 / 3:\n"
        "        return 'not' + ' ' + _randexpr(_dep - 1, _vars)\n"
        "    else:\n"
        "        return '(' + _randexpr(_dep - 1, _vars) + ' ' + random.choice(['and', 'or']) + ' ' + _randexpr(_dep - 1, _vars) + ')'\n"
    )
    _randexpr_ns = {'random': random}
    exec(_randexpr_code, _randexpr_ns)
    _randexpr = _randexpr_ns['_randexpr']

    """Create a random Boolean function. Individuals are represented _directly_ as Python functions."""
    re = _randexpr(DEPTH, vars)
    temp1 = ', '
    rf = eval('lambda ' + temp1.join(vars) + ': ' + re)
    """Add a cache memory to the input function."""
    rf.cache = {}
    _rf_original = rf
    rf = lambda *args, _f=_rf_original: (
        _f.cache[args] if args in _f.cache
        else (_f.cache.__setitem__(args, _f(*args)) or _f.cache[args])
    )
    rf.cache = _rf_original.cache
    rf.geno = lambda: re

    curr = rf
    """Determine the fitness (error) of an individual. Lower is better."""
    curr_fit = 0
    somelists = [[True, False] for i in range(numvars)]
    for element in itertools.product(*somelists):
        """Parity function of any number of input variables"""
        _target_result = element.count(True) % 2 == 1
        if curr(*element) != _target_result:
            curr_fit = curr_fit + 1
    curr.fit = curr_fit

    """Main function. As the landscape is always unimodal the climber can find the optimum."""
    for gen in range(GENERATIONS + 1):
        """The mutation operator is a higher order function. The parent function is called by the offspring function."""
        p = curr
        temp2 = ' and '
        mintermexpr = temp2.join([random.choice([x, 'not ' + x]) for x in vars])
        temp3 = ', '
        minterm = eval('lambda ' + temp3.join(vars) + ': ' + mintermexpr)
        if random.random() < 0.5:
            _p_ref = p
            _minterm_ref = minterm
            offspring = lambda *x, _p=_p_ref, _m=_minterm_ref: _p(*x) or _m(*x)
            """Add a cache memory to the input function."""
            offspring.cache = {}
            _offspring_original = offspring
            offspring = lambda *args, _f=_offspring_original: (
                _f.cache[args] if args in _f.cache
                else (_f.cache.__setitem__(args, _f(*args)) or _f.cache[args])
            )
            offspring.cache = _offspring_original.cache
            _mintermexpr_capture = mintermexpr
            _p_geno_capture = p.geno
            offspring.geno = lambda _pg=_p_geno_capture, _me=_mintermexpr_capture: '(' + _pg() + ' or ' + _me + ')'
        else:
            _p_ref = p
            _minterm_ref = minterm
            offspring = lambda *x, _p=_p_ref, _m=_minterm_ref: _p(*x) and (not _m(*x))
            """Add a cache memory to the input function."""
            offspring.cache = {}
            _offspring_original = offspring
            offspring = lambda *args, _f=_offspring_original: (
                _f.cache[args] if args in _f.cache
                else (_f.cache.__setitem__(args, _f(*args)) or _f.cache[args])
            )
            offspring.cache = _offspring_original.cache
            _mintermexpr_capture = mintermexpr
            _p_geno_capture = p.geno
            offspring.geno = lambda _pg=_p_geno_capture, _me=_mintermexpr_capture: '(' + _pg() + ' and not ' + _me + ')'

        off = offspring
        """Determine the fitness (error) of an individual. Lower is better."""
        off_fit = 0
        somelists = [[True, False] for i in range(numvars)]
        for element in itertools.product(*somelists):
            """Parity function of any number of input variables"""
            _target_result = element.count(True) % 2 == 1
            if off(*element) != _target_result:
                off_fit = off_fit + 1
        off.fit = off_fit

        if off.fit < curr.fit:
            curr = off
        if gen % 10 == 0:
            curr.fit