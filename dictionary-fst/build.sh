#!/bin/bash
hfst-lexc dict.lexc -o dict.hfst
hfst-fst2fst -O -i dict.hfst -o dict.hfstol