import MeCab
from edit_mlask import EditMLAsk

mecab = MeCab.Tagger("-Owakati") #品詞分解後の単語のみを取得するモード
emotion_analyzer = EditMLAsk()

# 色の辞書：10色（デフォルトの黒は辞書にない）
emotion_color_map = {
    "takaburi": (233, 113, 50),
    "ikari": (255, 0, 0),
    "iya": (160, 43, 147),
    "aware": (21, 96, 130),
    "odoroki": (15, 158, 213),
    "kowa": (25, 107, 36),
    "yasu": (142, 217, 115),
    "yorokobi": (255, 192, 0),
    "haji": (192, 79, 21),
    "suki": (216, 110, 204)
}

emotion_color_map_hex = {
    "takaburi": "#E97132",
    "ikari": "#FF0000",
    "iya": "#A02B93",
    "aware": "#156082",
    "odoroki": "#0F9ED5",
    "kowa": "#196B24",
    "yasu": "#8ED973",
    "yorokobi": "#FFC000",
    "haji": "#C04F15",
    "suki": "#D86ECC"
}

# フォントの辞書（デフォルトのフォントは辞書にない）
emotion_font_map = {
    "takaburi": "DelaGothicOne-Regular.ttf",
    "ikari": "ReggaeOne-Regular.ttf",
    "iya": "ZenAntiqueSoft-Regular.ttf",
    "aware": "ZenOldMincho-Regular.ttf",
    "odoroki": "KosugiMaru-Regular.ttf",
    "kowa": "PottaOne-Regular.ttf",
    "yasu": "SawarabiGothic-Regular.ttf",
    "yorokobi": "MochiyPopOne-Regular.ttf",
    "haji": "ZenKurenaido-Regular.ttf",
    "suki": "YuseiMagic-Regular.ttf"
}

# Orientation(ネガポジ分類)の辞書（3種, デフォルトはNEUTRAL）
orientation_map = {
    "POSITIVE": "POSITIVE",
    "mostly_POSITIVE":"POSITIVE",
    "mostly_NEGATIVE":"NEGATIVE",
    "NEGATIVE": "NEGATIVE",
    "NEUTRAL": "NEUTRAL"
}

# Activation(活性分類)の辞書（3種, デフォルトはNEUTRAL）
activation_map = {
    "ACTIVE": "ACTIVE",
    "mostly_ACTIVE":"ACTIVE",
    "PASSIVE": "PASSIVE",
    "mostly_PASSIVE":"PASSIVE",
    "NEUTRAL": "NEUTRAL"
}

# 辞書のリストを生成する関数
def create_emotion_text_list(data):
    result = []
    for emotion, texts in data.items():
        for text in texts:
            result.append({"emotion": emotion, "word": text})
    return result

def get_emotion_data(result):
    """ 感情分析の結果から単語、色、フォント、ネガポジ分類、活性分類を抽出する
    Args:
       result(dict): 感情分析の結果
    Returns:
       list: 感情分析の結果に基づく辞書のリスト
    """
    words_emotions = result.get('emotion', None)  # 'emotion'がNoneの場合はデフォルト値を設定
    orientation = result.get('orientation', 'NEUTRAL')  # ネガポジ分類を取得
    activation = result.get('activation', 'NEUTRAL')  # 活性分類を取得

    # 'emotion'がNoneの場合はデフォルトの辞書を返す
    if words_emotions is None:
        return [{'word': result.get('text', ''), 'emotion': 'NEUTRAL', 'color': '#000000', 'font': 'HGRSMP.ttf', 'orientation': orientation_map.get(orientation, 'NEUTRAL'), 'activation': activation_map.get(activation, 'NEUTRAL')}]

    # 各単語に対して、感情、色、フォント、ネガポジ、活性を取得して辞書リストを生成
    emotion_data = []
    hold_add_emo_word = []
    words_with_emo = create_emotion_text_list(words_emotions)
    for orig_word in (mecab.parse(result.get("text", ""))).split():  # 品詞分解
        # if orig_word in hold_add_emo_word:
        #     continue
        emo_dict = {'word': orig_word, 'emotion': 'NEUTRAL', 'color': '#000000', 'font': 'HGRSMP.ttf', 'orientation': orientation_map.get(orientation, 'NEUTRAL'), 'activation': activation_map.get(activation, 'NEUTRAL')}
        for word_with_emo in words_with_emo:
            if orig_word in word_with_emo["word"]:
                color = emotion_color_map_hex.get(word_with_emo["emotion"], "#000000")  # 感情に対応する色を取得
                font = emotion_font_map.get(word_with_emo["emotion"], "HGRSMP.ttf")  # 感情に対応するフォントを取得
                emo_dict = dict(
                    word=orig_word,
                    color=color,
                    font=font,
                    orientation=orientation_map.get(orientation, "NEUTRAL"),  # ネガポジ分類
                    activation=activation_map.get(activation, "NEUTRAL")  # 活性分類
                )
                # emotion_data.append(emo_dict)
                break
        emotion_data.append(emo_dict)
        # hold_add_emo_word.append(orig_word)
        # for emotion, words in words_emotions.items():
        #     for word in words:
        #         if orig_word in word:
        #             color = emotion_color_map_hex.get(emotion, "#000000")  # 感情に対応する色を取得
        #             font = emotion_font_map.get(emotion, "HGRSMP.ttf")  # 感情に対応するフォントを取得
        #             emo_dict = dict(
        #                 word=orig_word,
        #                 color=color,
        #                 font=font,
        #                 orientation=orientation_map.get(orientation, "NEUTRAL"),  # ネガポジ分類
        #                 activation=activation_map.get(activation, "NEUTRAL")  # 活性分類
        #             )
        #             emotion_data.append(emo_dict)
        #             break
        #         else:
        #             emotion_data.append({'word': orig_word, 'emotion': 'NEUTRAL', 'color': '#000000', 'font': 'HGRSMP.ttf', 'orientation': orientation_map.get(orientation, 'NEUTRAL'), 'activation': activation_map.get(activation, 'NEUTRAL')})
                
    # for emotion, words in words_emotions.items():
    #     for word in words:
    #         color = emotion_color_map_hex.get(emotion, "#000000")  # 感情に対応する色を取得
    #         font = emotion_font_map.get(emotion, "HGRSMP.ttf")  # 感情に対応するフォントを取得
    #         emo_dict = dict(
    #             word=word,
    #             color=color,
    #             font=font,
    #             orientation=orientation_map.get(orientation, "NEUTRAL"),  # ネガポジ分類
    #             activation=activation_map.get(activation, "NEUTRAL")  # 活性分類
    #         )
    #         emotion_data.append(emo_dict)
    
    return emotion_data


def get_representative_emotion(result):
    """ 文章全体の代表的な感情を取得する
    Args:
       result(dict): 感情分析の結果
    Returns:
       dict: 代表的な感情に基づく辞書
    """
    representative_emotion = result.get("representative", None) # 代表する感情を取得
    orientation = result.get("orientation", "NEUTRAL")  # ネガポジ分類を取得
    activation = result.get("activation", "NEUTRAL")  # 活性分類を取得
    word = result.get("text","")

    if representative_emotion:
        emotion = representative_emotion[0]  # 代表する感情を取得
        color = emotion_color_map_hex.get(emotion, "#000000")  # 感情に対応する色を取得
        font = emotion_font_map.get(emotion, "HGRSMP.ttf")  # 感情に対応するフォントを取得
        
        return dict(
            word=word,
            emotion=emotion,
            color=color,
            font=font,
            orientation=orientation_map.get(orientation, "NEUTRAL"),  # ネガポジ分類
            activation=activation_map.get(activation, "NEUTRAL")  # 活性分類
        )
    else:
        # 代表する感情がない場合、デフォルト値を返す
        return dict(
            word=word,
            emotion="NEUTRAL",
            color=(0, 0, 0),
            font="HGRSMP.ttf",
            orientation="NEUTRAL",
            activation="NEUTRAL"
        )

def emotion_main_words(text):
    """ 文章全体から感情分析を行い、「単語ごとに」１つの結果を出力する
    Args:
       text(str): 感情分析を行いたい文章
    """
    result = emotion_analyzer.analyze(text)
    emotion_data = get_emotion_data(result)
    
    return emotion_data

def emotion_main_text(text):
    """ 文章全体から代表的な感情を推定し、「入力文字列に対して」１つの結果を出力する
    Args:
       text(str): 感情分析を行いたい文章
    """
    result = emotion_analyzer.analyze(text)
    emotion_data = get_representative_emotion(result)

    return emotion_data

    
#-----------------------------------------------------------------------------------------------------------------------
# テスト用
if __name__ == "__main__":
    # text = "彼女のことが嫌いではない！(;´Д`)"
    text = "嬉しい喜び悲しい嫌いではない"
    with open("C:/Users/rikotaro/OneDrive - Hiroshima City University (1)/new_kamisibai/広島カープ昔話2023.06.18-2.txt",encoding="utf-8") as f:
      for s in f:
        s_result=emotion_main_words(s)[0]
        if "emotion" not in s_result.keys():
            break
        if s_result["emotion"] == "NEUTRAL" and s_result["orientation"] != "NEUTRAL":
          print("O",s_result)
        if s_result["emotion"] == "NEUTRAL" and s_result["activation"] != "NEUTRAL":
          print("A",s_result)
    #print(emotion_main_words(text))
    # print(emotion_main_text(text))

    #出力見本
    """emotion_main_words(text)
    {'word': 'びっくり', 'color': (15, 158, 213), 'font': 'KosugiMaru-Regular.ttf', 'orientation': 'POSITIVE', 'activation': 'ACTIVE'}
    {'word': 'フレンドリー', 'color': (216, 110, 204), 'font': 'YuseiMagic-Regular.ttf', 'orientation': 'POSITIVE', 'activation': 'ACTIVE'}
    {'word': '丁寧', 'color': (255, 192, 0), 'font': 'MochiyPopOne-Regular.ttf', 'orientation': 'POSITIVE', 'activation': 'ACTIVE'}
    {'word': '満足', 'color': (255, 192, 0), 'font': 'MochiyPopOne-Regular.ttf', 'orientation': 'POSITIVE', 'activation': 'ACTIVE'}
    """
    """emotion_main_text(text)

    {'word': '夕食がとても美味しく友達も喜んでいました。ありがとうございます！客室担当方はフレンドリーで丁寧に接客してくれました。朝ご飯もちょうどいいくらいの量で満足でした。部屋も予想よりも広くびっくりしました。', 
    'emotion': 'suki', 'color': (216, 110, 204), 'font': 'YuseiMagic-Regular.ttf', 'orientation': 'POSITIVE', 'activation': 'ACTIVE'}
    """