import pygame
import math

''' 컴퓨터공학부 202011353 이호은 '''
if __name__ == "__main__":
    pygame.init()

    SCR_WIDTH = 1200
    SCR_HEIGHT = 800

    POWER = 150
    RAW_ANGLE = 90
    ANGLE = math.radians(RAW_ANGLE)

    UP_DOWN_KEY_FLAG = 1
    LEFT_RIGHT_KEY_FLAG = 0
    BALL_FLAG = 0

    # 게임 진행 변수
    remain = 9
    HP = 10

    # 포물선 변수
    G = 9.8
    v0 = 0
    vX = 0
    vY = 0
    x = 0
    y = 0
    t = 0

    # 화면 설정
    size = [SCR_WIDTH, SCR_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Break The Wall")

    done = False
    clock = pygame.time.Clock()

    # 블록 배열 초기화
    arr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    while not done:
        clock.tick(30)

        # 닫기 버튼
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # 눌러진 키에 따른 FLAG 세팅
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    LEFT_RIGHT_KEY_FLAG = -1
                if event.key == pygame.K_RIGHT:
                    LEFT_RIGHT_KEY_FLAG = 1

                # 공 발사
                if event.key == pygame.K_SPACE:
                    if BALL_FLAG == 0:
                        # 포물선 변수 초기화
                        BALL_FLAG = 1
                        v0 = POWER / 3 + 30
                        x = 0
                        y = 0
                        t = 0
                        HP -= 1

            # 키가 더이상 눌러진 상태가 아니면 FLAG 0으로
            if event.type == pygame.KEYUP:
                LEFT_RIGHT_KEY_FLAG = 0

        # 파워 게이지 조정
        if UP_DOWN_KEY_FLAG == -1 and BALL_FLAG == 0:
            if POWER > 0:
                POWER -= 5
            if POWER == 0:
                UP_DOWN_KEY_FLAG = 1
        elif UP_DOWN_KEY_FLAG == 1 and BALL_FLAG == 0:
            if POWER < 300:
                POWER += 5
            if POWER == 300:
                UP_DOWN_KEY_FLAG = -1

        # 좌, 우 방향키 눌린 상태면
        if LEFT_RIGHT_KEY_FLAG == -1 and BALL_FLAG == 0:
            if RAW_ANGLE < 135:
                RAW_ANGLE += 5
        elif LEFT_RIGHT_KEY_FLAG == 1 and BALL_FLAG == 0:
            if RAW_ANGLE > 45:
                RAW_ANGLE -= 5

        # 배경
        screen.fill((255, 255, 255))

        # 남은 개수 세기
        for i in range(3):
            for j in range(3):
                if arr[i][j] == 0:
                    remain += 1

        # POWER 출력
        font_20 = pygame.font.Font(pygame.font.get_default_font(), 20)
        remain_text = font_20.render("REMAIN : ", True, (0, 0, 0))
        remain_num_text = font_20.render(str(remain), True, (0, 0, 0))
        screen.blit(remain_text, (50, 50))
        screen.blit(remain_num_text, (160, 50))

        # HP 출력
        font_20 = pygame.font.Font(pygame.font.get_default_font(), 20)
        remain_text = font_20.render("HEART : ", True, (0, 0, 0))
        remain_num_text = font_20.render(str(HP), True, (0, 0, 0))
        screen.blit(remain_text, (1000, 50))
        screen.blit(remain_num_text, (1100, 50))

        # 남은 블록 0개이면 승리
        if remain == 0:
            screen.fill((255, 255, 255))
            font_big = pygame.font.Font(pygame.font.get_default_font(), 50)
            end_text = font_big.render("VICTORY!!", True, (0, 0, 0))
            screen.blit(end_text, (500, 300))

        remain = 0

        # 각도 조절
        ANGLE = math.radians(RAW_ANGLE)
        pygame.draw.line(screen, (50, 50, 50), [600, 800], [600 + 80 * math.cos(ANGLE), 800 - 80 * math.sin(ANGLE)], 10)

        # POWER 조절
        pygame.draw.rect(screen, (200, 200, 200), [1200 - 80, 800 - 330, 50, 300])
        pygame.draw.rect(screen, (255, 100, 100), [1120, 770 - POWER, 50, POWER])

        # 공 그리기
        if BALL_FLAG == 1:
            x = v0 * math.cos(ANGLE) * t
            y = v0 * math.sin(ANGLE) * t - (0.5 * G * t * t)
            print(x, y)

            pygame.draw.circle(screen, (100, 100, 100), [600 + int(x), 800 - int(y)], 20)
            t += 1

            # 블럭 통과 체크
            if 540 >= 600 + int(x) >= 460 and 140 >= 800 - int(y) >= 60:
                arr[0][0] = 1
            if 640 >= 600 + int(x) >= 560 and 140 >= 800 - int(y) >= 60:
                arr[1][0] = 1
            if 740 >= 600 + int(x) >= 660 and 140 >= 800 - int(y) >= 60:
                arr[2][0] = 1

            if 540 >= 600 + int(x) >= 460 and 240 >= 800 - int(y) >= 160:
                arr[0][1] = 1
            if 640 >= 600 + int(x) >= 560 and 240 >= 800 - int(y) >= 160:
                arr[1][1] = 1
            if 740 >= 600 + int(x) >= 660 and 240 >= 800 - int(y) >= 160:
                arr[2][1] = 1

            if 540 >= 600 + int(x) >= 460 and 340 >= 800 - int(y) >= 260:
                arr[0][2] = 1
            if 640 >= 600 + int(x) >= 560 and 340 >= 800 - int(y) >= 260:
                arr[1][2] = 1
            if 740 >= 600 + int(x) >= 660 and 340 >= 800 - int(y) >= 260:
                arr[2][2] = 1

            # 공이 화면 밖으로 떨어지면
            if y < 0:
                BALL_FLAG = 0
                x = 0
                y = 0
                v0 = 0

        # 블럭
        for i in range(3):
            for j in range(3):
                if arr[i][j] == 0:
                    pygame.draw.rect(screen, (0, 0, 0), [460 + i * 100, 60 + j * 100, 80, 80], 3)

        # 생명
        if HP == 0:
            screen.fill((255, 255, 255))
            font_big = pygame.font.Font(pygame.font.get_default_font(), 50)
            end_text = font_big.render("FAIL!!", True, (0, 0, 0))
            screen.blit(end_text, (500, 300))

        pygame.display.flip()

    pygame.quit()
