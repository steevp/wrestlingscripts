#!/bin/sh
set -e
awk '{print $1}' list.txt | xargs -n 1 -P 10 wget -c
while read url filename; do
  mv -v "${url##*/}" "$filename"
done < list.txt
