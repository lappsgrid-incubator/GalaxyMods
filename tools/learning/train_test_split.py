import pandas
from sklearn.model_selection import train_test_split
import argparse


def main(infile, train_pct):
    """
    Split file into train and test datasets
    Args:
        infile: str, input tabular file
        train_pct: size of training set as a percentage
    """
        
    csv = pandas.read_csv(infile, sep='\t')
    train, test = train_test_split(csv, train_size = train_pct)

    train.to_csv(r'train_data.tsv', sep='\t')
    test.to_csv(r'test_data.tsv', sep='\t')


if __name__ == "__main__":
    aparser = argparse.ArgumentParser()
    aparser.add_argument("-i", "--input", dest="infile", required=True)
    aparser.add_argument("-p", "--pct", dest="train_pct", type=float, required=True)
    args = aparser.parse_args()
    main(args.infile, args.train_pct)
