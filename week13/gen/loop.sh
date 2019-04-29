#!/bin/bash

rm -rf benchmarks
rm -rf out
mkdir benchmarks
mkdir out
cp ../../gen/test*.in benchmarks

BINARY="python3 tap.py"
# BINARY="./tap"
# BINARY="./test"
# BINARY="./sucker"

for i in {1..15}
do
    { /usr/bin/time -v $BINARY benchmarks/test$i.in out/test$i.out ; } 2>&1 | gawk '/Elapsed \(wall clock\) time \(h:mm:ss or m:ss\):/ { printf("%s\t| ", $NF) }'
    ../../gen/eval.py benchmarks/test$i.in out/test$i.out | gawk -F ':' '/^max dist/ {a = $2} /^clone/ {b = $2} /^max load/ {c = $2} /^hpwl/ {d = $2} /^score/ {e = $2} END {print a "\t| " b "\t| " c "\t| " d "\t| " e}'
done

