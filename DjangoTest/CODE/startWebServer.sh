#! /bin/bash
declare -i i=1
while ((i<2))
do
  nohup python daemonServer.py &
  sleep 5
  nohup python daemonPassive.py &
  sleep 86400
  sudo killall -9 iperf
  sleep 5
  sudo killall -9 python
  sleep 5
  sudo killall -9 tcpdump
  sleep 5 
  echo 1
done
      
