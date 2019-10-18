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
        plt.ylabel(args.ylabel, rotation=args.yrotation)
    show(args.output)


def bar(args: argparse.Namespace):
    df = None
    # ArgParseのFileTypeを使うとエンコーディングが上手くいかないのでこうする
    if args.input == "-":
        df = pd.read_csv(sys.stdin, index_col=0)
    else:
        df = pd.read_csv(args.input, encoding=args.encoding, index_col=0)
    print(df)
    df.plot.barh()
    #plt.legend(loc='upper left')
    #plt.legend(bbox_to_anchor=(0, -0.1,1,0), loc='upper left', frameon=False,ncol=2)

    if args.under:
        plt.legend(bbox_to_anchor=(0, -0.1),
                   loc='upper left',
                   frameon=False,
                   ncol=2)
    if args.ylabel:
        plt.ylabel(None)
    if "xlabel" in args:
        plt.xlabel(args.xlabel)
    show(args.output)


def style(args: argparse.Namespace):
    # set seaborn style
    sns.set()
    sns.set_style("whitegrid", {"grid.linestyle": "--"})
    # set font
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams['font.sans-serif'] = [
        'Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao',
        'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP'
    ]
    # set size
    if args.size is not None:
        size = args.size.split(",")
        x = y = int(size[0])
        if len(size) >= 2:
            y = int(size[1])
        plt.rcParams["figure.figsize"] = (pixel2inch(x), pixel2inch(y))


def show(file: str):
    plt.tight_layout()
    if file == "-":
        plt.show()
    else:
        plt.savefig(file)


def pixel2inch(pixel: int, dpi: int = 100) -> float:
    return pixel / dpi


def main():
    # 引数のパース
    parser = argparse.ArgumentParser()
    parser.add_argument("-s",
                        "--size",
                        type=str,
                        help="set size. (eg: 640,480)")
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

    sub = sub_parser.add_parser("bar")
    sub.add_argument("-e", "--encoding", default="utf-8")
    sub.add_argument("-x", "--xlabel", type=str)
    sub.add_argument("-y", "--ylabel", action="store_false")
    sub.add_argument("-u", "--under", action="store_true")
    sub.add_argument("input", nargs="?", type=str, default="-")
    sub.add_argument("output", nargs="?", type=str, default="-")
    sub.set_defaults(func=bar)

    args = parser.parse_args()
    # 実行
    style(args)
    args.func(args)


if __name__ == "__main__":
    main()
