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


def __chromosome2cycle(c):
    n = []
    w = [-1, 1]
    b = [[0, -1], [-1, 0]]
    for i in c:
        n.append(w[i > 0] * 2 * i + b[i > 0][0])
        n.append(w[i > 0] * 2 * i + b[i > 0][1])
    return n


def __color_edges(g):
    res = []
    for c in g:
        cycle = __chromosome2cycle(c)
        for j in range(len(cycle) // 2):
            e = (cycle[1 + 2 * j], cycle[(2 + 2 * j) % len(cycle)])
            res.append(e)
    return res


def __graph2genome(G):
    adj = np.zeros(len(G) * 2, dtype=np.int)
    for e in G:
        adj[e[0] - 1] = e[1] - 1
        adj[e[1] - 1] = e[0] - 1
    res = []
    cl = []
    for e in G:
        sv = e[0]
        if sv in cl:
            continue
        cl.append(sv)
        c = sv - 1 if sv % 2 == 0 else sv + 1
        b = []
        while True:
            nv = sv / 2 if sv % 2 == 0 else -(sv + 1) / 2
            b.append(nv)
            fv = adj[sv - 1] + 1
            cl.append(fv)
            if fv == c:
                res.append(b)
                break
            sv = fv - 1 if fv % 2 == 0 else fv + 1
            cl.append(sv)
    return res


def __two_break_on_genome_graph(G, i, j, k, l):
    to_del = ((i, j), (j, i), (k, l), (l, k))
    res = [t for t in G if t not in to_del]
    res.append((i, k))
    res.append((j, l))
    return res


def __two_break_on_genome(gen, i, j, k, l):
    G = __color_edges(gen)
    G = __two_break_on_genome_graph(G, i, j, k, l)
    gen = __graph2genome(G)
    return gen


def calculate(input_path: str) -> str:
    with open(input_path, 'r') as file:
        data = file.readlines()[:2]
        p = data[0].strip().replace("\n", "").replace("+", "")[1:-1].split(")(")
        q = list(map(int, data[1].split(", ")))
        p = list(list(map(int, line.split())) for line in p)
        res = __two_break_on_genome(p, *q)

        value_func = lambda v: ['-', '+'][v > 0] + str(abs(int(v)))
        return " ".join(
            ['(' + ' '.join([value_func(v) for v in b]) + ')'
             for b in res])
        

def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()
