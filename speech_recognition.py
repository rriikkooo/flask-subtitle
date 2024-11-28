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

class SpeechRecognition:
    def __init__(self, queue_=None):
        self._queue_input_json = queue_
        self._queue_input_json_index = 1
        self._queue_input_audio = queue.Queue()
        self._speaker_recognition = speaker_recognition.SpeakerRecognition()
        self._translator = Translator()
        self._recorder = record.Recorder(filename="record.wav")
        self.emotion = Emotion()
        self.text_log = ["", "", ""]

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
        if "text" in result:
            text = result["text"]
        else:
            text = result["partial"]

        if text != "":
            self.text_log.append(text)
            self.text_log.pop(0)
        
        if "spk" in result:
            speaker = result["spk"]
        else:
            speaker = ""
        
        if "text" in result and text != "":
            try:
                translate_text = self._translator.translate(text, src='ja', dest='en').text
            except:
                translate_text = ""
        else:
            translate_text = ""

        if len(set(self.text_log)) == 1 or "text" in result:
            emo_style = self.emotion.get_text_emo_style(text)
        else:
            emo_style = {"color": (0, 0, 0), "font": "Arial"}
        
        template = {
            "index": self._queue_input_json_index,
            "datetime": datetime.datetime.now().isoformat(),
            "text": text,
            "eng": translate_text,
            "speaker": speaker,
            "color": emo_style["color"],
            "font": emo_style["font"]
        }
        
        if template["text"] != "":
            self._queue_input_json.put(template)
        self._queue_input_json_index += 1

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
                    if rec.AcceptWaveform(data) or len(self.text_log[-1]) > 80:
                        # self._recorder.stop()
                        result = self._str_to_json(rec.Result())
                        result["text"] = result["text"].replace(" ", "")
                        print(f"text:{result['text']}")
                        if "spk" in result:
                            print(self._speaker_recognition.recognition(result["spk"], result["text"]))
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