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

    # 最高値に注釈付ける奴(値でmaxを取って注釈？)
    if "ylabel" in args:
        plt.ylabel(args.ylabel, rotation=args.yrotation)
    if "title" in args:
        plt.title(args.title)
    show(args.output)


def bar(args: argparse.Namespace):
    df = None
    # ArgParseのFileTypeを使うとエンコーディングが上手くいかないのでこうする
    if args.input == "-":
        df = pd.read_csv(sys.stdin, index_col=0)
    else:
        df = pd.read_csv(args.input, encoding=args.encoding, index_col=0)
    print(df)
    ax = df.plot.barh()
    #plt.legend(loc="upper left")
    #plt.legend(bbox_to_anchor=(0, -0.1,1,0), loc="upper left", frameon=False,ncol=2)

    # 注釈
    if args.annotate:
        for p in ax.patches:
            width = p.get_width()
            x = width
            y = p.get_y() + p.get_height() / 4.5  # TODO: 4.5は決め打ち、データが2個の時用
            if args.inside:
                # 内側注釈
                ax.annotate(str(width),
                            xy=(x - 0.25, y),
                            color="#ffffff",
                            ha="right",
                            weight="medium")
            else:
                ax.annotate(str(width), xy=(x + 0.25, y))
    # 凡例位置
    if args.under:
        plt.legend(bbox_to_anchor=(0, -0.1),
                   loc="upper left",
                   frameon=False,
                   ncol=2)
    else:
        # 凡例の向きを合わせる
        handles, labels = ax.get_legend_handles_labels()
        plt.legend(handles[::-1], labels[::-1])
    # ラベルとタイトル
    if args.ylabel:
        plt.ylabel(None)
    if "xlabel" in args:
        plt.xlabel(args.xlabel)
    if "title" in args:
        plt.title(args.title)
    show(args.output)


def style(args: argparse.Namespace):
    # set seaborn style
    sns.set()
    sns.set_style("whitegrid", {"grid.linestyle": "--"})
    # set font
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = [
        "Hiragino Maru Gothic Pro", "Yu Gothic", "Meiryo", "Takao",
        "IPAexGothic", "IPAPGothic", "VL PGothic", "Noto Sans CJK JP"
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
        #bbox_inches="tight", pad_inches=0.05


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
    sub.add_argument("-t", "--title", type=str)
    sub.add_argument("input", nargs="?", type=str, default="-")
    sub.add_argument("output", nargs="?", type=str, default="-")
    sub.set_defaults(func=plot)

    sub = sub_parser.add_parser("bar")
    sub.add_argument("-e", "--encoding", default="utf-8")
    sub.add_argument("-x", "--xlabel", type=str)
    sub.add_argument("-y", "--ylabel", action="store_false")
    sub.add_argument("-u", "--under", action="store_true")
    sub.add_argument("-t", "--title", type=str)
    sub.add_argument("-a", "--annotate", action="store_false")
    sub.add_argument("--inside", action="store_true")
    sub.add_argument("input", nargs="?", type=str, default="-")
    sub.add_argument("output", nargs="?", type=str, default="-")
    sub.set_defaults(func=bar)

    args = parser.parse_args()
    # 実行
    style(args)
    args.func(args)


if __name__ == "__main__":
    main()
