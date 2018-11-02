from data import find_weather
from IO import recordMic,playAudio
from google_api import tts,stt

import sys
import os
import threading
import time

#GPIO interrupt를 위한 모듈
import RPi.GPIO as GPIO

# 알람들의 리스트가 저장
alarm_list=[]

# input으로 받는 time의 형식은 7시 30분이면 730, 12시 20분이면 1220
def alarm_add(time):
    global alarm_list
    alarm_list.append(time)

def alarm_remove(time):
    global alarm_list
    if time in alarm_list:
        alarm_list.remove(time)
        return True
    else:
        return False

# 알람을 관리해 줄 쓰레드
def alarm_manage(order):
    hourIndex = order.find('시')
    minIndex = order.find('분')


    time = findTime(order,hourIndex,minIndex) # 따로 처리해야하기 때문에 flag를 파라미터로 넘김

    '''
    알람에 대한 명령어는 두가지가 있다.
    1. 알람을 설정
    2. 알람을 취소
    '''
    # 알람을 취소
    if order.find('취소') != -1 or order.find('해제') != -1 or order.find('없') != -1:
        # 알람이 존재하면 지움
        if alarm_remove(time):
            # 알람 취소를 사용자에게 알림
            confirmTimeToSpeech(time,False)
        else:
            tts('설정되지 않은 알람입니다.')
            playAudio('result.wav')
    else:
        # 알람을 추가
        alarm_add(time)

        # 알람 설정을 사용자에게 알림
        confirmTimeToSpeech(time,True)

def confirmTimeToSpeech(time, flag):
    hour = int(time/100)
    minute = int(time%100)

    # 시간을 string으로 바꿈
    hour = str(hour)
    minute = str(minute)

    # 음성으로 변환 후 재생
    if flag == True:
        tts(hour + '시 ' + minute + '분에 알람이 설정되었습니다.')
        print(hour + '시 ' + minute + '분에 알람이 설정되었습니다.')
    else:
        tts(hour + '시 ' + minute + '분 알람이 취소되었습니다.')
        print(hour + '시 ' + minute + '분에 알람이 취소되었습니다.')

    playAudio('result.wav')

#현재 시간을 정해진 형식으로 바꿔주는 함수
def findTime(order, hourIndex, minIndex):

    hour = 0
    minute = 0

    if hourIndex != -1:
        if hourIndex > 1:
            hour = int(order[hourIndex-2:hourIndex]) * 100
        else:
            hour = int(order[hourIndex-1:hourIndex]) * 100
    if minIndex != -1:
        if minIndex > 1:
            minute = int(order[minIndex-2:minIndex])
        else:
            minute = int(order[minIndex-1:minIndex])

    time = hour + minute

    # 시간의 형식을 맞춤
    time = correctTime(time)
    return time

def alarm_run():
    global alarm_list

    while True:
        # 알람이 들어있으면 현재시간과 알람시간을 확인 후 일치한다면 알람을 울린다.
        for alarm in alarm_list:
            if alarm == getTime():
                playAudio("good_morning.mp3")
                tts(find_weather())
                playAudio("output.wav")

def getTime():
    # 시간을 가져옴
    now = time.localtime()
    hour = now.tm_hour
    minute = now.tm_min

    # 현재 시간 계산
    hour = int(hour)
    nowTime = hour * 100 + minute
    nowTime = int(nowTime)
    return nowTime

def ASMR_play():
    playAudio("ASMR.wav")

def order_manage():
    #듣고있어요 파일 만들어서 넣어주기
    playAudio("response.wav")

    # 녹음 시작 녹음파일이 저장될 이름을 파라미터로 전달(3초간 명령을 녹음)
    recordMic("input.raw")
    # 저장된 녹음파일을 텍스트로 전환
    responses = sst("input.raw")
    for response in responses:
        # response.alternatives[0].transcript 에 우리가 원하는 sst의 결과가 들어있다
        print("명령: " + response.alternatives[0].transcript)
        interpretOrder(response.alternatives[0].transcript)

# 명령의 종류를 확인 후 명령을 수행
def interpretOrder(order):
    if order.find("날씨") != -1:
        tts(findWeather(order))
        playAudio("output.wav")
    elif order.find("알람") != -1:
        alarm_manage(order)
        print("알람 리스트")
        print(alarm_list)
    elif order.find("안녕") != -1:
        tts("안녕하세요 다똑시입니다.")
        playAudio("output.wav")
    elif order.find("비트박스") != -1:
        tts("북치기 박치기 북치기 박치기")
        playAudio("output.wav")
    elif order.find("asmr") != -1:
        playAudio("asmr.wav")
    elif order.find("에이에스엠알") != -1:
        playAudio("asmr.wav")
    else:
        # 예외처리
        playAudio("exception.wav") # 이건 만들어야함.
try:
    # 알람을 쓰레드를 이용해 동작
    alarm_thread = threading.Thread(target=alarm_run)
    alarm_thread.start()




except:
    pass
