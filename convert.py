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
        reader = csv.reader(f)
        next(reader)
        d = read(reader)
        print(" 秒 ,温度")
        for v in d:
            print(f"{v[0]},{v[1]}")


def double(file1: str, file2: str):
    with open(file1) as f1, open(file2) as f2:
        r1 = csv.reader(f1)
        r2 = csv.reader(f2)
        next(r1)
        next(r2)
        t1 = read(r1)
        t2 = read(r2)

        d = []
        for v in t1:
            d.append({"time": v[0], "temp1": v[1]})
        for v in t2:
            d.append({"time": v[0], "temp2": v[1]})
        s = sorted(d, key=lambda x: x["time"])

        v1 = None
        v2 = None
        print(" 秒 ,温度1,温度2")
        for v in s:
            if "temp1" in v:
                v1 = v["temp1"]
            if "temp2" in v:
                v2 = v["temp2"]

            if (v1 is not None) and (v2 is not None):
                t = v["time"]
                print(f"{t},{v1},{v2}")


def main():
    if len(sys.argv) == 0:
        print(f"Usage: {sys.argv[0]} <single/double> [file]")
        sys.exit(1)

    if sys.argv[1] == "single":
        single(sys.argv[2])
    elif sys.argv[1] == "double":
        double(sys.argv[2], sys.argv[3])
    else:
        single(sys.argv[1])


if __name__ == "__main__":
    main()
