#!/usr/bin/env bash

echo 'contents of config.json before overwrite:'
cat config.json
cp config.template.json config.json
echo "" > template.csv

pipenv run python main.py 1

today=$(date '+%y-%m-%d')
expected=$(printf "date,value\r\n%s,1\r\n" "$today")
given=$(cat template.csv)
if [[ "$given" == "$expected" ]]; then
    echo "OK"
else
    echo "End-to-end test failed."
    printf "got\n%s" "$given"
    printf "but expected\n%s" "$expected"
    exit 1
fi
