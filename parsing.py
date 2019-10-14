"""For parsing dice/modifier math, e.g. {8 + prof + min(2, DEX)}.
Based on example from pyparsing's documentation: https://github.com/pyparsing/pyparsing/blob/master/examples/fourFn.py
"""
import pyparsing as pyp
import math
import operator
import statblock
import re
import utils


def build_grammar(stack: list):
    def push_first(tokens: list):
        stack.append(tokens[0])

    def push_unary_minus(tokens: list):
        for t in tokens:  # use a loop because we can have multiple -'s in a row
            if t == '-':
                stack.append('unary -')
            else:
                break

    dice = pyp.Regex(r'\d*d\d+')
    fnumber = pyp.Regex(r'[+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?')
    ident = pyp.Word(pyp.alphas, pyp.alphanums + '_$')
    plus, minus, mult, div = map(pyp.Literal, '+-*/')
    lpar, rpar = map(pyp.Suppress, '()')
    addop = plus | minus
    multop = mult | div

    expr = pyp.Forward()
    expr_list = pyp.delimitedList(pyp.Group(expr))
    fn_call = (ident + lpar - pyp.Group(expr_list) + rpar).setParseAction(lambda t: t.insert(0, (t.pop(0), len(t[0]))))
    atom = (addop[...] +
            ((fn_call | dice | fnumber | ident).setParseAction(push_first)
             | pyp.Group(lpar + expr + rpar))
            ).setParseAction(push_unary_minus)

    term = atom + (multop + atom).setParseAction(push_first)[...]
    expr <<= term + (addop + term).setParseAction(push_first)[...]
    return expr


epsilon = 1e-12
opn = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.ifloordiv,
    }
fn = {
    'min': min,
    'max': max,
    'abs': abs,
    'round': round,
    'trunc': math.floor,
    'sgn': lambda a: -1 if a < -epsilon else 1 if a > epsilon else 0
    }


def evaluate_stack(stack: list, vals: dict):
    op, num_args = stack.pop(), 0
    if isinstance(op, tuple):
        op, num_args = op
    op = op.replace('ft.', '').strip()

    if op == 'unary -':
        return -evaluate_stack(stack, vals)
    if op in "+-*/":
        op2 = evaluate_stack(stack, vals)
        op1 = evaluate_stack(stack, vals)
        return opn[op](op1, op2)
    elif op in fn:
        # note: args are pushed onto the stack in reverse order
        args = reversed([evaluate_stack(stack, vals) for _ in range(num_args)])
        return fn[op](*args)
    elif op in vals:
        return float(vals[op])
    elif op[0].isalpha():
        raise Exception(f'Invalid identifier "{op}" while parsing stack {stack} with vals {vals}')
    elif re.search(r'\d*d\d+', op):  # matches dice
        return utils.Dice.from_string(op).upper_average()
    else:
        try:
            return int(op)
        except ValueError:
            try:
                return float(op)
            except Exception as e:
                print(f'Exception while parsing stack {stack} with vals {vals}')
                raise e


def calculate(formula: str, vals: dict):
    stack = []
    results = build_grammar(stack).parseString(formula, parseAll=True)
    try:
        return int(math.floor(evaluate_stack(stack, vals)))
    except Exception as e:
        print(f'Exception while parsing stack {stack} with vals {vals}')
        raise e


if __name__ == '__main__':
    def test(s, expected, vals=None):
        vals = {} if vals is None else vals
        stack = []
        try:
            results = build_grammar(stack).parseString(s, parseAll=True)
            val = evaluate_stack(stack, vals)
        except pyp.ParseException as pe:
            print(s, "failed parse:", str(pe))
        except Exception as e:
            print(s, "failed eval:", str(e), stack)
        else:
            if val == expected:
                print(s, "=", val, results, "=>", stack)
            else:
                print(s + "!!!", val, "!=", expected, results, "=>", stack)

    warrior_vals = statblock.Statblock.from_markdown(filename='statblocks/warrior.md').get_substitutable_values()
    test('DEX * 3', 3, warrior_vals)
    test('3d4 / 3', 2)
    test("9", 9)
    test("-9", -9)
    test("--9", 9)
    test("9 + 3 + 6", 9 + 3 + 6)
    test("9 + 3 / 11", 9)
    test("(9 + 3)", (9 + 3))
    test("(9+3) / 11", 1)
    test("1 / 2", 0)
    test("3 / 2", 1)
    test("9 - 12 - 6", 9 - 12 - 6)
    test("9 - (12 - 6)", 9 - (12 - 6))
    test("2*3.14159", 2*3.14159)
    test("6.02E23 * 8.048", 6.02E23 * 8.048)
    test("sgn(-2)", -1)
    test("sgn(0)", 0)
    test("sgn(0.1)", 1)
    test("foo(0.1)", None)

