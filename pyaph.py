#!/usr/bin/env python3
# coding: utf-8

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import argparse
import sys
from pathlib import Path


def plot(args: argparse.Namespace):
    df = None
    if args.type == "csv":
        df = pd.read_csv(args.input,encoding="utf-8",index_col=0)
    elif args.type == "tsv":
        pass
    print(df)
    plt.rcParams["font.family"] = "IPAexGothic"
    df.plot()
    plt.ylabel("ﾟC",rotation=0)
    plt.show()


def show(file: Path = None):
    if file is None:
        plt.show()
    else:
        plt.savefig(file)


def main():
    # 引数のパース
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers()

    sub = sub_parser.add_parser("plot")
    sub.add_argument("-t", "--type", choices=["csv", "tsv", "json"],default="csv")
    sub.add_argument("input",
                     nargs="?",
                     type=argparse.FileType("r"),
                     default=sys.stdin)
    sub.add_argument("output",nargs="?",type=str,default="-")
    sub.set_defaults(func=plot)

    args = parser.parse_args()
    # set seaborn style
    sns.set()
    sns.set_style("whitegrid", {"grid.linestyle": "--"})
    # 実行
    args.func(args)

if __name__ == "__main__":
    main()
