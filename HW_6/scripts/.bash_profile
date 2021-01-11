#!/bin/bash
a=$(awk 'END{print NR}' ~/.data/quotes.csv)
a=$[a-1]
a=$(shuf -i 1-$a -n 1)
a=$(sed -n "${a}p" ~/.data/quotes.csv)

echo $a | cut -d ',' -f2-
b=$(echo $a | cut -d ',' -f1 | tr -d '"')
echo "             ~ $b"