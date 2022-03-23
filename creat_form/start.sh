#!/bin/bash
if [ ! -n "$1" ] ;then
    echo "please input command like './start.sh CWE416'"
    exit 1
fi
cd /home/weihaolai/joern-0.3.1
rm -rf .joernIndex

java -jar bin/joern.jar /home/weihaolai/ICKD_analysis/data_list/$1

cd ~
cd /home/weihaolai/usr/Neo4j/neo4j-community-2.1.8/bin
./neo4j console
