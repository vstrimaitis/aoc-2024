#!/bin/bash
set -e
if [[ $# -eq 0 ]] ; then
    echo "Usage: ./new_day.sh <day_number>"
    exit 1
fi

export DAY="$1"
export YEAR="2024"
DAY_FORMATTED=$(printf "%02d" $DAY)
TEMPLATES_FOLDER="templates"
INPUT_FILE="inputs/$DAY_FORMATTED.txt"

aocd > $INPUT_FILE
echo "First few lines of the input:"
head $INPUT_FILE
PURPLE='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'
LINE_COUNT="$(wc -l $INPUT_FILE | awk '{ print $1 }')"
BYTE_COUNT="$(wc -c $INPUT_FILE | awk '{ print $1 }')"
echo -e "${PURPLE}# of lines in the input: ${BOLD}${LINE_COUNT}${NC}"
echo -e "${PURPLE}# of bytes in the input: ${BOLD}${BYTE_COUNT}${NC}"

# Prepare Python solution
PYTHON_TARGET_FOLDER="python/$DAY_FORMATTED"
PYTHON_TEMPLATE_FOLDER="$TEMPLATES_FOLDER/python"

if [[ -d $PYTHON_TARGET_FOLDER ]] ; then
    read -p "Directory $PYTHON_TARGET_FOLDER already exists. Overwrite? (y/n) " yn
    case $yn in
        [Yy]* ) rm -rf $PYTHON_TARGET_FOLDER;;
        * ) echo "Exiting"; exit 0;;
    esac
fi

cp -r $PYTHON_TEMPLATE_FOLDER $PYTHON_TARGET_FOLDER

for filename in $PYTHON_TARGET_FOLDER/*; do
    tmpfile=$(mktemp)
    cp $filename $tmpfile
    envsubst < $filename > $tmpfile
    mv $tmpfile $filename
done

# fetch examples
cd $PYTHON_TARGET_FOLDER
python fetch_examples.py
