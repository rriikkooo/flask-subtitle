import ndjson
import sys
import os
import json
from vosk import Model, KaldiRecognizer, SpkModel, SetLogLevel
import numpy as np

# ログの非表示
SetLogLevel(-1)

class SpeakerRecognition:

    def __init__(self):
        # Voskモデルのロード
        self.model_path = "model/vosk-model-ja-0.22"
        self.model_spk = "model/vosk-model-spk-0.4"
        self.model = Model(self.model_path)

        self.all_data = self.read_all_data()

    def cosine_dist(self, x, y):
        nx = np.array(x)
        ny = np.array(y)
        return np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)

    def read_all_data(self):
        all_data = {}
        for filename in os.listdir("data"):
            with open("data/" + filename) as f:
                datasets = ndjson.load(f)
                data_list = []
                for data in datasets:
                    data_list.append(data["data"])
            
            name = filename.split(".")[0]
            all_data[name] = data_list

        return all_data

    def recognition(self, speaker_data, text):
        compare_result = {}
        for name, data_list in self.all_data.items():
            dis_list = []
            for data in data_list:
                dis_list.append(self.cosine_dist(data, speaker_data))
            compare_result[name] = np.mean(dis_list)
        
        result_speaker = max(compare_result, key=compare_result.get)
        result = compare_result[result_speaker]
        # print(f"{result_speaker}:{result}")
        border = 0.05 * min(len(text), 8)
        if result >= border:
            return result_speaker
        else:
            return "話者を特定できませんでした"

if __name__ == "__main__":
    spk_sig = [-1.110417,0.09703002,1.35658,0.7798632,-0.305457,-0.339204,0.6186931,
        -0.4521213,0.3982236,-0.004530723,0.7651616,0.6500852,-0.6664245,0.1361499,
        0.1358056,-0.2887807,-0.1280468,-0.8208137,-1.620276,-0.4628615,0.7870904,
        -0.105754,0.9739769,-0.3258137,-0.7322628,-0.6212429,-0.5531687,-0.7796484,
        0.7035915,1.056094,-0.4941756,-0.6521456,-0.2238328,-0.003737517,0.2165709,
        1.200186,-0.7737719,0.492015,1.16058,0.6135428,-0.7183084,0.3153541,0.3458071,
        -1.418189,-0.9624157,0.4168292,-1.627305,0.2742135,-0.6166027,0.1962581,
        -0.6406527,0.4372789,-0.4296024,0.4898657,-0.9531326,-0.2945702,0.7879696,
        -1.517101,-0.9344181,-0.5049928,-0.005040941,-0.4637912,0.8223695,-1.079849,
        0.8871287,-0.9732434,-0.5548235,1.879138,-1.452064,-0.1975368,1.55047,
        0.5941782,-0.52897,1.368219,0.6782904,1.202505,-0.9256122,-0.9718158,
        -0.9570228,-0.5563112,-1.19049,-1.167985,2.606804,-2.261825,0.01340385,
        0.2526799,-1.125458,-1.575991,-0.363153,0.3270262,1.485984,-1.769565,
        1.541829,0.7293826,0.1743717,-0.4759418,1.523451,-2.487134,-1.824067,
        -0.626367,0.7448186,-1.425648,0.3524166,-0.9903384,3.339342,0.4563958,
        -0.2876643,1.521635,0.9508078,-0.1398541,0.3867955,-0.7550205,0.6568405,
        0.09419366,-1.583935,1.306094,-0.3501927,0.1794427,-0.3768163,0.9683866,
        -0.2442541,-1.696921,-1.8056,-0.6803037,-1.842043,0.3069353,0.9070363,-0.486526]
    filename = "fujitou_normal/fujitou_normal_099.wav"
    speaker_recognition = SpeakerRecognition()
    print(speaker_recognition.recognition(spk_sig))