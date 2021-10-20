# 用于执行linux cron表达式 配置的本项目脚本
# 30 0 * * * /usr/local/bin/python3 /home/dhph/python_workspace/dh_account_check/execute_py_for_cron.py check_customer &>/home/dhph/logs/check_customer.log 2>&1
# 15 0 24 4 * /usr/local/bin/python3 /home/dhph/python_workspace/dh_account_check/execute_py_for_cron.py check_borrower &>/home/dhph/logs/check_borrower.log 2>&1
from service import check_lender_to_save as lender
from service import check_borrower_to_save as borrower
import sys

if len(sys.argv) > 1:
    start_py = sys.argv[1]
    if start_py == 'check_customer':
        print("开始启动用户账户核对")
        lender.main()
    if start_py == 'check_borrower':
        print("开始启动借款用户账户核对")
        borrower.main()
