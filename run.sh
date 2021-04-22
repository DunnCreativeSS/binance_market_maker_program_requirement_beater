#!/bin/bash

while :
do
OUTPUT=$(ps -aux | grep -cE "market_maker.py")

if (( OUTPUT > 1 )); then
    echo "python3 is running"
	sleep 30s
else
    echo "python3 is not running"
	
    sudo nohup python3.7  market_maker.py MQsPcSHk1AZ96FQSUlScuZHZFSITb10TrUeuNXQuq2zF5IgsZefp7p3noI4ZOVST &
fi


done
