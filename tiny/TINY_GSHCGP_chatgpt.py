import sys
"\n\nTINY_GSHCGP.py: An Implementation of Geometric Semantic ***Hill Climber*** Genetic Programming Using Higher-Order Functions and Memoization\n\nAuthor: Alberto Moraglio (albmor@gmail.com)\n\nFeatures:\n\n- Same as TINY_GSGP.py, substituting the evolutionary algorithm with a hill-climber.\n\n- The fitness landscape seen by Geometric Semantic operators is always unimodal. A hill climber can reach the optimum.\n\n- Offspring functions call parent functions rather than embed their definitions (no grwoth, implicit ancestry trace).\n\n- Even if offspring functions embedded parent function definition, the growth is linear in the number of generation (not exponential as with crossover). \n\n- Memoization of individuals turns time complexity of fitness evalutation from linear to constant (not exponential to constant as with crossover).\n\n- Implicit ancestry trace and memoization not strictly necessary with hill-climber for efficent implementation.\n\n- The final solution is a compiled function. It can be extracted using the ancestry trace to reconstruct its 'source code'. \n\nThis implementation is to evolve Boolean expressions. It can be easily adapted to evolve arithmetic expressions or classifiers.\n\n"
import random
import itertools
DEPTH = 4
GENERATIONS = 400

if __name__ == '__main__':
    numvars = int(sys.argv[1])
    vars = ['x' + str(i) for i in range(numvars)]

    dep = DEPTH
    _stack = [{'dep': dep, 'stage': 0}]
    _last_expr = None
    while _stack:
        _frame = _stack[-1]
        dep = _frame['dep']
        stage = _frame['stage']
        if stage == 0:
            if dep == 1:
                _last_expr = random.choice(vars)
                _stack.pop()
                continue
            if random.random() < 1.0 / (2 ** dep - 1):
                _last_expr = random.choice(vars)
                _stack.pop()
                continue
            if random.random() < 1.0 / 3:
                _frame['type'] = 'unary'
                _frame['stage'] = 1
                _stack.append({'dep': dep - 1, 'stage': 0})
                continue
            else:
                _frame['type'] = 'binary'
                _frame['stage'] = 1
                _stack.append({'dep': dep - 1, 'stage': 0})
                continue
        if _frame['type'] == 'unary' and stage == 1:
            _last_expr = 'not' + ' ' + _last_expr
            _stack.pop()
            continue
        if _frame['type'] == 'binary' and stage == 1:
            _frame['left'] = _last_expr
            _frame['op'] = random.choice(['and', 'or'])
            _frame['stage'] = 2
            _stack.append({'dep': dep - 1, 'stage': 0})
            continue
        if _frame['type'] == 'binary' and stage == 2:
            _last_expr = '(' + _frame['left'] + ' ' + _frame['op'] + ' ' + _last_expr + ')'
            _stack.pop()
            continue
    re = _last_expr

    temp1 = ', '
    rf0 = eval('lambda ' + temp1.join(vars) + ': ' + re)
    rf0.cache = {}
    rf = (lambda *args, _f=rf0: _f.cache[args] if args in _f.cache else _f.cache.setdefault(args, _f(*args)))
    rf.geno = (lambda re=re: re)
    curr = rf

    fit = 0
    somelists = [[True, False] for i in range(numvars)]
    for element in itertools.product(*somelists):
        if curr(*element) != (element.count(True) % 2 == 1):
            fit = fit + 1
    curr.fit = fit

    for gen in range(GENERATIONS + 1):
        temp2 = ' and '
        mintermexpr = temp2.join([random.choice([x, 'not ' + x]) for x in vars])
        temp3 = ', '
        minterm = eval('lambda ' + temp3.join(vars) + ': ' + mintermexpr)
        if random.random() < 0.5:
            offspring0 = (lambda *x, p=curr, minterm=minterm: p(*x) or minterm(*x))
            offspring0.cache = {}
            off = (lambda *args, _f=offspring0: _f.cache[args] if args in _f.cache else _f.cache.setdefault(args, _f(*args)))
            off.geno = (lambda p=curr, mintermexpr=mintermexpr: '(' + p.geno() + ' or ' + mintermexpr + ')')
        else:
            offspring0 = (lambda *x, p=curr, minterm=minterm: p(*x) and (not minterm(*x)))
            offspring0.cache = {}
            off = (lambda *args, _f=offspring0: _f.cache[args] if args in _f.cache else _f.cache.setdefault(args, _f(*args)))
            off.geno = (lambda p=curr, mintermexpr=mintermexpr: '(' + p.geno() + ' and not ' + mintermexpr + ')')

        fit = 0
        somelists = [[True, False] for i in range(numvars)]
        for element in itertools.product(*somelists):
            if off(*element) != (element.count(True) % 2 == 1):
                fit = fit + 1
        off.fit = fit

        if off.fit < curr.fit:
            curr = off
        if gen % 10 == 0:
            curr.fit
