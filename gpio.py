import RPi.GPIO as GPIO
import time

# 핀 셋팅을 BCM 방식으로 설정
GPIO.setmode(GPIO.BCM)

# warning을 끔
GPIO.setwarnings(False)

# 7 Segment 선택을 위한 변수 #노랑이
digit_minute_1 =
digit_minute_10 =
digit_hour_1 =
digit_hour_10 =

# 7 Segment 표현을 위한 변수
segA = 27
segB = 22
segC = 19
segD = 6
segE = 5
segF = 9
segG = 4

# 버튼을 위한 변수
button = 8

def initGPIO():
    # GPIO 핀 셋팅
    GPIO.setup(digit_hour_1, GPIO.OUT)
    GPIO.setup(digit_hour_10, GPIO.OUT)
    GPIO.setup(digit_minute_1, GPIO.OUT)
    GPIO.setup(digit_minute_10, GPIO.OUT)

    GPIO.setup(segA, GPIO.OUT)
    GPIO.setup(segB, GPIO.OUT)
    GPIO.setup(segC, GPIO.OUT)
    GPIO.setup(segD, GPIO.OUT)
    GPIO.setup(segE, GPIO.OUT)
    GPIO.setup(segF, GPIO.OUT)
    GPIO.setup(segG, GPIO.OUT)

    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def displaySegment(nowTime): #시간을 세그먼트에 표시
    for i in range(4):
        # 7시 50분의 경우 07:50으로 표시 되지 않고 7:50 으로 표시 되기 위해 예외처리
        if i == 3 and nowTime == 0:
            break

        # 세그먼트에 숫자를 표시 (맨 끝수)
        setSegmentNumber(nowTime % 10)

        # 전원을 넣어줄 세그먼트를 선택
        if i == 0:
            GPIO.output(digit_minute_1, True)
        elif i == 1:
            GPIO.output(digit_minute_10, True)
        elif i == 2:
            GPIO.output(digit_hour_1, True)
        elif i == 3:
            GPIO.output(digit_hour_10, True)

        # LED를 표시하기 위해 딜레이
        time.sleep(0.001)

        # 모든 세그먼트를 끔
        GPIO.output(digit_minute_1, False)
        GPIO.output(digit_minute_10, False)
        GPIO.output(digit_hour_1, False)
        GPIO.output(digit_hour_10, False)

        # 끝수를 버림
        nowTime = int(nowTime / 10)


# 7 세그먼트를 사용하므로 넣은 숫자에 따라 세그먼트에 수를 표시 #False 끄기 True 켜기
def setSegmentNumber(num):
    if num == 0:
        GPIO.output(segA, False)
        GPIO.output(segB, False)
        GPIO.output(segC, False)
        GPIO.output(segD, False)
        GPIO.output(segE, False)
        GPIO.output(segF, False)
        GPIO.output(segG, True)
    elif num == 1:
        GPIO.output(segA, True)
        GPIO.output(segB, False)
        GPIO.output(segC, False)
        GPIO.output(segD, True)
        GPIO.output(segE, True)
        GPIO.output(segF, True)
        GPIO.output(segG, True)
    elif num == 2:
        GPIO.output(segB, False)
        GPIO.output(segA, False)
        GPIO.output(segC, True)
        GPIO.output(segD, False)
        GPIO.output(segE, False)
        GPIO.output(segF, True)
        GPIO.output(segG, False)
    elif num == 3:
        GPIO.output(segA, False)
        GPIO.output(segB, False)
        GPIO.output(segC, False)
        GPIO.output(segD, False)
        GPIO.output(segE, True)
        GPIO.output(segF, True)
        GPIO.output(segG, False)
    elif num == 4:
        GPIO.output(segA, True)
        GPIO.output(segB, False)
        GPIO.output(segC, False)
        GPIO.output(segD, True)
        GPIO.output(segE, True)
        GPIO.output(segF, False)
        GPIO.output(segG, False)
    elif num == 5:
        GPIO.output(segA, False)
        GPIO.output(segB, True)
        GPIO.output(segC, False)
        GPIO.output(segD, False)
        GPIO.output(segE, True)
        GPIO.output(segF, False)
        GPIO.output(segG, False)
    elif num == 6:
        GPIO.output(segA, False)
        GPIO.output(segB, True)
        GPIO.output(segC, False)
        GPIO.output(segD, False)
        GPIO.output(segE, False)
        GPIO.output(segF, False)
        GPIO.output(segG, False)
    elif num == 7:
        GPIO.output(segA, False)
        GPIO.output(segB, False)
        GPIO.output(segC, False)
        GPIO.output(segD, True)
        GPIO.output(segE, True)
        GPIO.output(segF, True)
        GPIO.output(segG, True)
    elif num == 8:
        GPIO.output(segA, False)
        GPIO.output(segB, False)
        GPIO.output(segC, False)
        GPIO.output(segD, False)
        GPIO.output(segE, False)
        GPIO.output(segF, False)
        GPIO.output(segG, False)
    elif num == 9:
        GPIO.output(segA, False)
        GPIO.output(segB, False)
        GPIO.output(segC, False)
        GPIO.output(segD, False)
        GPIO.output(segE, True)
        GPIO.output(segF, False)
        GPIO.output(segG, False)
    elif num == 10:
        GPIO.output(segA, True)
        GPIO.output(segB, True)
        GPIO.output(segC, True)
        GPIO.output(segD, True)
        GPIO.output(segE, True)
        GPIO.output(segF, True)
        GPIO.output(segG, True)


def getButton():
    return button


# 시간 형식은 오전 7시 30분의 경우 730, 12시 20분의 경우 1220
def getTime12():
    # 시간을 가져옴
    now = time.localtime()
    hour = now.tm_hour
    minute = now.tm_min

    # 시는 0~12시로 표시
    hour = int(hour)
    if hour > 12:
        hour = hour - 12

    # 현재 시간 계산
    nowTime = hour * 100 + minute
    nowTime = int(nowTime)
    return nowTime


def getTime24():
    # 시간을 가져옴
    now = time.localtime()
    hour = now.tm_hour
    minute = now.tm_min

    # 현재 시간 계산
    hour = int(hour)
    nowTime = hour * 100 + minute
    nowTime = int(nowTime)
    return nowTime


# 버튼 인터럽트 테스트
def printTest(self):
    print("thread Test")


if __name__ == "__main__":

    try:
        initGPIO()
        while True:
            if not 'event' in locals():
                event = GPIO.add_event_detect(button, GPIO.FALLING, callback=printTest, bouncetime=1000)
            else:
                time.sleep(1)

        while True:
            color = 0

            nowTime = getTime12()
            '''
            # 시간을 세그먼트에 표시
            for i in range(500):
                # 버튼 실험
                if GPIO.input(button) == 0:
                    print("button pressed")
                    if color == 3:
                        color = 0
                    else:
                        color = color + 1
                setLED(color)
                displaySegment(nowTime)
            '''


    # ctrl + c 누르면 들어감 GPIO cleanup
    except KeyboardInterrupt:
        # GPIO 핀 초기화
        GPIO.cleanup()
    GPIO.cleanup()