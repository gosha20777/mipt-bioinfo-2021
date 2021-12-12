import argparse
import os
import collections
import itertools

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


mis_table = {
    "A": "CGT",
    "C": "AGT",
    "G": "ACT",
    "T": "ACG"
}

complement_table = {
    "A": "T",
    "C": "G",
    "G": "C",
    "T": "A"
}

def get_kmer_variations(kmer, d):
    variation_list = [kmer]

    for delta in range(1, d + 1):
        for delta_idx in itertools.combinations(range(len(kmer)), delta):
            for variants in itertools.product(*[mis_table[kmer[i]] for i in delta_idx]):
                result = list(kmer)
                for idx, val in zip(delta_idx, variants):
                    result[idx] = val
                variation_list.append("".join(result))

    return variation_list


def calculate(input_path: str) -> str:
    with open(input_path, 'r') as file:
        text = file.readline()[:-1]
        k, d = list(map(int, file.readline().split()))
        word_list = collections.defaultdict(int)

        for i in range(len(text) - k + 1):
            word_list[text[i:i + k]] += 1
        variation_list = collections.defaultdict(int)
        for key, value in word_list.items():
            for variation in get_kmer_variations(key, d):
                variation_list[variation] += value

        maximum = max(variation_list.values())

        result = [key for key, value in variation_list.items() if value == maximum]
        return "\t".join(result)


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()
