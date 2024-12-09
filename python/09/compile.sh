#!/bin/bash
set -e

g++-12 -O2 -std=c++17 -Wl,-stack_size -Wl,20000000 main.cpp -o main
