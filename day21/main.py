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
    if isinstance(job, int): return job
    if isinstance(job, dict):
        m1, m2 = job['monkeys']
        left  = monkey_yells(m1, monkeys)
        right = monkey_yells(m2, monkeys)
        op    = job['op']
        if   op == '+': return left + right
        elif op == '-': return left - right
        elif op == '*': return left * right
        elif op == '/': return left // right


def humn_yells(name: str, monkeys: dict[str, dict | int]):
    kkk

if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    # assert monkey_yells('root', assert_data) == 152
    print(monkey_yells('root', assert_data))

    input_data = load_data('./input.txt')
    # part 1
    # print(monkey_yells('root', input_data))
    # part 2

