#! /bin/bash
sudo killall -9 iperf
sleep 3
sudo killall -9 python
sleep 3
sudo killall -9 tcpdump
sleep 3
sudo killall -9 sleep
sleep 3
nohup python daemonServer.py



#declare -i i=1
#while ((i<2))
#do
#  nohup python daemonServer.py
#  sleep 86400
#  sudo killall -9 iperf
#  sleep 5
#  sudo killall -9 python
#  sleep 5
#  sudo killall -9 tcpdump
#  sleep 5 
#  echo 1
#done
      
