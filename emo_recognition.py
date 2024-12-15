import judge_text_emo_new_v2 as judge_text_emo

class Emotion:
    def __init__(self):
        pass

    def get_text_emo_style(self, text):
        return judge_text_emo.emotion_main_words(text)
