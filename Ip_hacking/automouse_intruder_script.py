import pyautogui
import time
import os

# 명령어 리스트
commands = [
    "msconfig",       # 시스템 구성 유틸리티 실행
    "control",        # 제어판 열기
    "taskmgr",        # 작업 관리자 열기
    "regedit",        # 레지스트리 편집기 실행
    "explorer",       # 파일 탐색기 열기
    "ipconfig"        # IP 구성 정보
]

# 명령어 선택 (여기서는 0번 명령어를 선택한 것으로 예시)
selected_command = commands[0]  # 예를 들어 "msconfig" 명령어를 선택한 것처럼

# 선택된 명령어를 실행하는 함수
def execute_command(selected_command):
    # Window + R 눌러 실행 창 열기
    pyautogui.keyDown('winleft')
    pyautogui.press('r')
    pyautogui.keyUp('winleft')
    time.sleep(1)

    # "cmd" 입력 후 실행
    pyautogui.write("cmd")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)

    # 선택한 명령어 입력 후 실행
    file_path = f"C:\\Users\\dolch\\Desktop\\python\\mini_project\\ip_hacking\\{selected_command}.txt"
    pyautogui.write(f"{selected_command} > {file_path}")
    time.sleep(1)
    pyautogui.press("enter")

# 선택된 명령어 실행
execute_command(selected_command)
