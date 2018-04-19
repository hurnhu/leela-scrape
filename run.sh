#!/bin/bash
i=1
while [ $i -le $(($2 - $3)) ]
do
  echo $i
  echo $(($i + $3))
  xvfb-run -a python3 scrape.py --start=$i --end=$(($i + $3)) &
  sleep 30
  i=$(($i + $3))
  #echo $i
done
