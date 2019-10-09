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
    # ArgParseのFileTypeを使うとエンコーディングが上手くいかないのでこうする
    if args.input == "-":
        df = pd.read_csv(sys.stdin, index_col=0)
    else:
        df = pd.read_csv(args.input, encoding=args.encoding, index_col=0)
    print(df)
    df.plot()

    if "ylabel" in args:
        plt.ylabel(args.ylabel,rotation=args.yrotation)
    show(args.output)


def show(file: str):
    if file == "-":
        plt.show()
    else:
        plt.savefig(file)


def main():
    # 引数のパース
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers()

    sub = sub_parser.add_parser("plot")
    #sub.add_argument("-t",
    #                 "--type",
    #                 choices=["csv", "tsv", "json"],
    #                 default="csv")
    sub.add_argument("-e", "--encoding", default="utf-8")
    sub.add_argument("-y", "--ylabel", type=str)
    sub.add_argument("--yrotation", type=int, default=90)
    sub.add_argument("input", nargs="?", type=str, default="-")
    sub.add_argument("output", nargs="?", type=str, default="-")
    sub.set_defaults(func=plot)

    args = parser.parse_args()
    # set seaborn style
    sns.set()
    sns.set_style("whitegrid", {"grid.linestyle": "--"})
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams['font.sans-serif'] = [
        'Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao',
        'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP'
    ]
    # 実行
    args.func(args)


if __name__ == "__main__":
    main()
