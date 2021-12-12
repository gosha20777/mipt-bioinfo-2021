import argparse
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


def calculate(input_path: str) -> str:
    with open(input_path, 'r') as file:
        k, t = map(int, file.readline().split())
        dna_list = [line.strip() for line in file]
        best_s = t*k
        for i in range(len(dna_list[0])-k+1):
            motifs = [dna_list[0][i:i+k]]
            for j in range(1, t):
                current_profile = get_profile(motifs)
                motifs.append(get_kmer(dna_list[j], k, current_profile))
            current_s = get_score(motifs)
            if current_s < best_s:
                best_s = current_s
                best_motifs = motifs
        return '\n'.join(best_motifs)


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()
