import pyaudio
import wave
import threading

class Recorder:
    def __init__(self, filename="output.wav", channels=1, rate=44100, frames_per_buffer=1024):
        self.filename = filename
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False

    def start(self):
        if self.is_recording:
            # print("Recording is already in progress")
            return

        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.is_recording = True
        self.frames = []

        print("Recording started")
        self._record()

    def _record(self):
        def callback():
            while self.is_recording:
                data = self.stream.read(self.frames_per_buffer)
                self.frames.append(data)

        self.recording_thread = threading.Thread(target=callback)
        self.recording_thread.start()

    def stop(self):
        if not self.is_recording:
            # print("Recording is not in progress")
            return

        self.is_recording = False
        self.recording_thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self._save()

        print("Recording stopped and saved")

    def _save(self):
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

    def __del__(self):
        self.audio.terminate()

if __name__ == "__main__":
    # 使用例
    recorder = Recorder(filename="output.wav")

    # 録音を開始
    recorder.start()

    import time
    time.sleep(4)
    
    recorder.stop()