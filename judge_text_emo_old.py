import MeCab
from edit_mlask import EditMLAsk

mecab = MeCab.Tagger("-Owakati") #品詞分解後の単語のみを取得するモード
emotion_analyzer = EditMLAsk()

#================以下から各辞書の定義===============================

#色の辞書：10色（デフォルトの黒は辞書にない）
'''
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
'''
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

#フォントの辞書（デフォルトのフォントは辞書にない）
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

# Orientation(ネガポジ分類)の辞書（3種,デフォルトはNEUTRAL）
orientation_map = {
    "POSITIVE": "POSITIVE",
    "NEGATIVE": "NEGATIVE",
    "NEUTRAL": "NEUTRAL"
}

# Activation(活性分類)の辞書（3種,デフォルトはNEUTRAL）
activation_map = {
    "ACTIVE": "ACTIVE",
    "PASSIVE": "PASSIVE",
    "NEUTRAL": "NEUTRAL"
}

#=============以下から各関数の定義==========================================================
def get_emotion_color(text):
    """textのRGB値を返す
    Args:
       text(str):RGB値を知りたい文字列
    Returns:
       int:右の形で出力されます-> (0,0,0)
    """
    result = emotion_analyzer.analyze(text)
    try:
        emotion = result["representative"][0]  # 'representative'を使って感情を取得
        return emotion_color_map_hex.get(emotion, "#000000")  # デフォルトの色
    except:
        return "#000000" # デフォルトの色


def get_emotion_font(text):
    """ textのフォント(.ttfファイル)を返す
    Args:
       text(str):RGB値を知りたい文字列
    Returns:
       str:右の形で出力されます-> HGRME.ttf
    """
    result = emotion_analyzer.analyze(text)
    try:
        emotion = result["representative"][0]
        return emotion_font_map.get(emotion, "HGRSMP.ttf")  
    except:
        return "HGRSMP.ttf"  # デフォルトのフォント


def get_emotion_orientation(text):
    """ ネガポジ分類を取得
    Args:
       text(str):ネガポジ分類を知りたい文字列
    Returns:
       str:右の形で出力されます-> NEUTRAL
    """
    result = emotion_analyzer.analyze(text)
    try:
        orientation = result.get("orientation", "NEUTRAL")
        return orientation_map.get(orientation, "NEUTRAL")  # ネガポジを分類
    except:
        return "NEUTRAL"


def get_emotion_activation(text):
    """ 活性分類を取得
    Args:
       text(str):活性分類を知りたい文字列
    Returns:
       str:右の形で出力されます-> NEUTRAL
    """
    result = emotion_analyzer.analyze(text)
    try:
        activation = result.get("activation", "NEUTRAL")
        return activation_map.get(activation, "PASSIVE")  # 活性度を分類
    except:
        return "NEUTRAL"

def emotion_main(text):
    """ テキストを単語に分解して分析結果を取得
    Args:
       text(str):分析したい文字列
    Returns:
       dict:以下の様に出力
            {'word': '単語', 'color': (0, 0, 0), 'font': 'HGRSMP.ttf', 'orientation': 'NEUTRAL', 'activation': 'NEUTRAL'}
    """
    emo_dicts = []
    for word in (mecab.parse(text)).split():  # 品詞分解
        color = get_emotion_color(word)
        font = get_emotion_font(word)
        orientation = get_emotion_orientation(word)
        activation = get_emotion_activation(word)
        #print(color,font,orientation,activation)
        emo_dict = dict(word=word,color=color, font=font,orientation=orientation,activation=activation)
        emo_dicts.append(emo_dict)
    return emo_dicts


if __name__ == "__main__":
    #===================以下テスト用===================================
    text1 = "そういやあ～広島のチームの名前はきまったんか"
    text2 = "夕食がとても美味しく友達も喜んでいました。ありがとうございます！客室担当方はフレンドリーで丁寧に接客してくれました。朝ご飯もちょうどいいくらいの量で満足でした。部屋も予想よりも広くびっくりしました。"
    print(emotion_main(text1))
