#!/usr/bin/env python3
# coding: utf-8

import sys
import csv
from datetime import datetime, timedelta, timezone

tz = timezone(timedelta(hours=+9), 'JST')


def date2sec(day: str, time: str) -> float:
    d = day.split(".")
    if len(d) == 1:
        return None

    t = time.split(":")
    s = t[2].split(".")

    return datetime(year=int(d[2]),
                    month=int(d[1]),
                    day=int(d[0]),
                    hour=int(t[0]),
                    minute=int(t[1]),
                    second=int(s[0]),
                    microsecond=int(s[1]) * 1000,
                    tzinfo=tz).timestamp()


def read(reader):
    #　ヘッダー飛ばし
    next(reader)
    result = []

    first = None
    for row in reader:
        time = date2sec(row[0], row[1])
        if time is None:
            continue

        elapsed = 0
        if first is None:
            first = time
        else:
            elapsed = time - first
        result.append((elapsed, row[2]))
    return result


def single(file: str):
    with open(file) as f:
        print(" 秒 ,温度")
        for v in read(csv.reader(f)):
            print(f"{v[0]},{v[1]}")


def multi(files: list):
    reader = []
    # 指定されたファイルを全て読む
    for file in files:
        with open(file) as f:
            reader.append(read(csv.reader(f)))

    # 辞書配列に入れてソート
    d = []
    value = []
    for i, j in enumerate(reader):
        value.append(None)
        for v in j:
            d.append({"index": i, "time": v[0], "temp": v[1]})
    s = sorted(d, key=lambda x: x["time"])

    # ヘッダー
    print(" 秒 ", end="")
    for i in range(len(value)):
        print(f",温度{i+1}", end="")
    print("")
    # 出力
    for v in s:
        value[v["index"]] = v["temp"]
        # Noneが含まれるなら値がまだ
        if None in value:
            continue
        print(v["time"], end="")
        for n in value:
            print(f",{n}", end="")
            pass
        print("")


def main():
    if len(sys.argv) <= 1:
        print(f"Usage: {sys.argv[0]} [file...]")
        sys.exit(1)

    if len(sys.argv) == 2:
        single(sys.argv[1])
    else:
        sys.argv.pop(0)
        multi(sys.argv)


if __name__ == "__main__":
    main()
