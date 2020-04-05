#!/usr/bin/env python3
# coding: utf-8
# これなに？→HWiNFOで取得したデータをpyaphで扱えるようにする奴

import os
import sys
import csv
import argparse
from collections import namedtuple
from datetime import datetime


def date_hwinfo(date: str, time: str) -> float:
    d = date.split(".")
    if len(d) == 1:
        return None

    t = time.split(":")
    s = t[2].split(".")

    # TimeZoneは必要ない
    # なぜなら、この時間は相対化にしか使わないから絶対的な値はどうでもいい
    return datetime(year=int(d[2]),
                    month=int(d[1]),
                    day=int(d[0]),
                    hour=int(t[0]),
                    minute=int(t[1]),
                    second=int(s[0]),
                    microsecond=int(s[1]) * 1000).timestamp()


def read_txbench(file: os.PathLike, row: int):
    Column = namedtuple("Column", ["elapsed", "value"])

    with open(file) as fp:
        # 3行読み飛ばす必要がある
        for _ in range(3):
            fp.readline()
        for value in csv.reader(fp):
            d = value[0].split(":")
            time = 0.0
            time += int(d[0]) * 3600
            time += int(d[1]) * 60
            time += int(d[2])
            time += float(d[3]) / 1000
            yield Column(time, value[row])


def read_hwinfo(file: os.PathLike, row: int):
    # ヘッダー飛ばさなくても変換結果で判断する
    #next(reader)
    Column = namedtuple("Column", ["elapsed", "value"])

    with open(file) as fp:
        first = None
        for value in csv.reader(fp):
            time = date_hwinfo(value[0], value[1])
            if time is None:
                continue

            elapsed = 0
            if first is None:
                first = time
            else:
                elapsed = time - first
            yield Column(elapsed, value[row])


def single(file: str, row: int, read_method):
    print(f" 秒 ,{os.path.basename(file)}")
    for v in read_method(file, row):
        print(f"{v.elapsed},{v.value}")


def multi(files: list, row: int, read_method):
    CSV = namedtuple("CSV", ["file", "csv"])
    reader = []
    # 指定されたファイルを全て読む
    for file in files:
        reader.append(CSV(os.path.basename(file), read_method(file, row)))

    # 配列に入れてソート
    Value = namedtuple("Value", ["index", "elapsed", "value"])
    values = []
    for i, j in enumerate(reader):
        for v in j.csv:
            values.append(Value(i, v.elapsed, v.value))
    values = sorted(values, key=lambda x: x.elapsed)

    # ヘッダー
    print(" 秒 ," + ",".join([v.file for v in reader]))

    # 出力
    value = [None] * len(reader)
    for v in values:
        value[v.index] = v.value
        # Noneが含まれるなら値がまだ
        if None in value:
            continue
        # 値アリなら出す
        print(str(v.elapsed) + "," + ",".join(value))


def calc(files: list, row: int):
    Value = namedtuple("Value", ["name", "value"])
    values = []
    for file in files:
        with open(file) as f:
            # ヘッダー/フッターを飛ばす必要があるので内包表記が使えない
            tmp = []
            for v in csv.reader(f):
                try:
                    tmp.append(float(v[row]))
                except ValueError:
                    continue
            values.append(Value(os.path.basename(file), tmp))

    # ヘッダー
    print("type," + ",".join([v.name for v in values]))
    # min
    print("min," + ",".join([str(min(v.value)) for v in values]))
    # max
    print("max," + ",".join([str(max(v.value)) for v in values]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c",
                        "--calc",
                        action="store_true",
                        help="Calculation mode")
    parser.add_argument("-r",
                        "--row",
                        type=int,
                        default=2,
                        help="Select row (0 started)")
    parser.add_argument("-t",
                        "--type",
                        type=str,
                        choices=["hwinfo", "txbench"],
                        default="hwinfo",
                        help="Select data type.")
    parser.add_argument("file", nargs="+", help="CSV file")
    args = parser.parse_args()

    if args.type == "hwinfo":
        reader = read_hwinfo
    elif args.type == "txbench":
        reader = read_txbench

    if args.calc:
        calc(args.file, args.row)
    elif len(args.file) == 1:
        # 実はmultiでできるんだけど……
        single(args.file[0], args.row, reader)
    else:
        multi(args.file, args.row, reader)


if __name__ == "__main__":
    main()
