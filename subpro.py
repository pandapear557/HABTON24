import subprocess
import sys

# 현재 인터프리터 경로
current_interpreter = sys.executable

# 다른 인터프리터 경로 (예: /usr/bin/python3.8)
new_interpreter = "/Users/seohyeongjun/.pyenv/shims/python"
gui = "/Users/seohyeongjun/opt/anaconda3/envs/habton"

# imagine.py 실행
subprocess.run([new_interpreter, "midj_prop.py"])
subprocess.run([gui, "main_lic.py"])
