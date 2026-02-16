import sys
import random
import itertools

"\n\nTINY_GSHCGP.py: An Implementation of Geometric Semantic ***Hill Climber*** Genetic Programming Using Higher-Order Functions and Memoization\n\nAuthor: Alberto Moraglio (albmor@gmail.com)\n\nFeatures:\n\n- Same as TINY_GSGP.py, substituting the evolutionary algorithm with a hill-climber.\n\n- The fitness landscape seen by Geometric Semantic operators is always unimodal. A hill climber can reach the optimum.\n\n- Offspring functions call parent functions rather than embed their definitions (no grwoth, implicit ancestry trace).\n\n- Even if offspring functions embedded parent function definition, the growth is linear in the number of generation (not exponential as with crossover). \n\n- Memoization of individuals turns time complexity of fitness evalutation from linear to constant (not exponential to constant as with crossover).\n\n- Implicit ancestry trace and memoization not strictly necessary with hill-climber for efficent implementation.\n\n- The final solution is a compiled function. It can be extracted using the ancestry trace to reconstruct its 'source code'. \n\nThis implementation is to evolve Boolean expressions. It can be easily adapted to evolve arithmetic expressions or classifiers.\n\n"

DEPTH = 4
GENERATIONS = 400

numvars = int(sys.argv[1])
vars = ['x' + str(i) for i in range(numvars)]

# Inline randfunct logic to create initial 'curr'
# Inline randexpr logic using a stack to generate the expression string 're'
work_stack = [DEPTH]
expr_parts = []
while work_stack:
    item = work_stack.pop()
    if isinstance(item, str):
        expr_parts.append(item)
    elif item == 'GEN_OP':
        expr_parts.append(random.choice(['and', 'or']))
    else:
        dep = item
        if dep == 1 or random.random() < 1.0 / (2 ** dep - 1):
            expr_parts.append(random.choice(vars))
        elif random.random() < 1.0 / 3:
            # Structure: 'not ' + randexpr(dep - 1)
            work_stack.append(dep - 1)
            work_stack.append('not ')
        else:
            # Structure: '(' + randexpr(dep - 1) + ' ' + choice + ' ' + randexpr(dep - 1) + ')'
            # Stack is LIFO, so push in reverse order of appearance
            work_stack.append(')')
            work_stack.append(dep - 1)   # Right operand
            work_stack.append(' ')
            work_stack.append('GEN_OP')  # Operator choice
            work_stack.append(' ')
            work_stack.append(dep - 1)   # Left operand
            work_stack.append('(')

re = "".join(expr_parts)
temp1 = ', '
rf_raw = eval('lambda ' + temp1.join(vars) + ': ' + re)

# Inline memoization for curr
rf_cache = {}
rf = lambda *args, _f=rf_raw, _c=rf_cache: _c[args] if args in _c else _c.setdefault(args, _f(*args))
rf.geno = lambda: re

curr = rf

# Inline fitness for initial curr
fit = 0
somelists = [[True, False] for i in range(numvars)]
for element in itertools.product(*somelists):
    # Inline targetfunct: args.count(True) % 2 == 1
    target_val = element.count(True) % 2 == 1
    if curr(*element) != target_val:
        fit = fit + 1
curr.fit = fit

# Main climb loop
for gen in range(GENERATIONS + 1):
    # Inline mutation to create offspring 'off'
    # Generate mintermexpr
    temp2 = ' and '
    mintermexpr = temp2.join([random.choice([x, 'not ' + x]) for x in vars])
    temp3 = ', '
    minterm = eval('lambda ' + temp3.join(vars) + ': ' + mintermexpr)
    
    if random.random() < 0.5:
        # Offspring OR
        offspring_raw = lambda *x, _p=curr, _m=minterm: _p(*x) or _m(*x)
        geno_lambda = lambda _p=curr, _m_expr=mintermexpr: '(' + _p.geno() + ' or ' + _m_expr + ')'
    else:
        # Offspring AND NOT
        offspring_raw = lambda *x, _p=curr, _m=minterm: _p(*x) and (not _m(*x))
        geno_lambda = lambda _p=curr, _m_expr=mintermexpr: '(' + _p.geno() + ' and not ' + _m_expr + ')'

    # Inline memoization for offspring
    off_cache = {}
    off = lambda *args, _f=offspring_raw, _c=off_cache: _c[args] if args in _c else _c.setdefault(args, _f(*args))
    off.geno = geno_lambda

    # Inline fitness for offspring
    fit = 0
    somelists = [[True, False] for i in range(numvars)]
    for element in itertools.product(*somelists):
        target_val = element.count(True) % 2 == 1
        if off(*element) != target_val:
            fit = fit + 1
    off.fit = fit

    if off.fit < curr.fit:
        curr = off
    if gen % 10 == 0:
        curr.fit