#!/bin/bash

if [ ! -n "$1" ] ;then
    echo "please input command like './data_list.sh CWE121/s01'"
    exit 1
fi

outPath="/home/weihaolai/ICKD_analysis/creat_form/data/$1"

if [ -d "$outPath" ]; then
    echo "dir exist"    
    rm -rf $outPath
    echo "remove file done"
    mkdir -p $outPath
else
    mkdir -p $outPath
fi

cp /home/weihaolai/ICKD_analysis/exec_program/clean/$1/data/* $outPath
echo "copy xls done"

python var.py $1 &
python func.py $1 &
python op.py $1 &
python def.py $1 &
python def_use.py $1 &
python pointer.py $1 &
wait
echo "save xls done"
python get_array.py $1
echo "change xls done"
