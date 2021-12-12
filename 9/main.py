import argparse
import os
from numpy.random import randint


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


def get_score(motif_list):
    col_list = [''.join(seq) for seq in zip(*motif_list)]
    max_c = sum([max([c.count(x) for x in 'ACGT']) for c in col_list])
    return len(motif_list[0])*len(motif_list) - max_c

def get_profile(motif_list):
    col_list = [''.join(seq) for seq in zip(*motif_list)]
    return [[(c.count(nuc) + 1) / (len(c) + 4) for nuc in 'ACGT'] for c in col_list]

def get_kmer(dna, k, profile):
    nuc_loc = {
        nucleotide: index for index, nucleotide in enumerate('ACGT')
    }
    max_prob = -1
    for i in range(len(dna)-k+1):
        current_prob = 1
        for j, nuc in enumerate(dna[i:i+k]):
            current_prob *= profile[j][nuc_loc[nuc]]
        if current_prob > max_prob:
            max_prob = current_prob
            result = dna[i:i+k]
    return result

def search(dna_list, k, t, N):
    rand_int_list = [randint(0, len(dna_list[0])-k) for a in range(t)]
    motif_list = [dna_list[i][r:r+k] for i, r in enumerate(rand_int_list)]
    best_s = [get_score(motif_list), motif_list]
    for _ in range(N):
        i = randint(t)
        no_i_motif_list = motif_list[:i] + motif_list[i+1:]
        current_profile = get_profile(no_i_motif_list)
        motif_list = motif_list[:i] +\
            [get_kmer(dna_list[i], k, current_profile)] +\
            motif_list[i+1:]
        current_s = get_score(motif_list)
        if current_s < best_s[0]:
            best_s = [current_s, motif_list]
    return best_s


def calculate(input_path: str) -> str:
    with open(input_path, 'r') as file:
        k, t, N = map(int, file.readline().split())
        dna_list = [line.strip() for line in file]
        best_motif_list = search(dna_list, k, t, N)
        for _ in range(1, 20):
            new_motif_list = search(dna_list, k, t, N)
            if new_motif_list[0] < best_motif_list[0]:
                best_motif_list = new_motif_list
        return '\n'.join(best_motif_list[1])


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()
