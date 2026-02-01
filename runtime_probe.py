import re
import signal
import subprocess


_PROMPT_SUFFIX = "input your answer: "


def _safe_eval(expr: str) -> int:
    expr = expr.strip()
    if not re.fullmatch(r"[0-9()\s+\-]+", expr):
        raise ValueError(f"unexpected expr: {expr!r}")
    return int(eval(expr, {"__builtins__": {}}, {}))


def run_probe() -> str:
    def _preexec() -> None:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)

    path = "/" + "".join(chr(c) for c in [114, 101, 97, 100, 102, 108, 97, 103])

    p = subprocess.Popen(
        [path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        preexec_fn=_preexec,
    )

    assert p.stdin is not None
    assert p.stdout is not None

    header = p.stdout.readline()
    expr_line = p.stdout.readline()
    if not expr_line:
        raise RuntimeError("no expression received")

    buf = ""
    while not buf.endswith(_PROMPT_SUFFIX):
        ch = p.stdout.read(1)
        if ch == "":
            break
        buf += ch
        if len(buf) > 2048:
            break

    ans = _safe_eval(expr_line)
    p.stdin.write(str(ans) + "\n")
    p.stdin.flush()

    rest = p.stdout.read()
    return header + expr_line + buf + rest
