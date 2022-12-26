import re
from dataclasses import dataclass


def load_data(path: str):
    with open(path) as f:
        lines = [Monkey(s.strip('\n')).parse() for s in f.readlines()]

    monkeys = {}
    for monkey in lines: monkeys |= monkey

    return monkeys


@dataclass
class Monkey:
    signature: str

    def parse(self):
        name, job = self.signature.split(': ')
        pattern = r'(\+|\-|\*|\/)'
        op = re.findall(pattern, job)
        if op:
            op = op.pop()
            left, right = job.split(op)
            return {name: {'monkeys': [left.strip(), right.strip()], 'op': op}}
        else: return {name: int(job)}


def monkey_yells(name: str, monkeys: dict[str, dict | int]):
    job = monkeys[name]
    if isinstance(job, int | float): return job
    if isinstance(job, dict):
        m1, m2 = job['monkeys']
        left   = monkey_yells(m1, monkeys)
        right  = monkey_yells(m2, monkeys)
        op     = job['op']
        if   op == '+': return left + right
        elif op == '-': return left - right
        elif op == '*': return left * right
        elif op == '/': return left // right


def humn_yells(monkeys: dict[str, dict | int]):
    m1, m2 = monkeys['root']['monkeys']

    # learning rate
    lr = 1e-2
    # mean absolute error
    mae = lambda x, y: abs(x - y)
    # gradient descent step
    grad = lambda x, lr, loss: x - lr * loss
    # initial guess
    x = monkeys['humn']
    # initial loss
    loss = mae(monkey_yells(m1, monkeys), monkey_yells(m2, monkeys))

    while loss != 0:
        x -= grad(x, lr, loss)
        monkeys['humn'] += x
        loss = mae(monkey_yells(m1, monkeys), monkey_yells(m2, monkeys))

    return int(monkeys['humn'])


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert monkey_yells('root', assert_data) == 152
    assert humn_yells(assert_data) == 301

    input_data = load_data('./input.txt')
    # part 1
    print(monkey_yells('root', input_data))
    # part 2
    print(humn_yells(input_data))

