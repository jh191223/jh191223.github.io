import pyautogui
import time
import tkinter as tk

# Tkinter 창 설정
root = tk.Tk()
root.title("System Info Control with Tkinter & Automouse")
root.geometry("400x500")

# Listbox 생성
listbox = tk.Listbox(root, selectmode=tk.SINGLE)
listbox.pack(pady=20)

# 명령어 리스트 추가
commands = [
    "msconfig",       # 시스템 구성 유틸리티 실행
    "control",        # 제어판 열기
    "taskmgr",        # 작업 관리자 열기
    "regedit",        # 레지스트리 편집기 실행
    "explorer",       # 파일 탐색기 열기
    "ipconfig"
]

for command in commands:
    listbox.insert(tk.END, command)

# 선택한 명령어를 실행하는 함수
def execute_command():
    selected_index = listbox.curselection()  # 선택된 항목의 인덱스 가져오기
    if selected_index:
        selected_command = listbox.get(selected_index)  # 선택된 명령어 가져오기
        label.config(text=f"실행 중: {selected_command}")  # 실행 상태 표시

        # Window + R 눌러 실행 창 열기
        pyautogui.keyDown('winleft')
        pyautogui.press('r')
        pyautogui.keyUp('winleft')
        time.sleep(1)

        pyautogui.write("cmd")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(2)

        # 선택한 명령어 입력 후 실행
        pyautogui.write(selected_command+f" > {selected_command}.txt")
        time.sleep(1)
        pyautogui.press("enter")


# 실행 상태 표시 레이블
label = tk.Label(root, text="선택된 명령어: 없음")
label.pack()

# 실행 버튼 추가
button = tk.Button(root, text="선택한 명령어 실행", command=execute_command)
button.pack(pady=20)

# Tkinter 실행
root.mainloop()

# 질문 사항 
# 이제 해킹의 경우, 취약점 파악 -> 권한 획득 -> 백도어 설치-> 침입 흔적 제거
# 어떤 방식이 있을지와, 구현 방향 및  백도어 설치-> 침입 흔적 제거 두 부분 Q&A
