import pygame
import sys
import time

FPS = 60
MAX_WIDTH = 600
MAX_HEIGHT = 400

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))

# 배경 이미지 로드
background = pygame.image.load("./점프게임/배경사진모음/봄_벚꽃_사진.jpg")
background = pygame.transform.scale(background, (MAX_WIDTH, MAX_HEIGHT))  # 화면 크기 조정

# 캐릭터 이미지 로드
player_img = pygame.image.load("./점프게임/player모음/squarrel.jpg")
player_img = pygame.transform.scale(player_img, (40, 40))  # 캐릭터 크기 조정

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isJump = False
        self.jumpCount = 10
        self.rect = pygame.Rect(self.x, self.y, 40, 40)  # 플레이어의 rect 객체
        self.last_jump_time = None  # 마지막 점프 시간 기록
        self.jump_intervals = []  # 점프 간격 기록 (매크로 감지용)

    def draw(self):
        screen.blit(player_img, (self.x, self.y))  # 캐릭터 이미지 그리기
        self.rect.topleft = (self.x, self.y)  # rect의 위치 업데이트

    def jump(self):
        if self.isJump:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount**2 * 0.7 * neg 
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10

#### 중력 구현 ####
# def jump(self):
#     if self.isJump:
#         # 올라갈 때 점프 강도를 줄여가며
#         if self.jumpCount >= 0:
#             self.y -= (self.jumpCount ** 2) * 0.7  # 올라갈 때
#         else:
#             # 내려갈 때 속도 증가
#             self.y += (self.jumpCount ** 2) * 0.7  # 내려갈 때

#         # 점프 카운트 업데이트
#         self.jumpCount -= 1

#         # 점프가 끝나면 리셋
#         if self.jumpCount == -11:
#             self.isJump = False
#             self.jumpCount = 10

    def record_jump_time(self):
        """ 점프 간격을 기록하여 일정한 패턴인지 분석 """
        current_time = time.time()
        if self.last_jump_time is not None:
            interval = round(current_time - self.last_jump_time, 3)  # 간격을 소수점 3자리로 저장
            self.jump_intervals.append(interval)

            # 최근 10번의 점프 패턴이 일정하면 매크로로 판단
            if len(self.jump_intervals) > 10:
                self.jump_intervals.pop(0)  # 가장 오래된 기록 제거

                # 변동이 거의 없는 경우 (0.1초 이하 차이)  
                if max(self.jump_intervals) - min(self.jump_intervals) < 0.1:
                    print("⚠️ 매크로 감지됨! 경고 후 종료")
                    pygame.quit()
                    sys.exit()

        self.last_jump_time = current_time  # 마지막 점프 시간 갱신

class Enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 20, 40)  # 적의 rect 객체
        
    def draw(self):
        return pygame.draw.rect(screen, (255, 0, 0), self.rect)  # 적은 빨간색으로 그리기
    
    def move(self, speed):
        self.x -= speed
        self.rect.x = self.x  # 적의 rect 위치 업데이트
        if self.x <= 0:
            self.x = MAX_WIDTH
            self.rect.x = self.x  # 재시작 시 적의 rect 위치 업데이트

player = Player(50, MAX_HEIGHT - 40)
enemy = Enemy(MAX_WIDTH, MAX_HEIGHT - 40)

macro_enabled = False  # 매크로 기능 초기 상태: OFF

def main():
    global macro_enabled
    speed = 7

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # 'M' 키로 매크로 모드 ON/OFF
                    macro_enabled = not macro_enabled
                    print(f"🟢 매크로 모드: {'ON' if macro_enabled else 'OFF'}")
                if not macro_enabled and event.key == pygame.K_SPACE:  # 매크로 OFF 상태에서 수동 점프
                    player.isJump = True

        # 배경 이미지 그리기
        screen.blit(background, (0, 0))  # 배경을 화면에 그리기

        # 매크로가 활성화되었을 때만 자동 점프
        if macro_enabled and not player.isJump:
            if enemy.x - player.x < 100 and enemy.x - player.x > 0:  # 장애물이 100픽셀 이내로 가까워졌을 때
                player.isJump = True  # 점프 시작
                player.record_jump_time()  # 점프 시간 기록 (매크로 감지용)

        clock.tick(FPS)
        
        player.draw()  # 플레이어 그리기
        player.jump()

        enemy.draw()  # 적 그리기
        enemy.move(speed)
        speed += 0.01  # enemy가 빨라짐

        # 충돌 체크
        if player.rect.colliderect(enemy.rect):  # player_rect와 enemy_rect 비교
            print("충돌")
            pygame.quit()  # 게임 종료
            sys.exit()

        pygame.display.update()

if __name__ == '__main__':
    main()


## *** 추가프로젝트 *** 
## 기준점 변동에따른 세밀도 분석 추가 프로젝트 => line 77
## 매크로를 껐다 켰다 하면서 하는 경우 macro 분석이 어렵지 않을까
## 일정 시간에 따라 난이도 변경 및 배경 변경