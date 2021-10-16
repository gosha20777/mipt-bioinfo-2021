import argparse
import collections
import os


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


def __get_suffix(row: str) -> str:
    if isinstance(row, (tuple)):
        return tuple([x[1:] for x in row])
    elif isinstance(row, str):
        return row[1:]
    else:
        raise Exception()


def __get_prefix(row: str) -> str:
    if isinstance(row, (list, tuple)):
        return tuple([x[:-1] for x in row])
    elif isinstance(row, str):
        return row[:-1]
    else:
        raise Exception()


def __build_graph(rows: list) -> dict:
    graph = collections.defaultdict(list)
    for row in rows:
        prefix = __get_prefix(row)
        suffix = __get_suffix(row)
        graph[prefix].append(suffix)
    return graph


def __count_in_out(graph: dict) -> dict:
    counter = collections.defaultdict(lambda: (0, 0))
    for k, v in graph.items():
        counter[k] = (counter[k][0], counter[k][1] + len(v))
        for node in v:
            counter[node] = (counter[node][0] + 1, counter[node][1])
    return counter


def __node_contig(graph: dict, node: str, outs: list) -> list:
    contigs = []
    for v in graph[node]:
        way = [node, v]
        i, o = outs[v]
        while i == 1 and o == 1:
            node = v
            v = graph[node][0]
            way.append(v)
            i, o = outs[v]
        contigs.append(way)
    return contigs


def __graph_to_contig(graph: dict) -> list:
    outs = __count_in_out(graph)
    contigs = []
    for k, (i, o) in outs.items():
        if o > 0 and not (o == 1 and i == 1):
            contigs.extend(__node_contig(graph, k, outs))
    return contigs


def calculate(input_path: str) -> str:
    with open(input_path, 'r') as file:
        rows = list(map(lambda x: x.replace("\n", "").strip(), file.readlines()))
        graph = __build_graph(rows)
        path = __graph_to_contig(graph)
        contig = list(map(
            lambda y: "".join([x[0] for x in y] + [y[-1][1:]]), path))
        return " ".join(contig)


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()