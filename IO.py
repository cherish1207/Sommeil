# 녹음을 위한 library
import pyaudio
import wave

# 오디오파일 재생을 위한 library
import sys
import pygame as pg



# 저장할 파일의 이름을 받고 그 이름으로 저장(raw 형식)
#  ex)recordMic("jooyong.raw")
def recordMic(text):
    FORMAT = pyaudio.paInt16

    CHANNELS = 1
    RATE = 16000
    CHUNK = int(RATE / 10)
    RECORD_SECONDS = 3

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
    print ("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print ("finished recording")


    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()


    wf = wave.open( text, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# 오디오 파일 이름을 받고 그 파일을 재생시켜 줌 (mp3, wav, raw 형식)
# ex) playAudio("jooyoung.mp3")
def playAudio(audioFile):
    volume=1    # optional volume 0 to 1.0
    
    pg.mixer.init()

    # volume value 0.0 to 1.0
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()

    try:
        pg.mixer.music.load(audioFile)
        print("Music file {} loaded!".format(audioFile))
    except pg.error:
        print("File {} not found! ({})".format(audioFile, pg.get_error()))
        return

    pg.mixer.music.play()
    while pg.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(10)
    pg.quit()

if __name__ == "__main__":
    recordMic("input.raw")
    playAudio("input.raw")
    #playAudio("timeException.wav")
