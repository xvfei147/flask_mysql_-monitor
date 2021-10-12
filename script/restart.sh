ps auxf | grep monitor_server.py | grep -v "grep" | awk '{print "kill -9 " $2}' | bash
# 改为monitor_server的绝对路径
nohup python3 ,,/monitor_server.py &
