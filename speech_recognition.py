import argparse
import queue
import sys
import json
import sounddevice as sd
import speaker_recognition
import record
import datetime
from googletrans import Translator
import numpy as np
from vosk import Model, KaldiRecognizer, SpkModel
from emo_recognition import Emotion
from predict_text import CERTextMatcher

class SpeechRecognition:
    def __init__(self, queue_=None):
        self._queue_input_json = queue_
        self._queue_input_json_index = 1
        self._queue_input_audio = queue.Queue()
        self._speaker_recognition = speaker_recognition.SpeakerRecognition()
        self._translator = Translator()
        self._recorder = record.Recorder(filename="record.wav")
        self.emotion = Emotion()
        self.textmacher = CERTextMatcher("output.txt", cer_threshold=0.4)
        self.previous_text = ""

        # コマンドライン引数の設定
        parser = argparse.ArgumentParser(add_help=False)
        self._parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[parser])
        self._parser.add_argument(
            "-f", "--filename", type=str, metavar="FILENAME",
            help="audio file to store recording to")
        self._parser.add_argument(
            "-d", "--device", type=self._int_or_str,
            help="input device (numeric ID or substring)")
        self._parser.add_argument(
            "-r", "--samplerate", type=int, help="sampling rate")
        self._parser.add_argument(
            "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
        self._args = self._parser.parse_args()

    def _is_silent(self, data, threshold=100):
        audio_data = np.frombuffer(data, dtype=np.int16)
        # return np.all(np.abs(audio_data) <= threshold)
        # print(audio_data.max())
        return audio_data.max() <= threshold

    def _int_or_str(self, text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    def _callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self._queue_input_audio.put(bytes(indata))

    def _str_to_json(self, result):
        return json.loads(result)
    
    def _result_input_queue(self, result):
        text = result["text"] if "text" in result else result["partial"]
        # speaker = result["spk"] if "spk" in result else ""
        speaker = ""

        MIN_TEXT_LEN = 1
        if len(text) > MIN_TEXT_LEN or len(set(text)) > 1:
            text = self.textmacher.find_best_match(text)
            if "text" in result:
                try:
                    # translate_text = self._translator.translate(text, src='ja', dest='en').text
                    # print(translate_text)
                    translate_text = ""
                except:
                    translate_text = ""
            else:
                translate_text = ""

            if self.previous_text != text or "text" in result:
                emo_dicts = self.emotion.get_text_emo_style(text)
                words = []
                for idx, emo_dict in enumerate(emo_dicts):
                    word = {
                        "no": idx + 1,
                        "text": emo_dict["word"],
                        "color": emo_dict["color"],
                        "font": emo_dict["font"].split('.')[0],
                        "size": 60,
                    }
                    words.append(word)
                emo_style = {
                    "index": self._queue_input_json_index,
                    "datetime": datetime.datetime.now().isoformat(),
                    "words": words,
                    "eng": translate_text,
                    "speaker": speaker,
                    "color": "#000000",
                    "font": "Arial",
                    "size": 30
                }
                emo_dict = dict(emo_style)
                self._queue_input_json.put(emo_dict)
                self._queue_input_json_index += 1          
            else:
                emo_style = {"color": (0, 0, 0), "font": "Arial"}

            # テキスト情報を保持
            self.previous_text = text

    def run(self):
        try:
            if self._args.samplerate is None:
                device_info = sd.query_devices(self._args.device, "input")
                # soundfile expects an int, sounddevice provides a float:
                self._args.samplerate = int(device_info["default_samplerate"])
                
            if self._args.model is None:
                model = Model("model/vosk-model-ja-0.22")
            else:
                model = Model(lang=self._args.model)

            with sd.RawInputStream(samplerate=self._args.samplerate, blocksize = 8000, device=self._args.device,
                    dtype="int16", channels=1, callback=self._callback):
                print("#" * 80)
                print("Press Ctrl+C to stop the recording")
                print("#" * 80)

                rec = KaldiRecognizer(model, self._args.samplerate)
                spk_model = SpkModel("model/vosk-model-spk-0.4")
                rec.SetSpkModel(spk_model)
                while True:
                    data = self._queue_input_audio.get()
                    if not self._is_silent(data):
                        pass
                        # self._recorder.start()
                    if rec.AcceptWaveform(data) or len(self.previous_text) > 40:
                        # self._recorder.stop()
                        result = self._str_to_json(rec.Result())
                        result["text"] = result["text"].replace(" ", "")
                        print(f"text:{result['text']}")
                        # if "spk" in result:
                        #     print(self._speaker_recognition.recognition(result["spk"], result["text"]))
                    else:
                        result = self._str_to_json(rec.PartialResult())
                        result["partial"] = result["partial"].replace(" ", "")
                        print(f"partial:{result['partial']}")
                    
                    self._result_input_queue(result)

        except KeyboardInterrupt:
            # self._recorder.stop()
            print("\nDone")
            self._parser.exit(0)
        except Exception as e:
            self._parser.exit(type(e).__name__ + ": " + str(e))

if __name__ == "__main__":
    speech_recognition = SpeechRecognition()
    speech_recognition.run()