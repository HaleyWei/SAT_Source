#!/bin/bash
if [ ! -n "$1" ] ;then
    echo "please input command like './piao.sh CWE416'"
    exit 1
fi

inPath="/home/weihaolai/ICKD_analysis/data_list/$1/*"
outPath="/home/weihaolai/ICKD_analysis/data_CVE/$1/code/"
exPath="/home/weihaolai/ICKD_analysis/data_CVE/$1/code"


if [ -d "$exPath" ]; then
	echo "代码目录已存在"
        rm -rf $exPath
        echo "代码目录删除成功"
	mkdir -p $exPath
else
	mkdir -p $exPath
fi

cp -r $inPath $outPath
echo "creat database success"

python finish.py $1
python pointer_change.py $1
python unsafe_pointer.py $1
python unsafe_op.py $1
#python dp.py $1
#python unsafe_line.py $1
#python all_path.py $1
#python vulnerable_search.py $1

