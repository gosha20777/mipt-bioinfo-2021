import argparse
import os
import numpy as np
import collections


def parse_args(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Make submission')
    parser.add_argument(
        '-i', '--input',
        help='path to input file',
        type=str,
        required=True
    )
    parser.add_argument(
        '-o', '--output',
        help='path to output file',
        type=str,
        required=True
    )
    return parser.parse_args(args)

def __get_distance(p, q):
    G = collections.defaultdict(list)
    for x in p + q:
        n = len(x)
        for i in range(n):
            G[x[i]].append(-1 * x[(i + 1) % n])
            G[-1 * x[(i + 1) % n]].append(x[i])
    m = 0
    c_k = set(G.keys())
    while len(c_k) > 0:
        m += 1
        q_k = [c_k.pop()]
        while q_k:
            k = q_k.pop()
            q_k += list(filter(lambda nd: nd in c_k, G.get(k, [])))
            c_k -= set(q_k)
    return sum(map(len, p)) - m


def calculate(input_path: str) -> str:
    with open(input_path, 'r') as file:
        data = file.readlines()[:2]
        p, q = [l.strip().replace("\n", "").replace("+", "")[1:-1].split(")(") for l in data]
        p = list(list(map(int, l.split())) for l in p)
        q = list(list(map(int, l.split())) for l in q)
        return str(__get_distance(p, q))
        

def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()
