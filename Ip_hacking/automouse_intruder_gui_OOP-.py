import pyautogui
import time
import os

class CommandExecutor:
    def __init__(self, selected_command):
        self.commands = [
            "msconfig",   # 시스템 구성 유틸리티 실행
            "control",    # 제어판 열기
            "taskmgr",    # 작업 관리자 열기
            "regedit",    # 레지스트리 편집기 실행
            "explorer",   # 파일 탐색기 열기
            "ipconfig"    # IP 구성 정보
        ]
        self.selected_command = selected_command  # 실행할 명령어

    def execute_command(self):
        """선택된 명령어를 실행하는 함수"""
        # 실행 창 열기 (Win + R)
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
        file_path = f"C:\\Users\\dolch\\Desktop\\python\\mini_project\\ip_hacking\\{self.selected_command}.txt"
        pyautogui.write(f"{self.selected_command} > {file_path}")
        time.sleep(1)
        pyautogui.press("enter")

# 객체 생성 후 실행
executor = CommandExecutor("msconfig")  # 실행할 명령어 선택
executor.execute_command()
