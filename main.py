from multiprocessing import Process, Queue
import speech_recognition
import app

def start_speech_recognition(queue):
    speech_recognition_ = speech_recognition.SpeechRecognition(queue)
    speech_recognition_.run()

def start_gui(queue):
    gui = app.SubtitleApp(queue)
    gui.run()

if __name__ == "__main__":
    queue = Queue()
    recognition_process = Process(target=start_speech_recognition, args=(queue,))
    gui_process = Process(target=start_gui, args=(queue,))

    recognition_process.start()
    gui_process.start()

    recognition_process.join()
    gui_process.join()