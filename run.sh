#!/bin/bash

time python ~/thesis-code/src/Main.py -p $1 > stdout 2> stderr < /dev/null &
