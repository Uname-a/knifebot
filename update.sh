#!/bin/bash
localPATH=`pwd`                                         # path of current directory
sep='---------------'                                   
while true; do
  echo $sep"Processing" $d$sep
  git pull origin master
  echo -e "\n"
  sleep 30
done
