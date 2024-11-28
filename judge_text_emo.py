import MeCab
from edit_mlask import EditMLAsk
# from mlask import MLAsk
t = MeCab.Tagger()
emotion_analyzer = EditMLAsk()

###########テスト#######################################################
# sentence = "太郎はこの本を女性に渡した。"
# print(t.parse(sentence))
# analyze_result1 = emotion_analyzer.analyze('彼のことは嫌いではない！(;´Д`)')
# text = "夕食がとても美味しく友達も喜んでいました。ありがとうございます！" \
#        "客室担当方はフレンドリーで丁寧に接客してくれました。" \
#        "朝ご飯もちょうどいいくらいの量で満足でした。" \
#        "部屋も予想よりも広くびっくりしました。"
# analyze_result2 = emotion_analyzer.analyze(text)
# print(analyze_result1)
# print(analyze_result2)
########################################################################

#色の辞書
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

#フォントの辞書
emotion_font_map = {
    "takaburi": "DelaGothicOne-Regular",
    "ikari": "ReggaeOne-Regular",
    "iya": "ZenAntiqueSoft-Regular",
    "aware": "ZenOldMincho-Regular",
    "odoroki": "KosugiMaru-Regular",
    "kowa": "PottaOne-Regular",
    "yasu": "SawarabiGothic-Regular",
    "yorokobi": "MochiyPopOne-Regular",
    "haji": "ZenKurenaido-Regular",
    "suki": "YuseiMagic-Regular"
}

def get_text_emo_style(text):
    result = emotion_analyzer.analyze(text)
    color = get_emotion_color(result)
    font = get_emotion_font(result)
    return {"color": color, "font": font}

def get_emotion_color(result):
    """
    textのRGB値を返す

    Args:
       text(str):RGB値を知りたい文字列
    
    Returns:
       int:右の形で出力されます (0,0,0)

    """
    # result = emotion_analyzer.analyze(text)
    try:
        emotion = result["representative"][0]  # 'representative'を使って感情を取得
        # print(emotion)

        return emotion_color_map.get(emotion, (0, 0, 0))  # デフォルトの色
    except:
        return (0, 0, 0) # デフォルトの色

def get_emotion_font(result):
    """
    textのフォント(ファイル)を返す
    
    Args:
       text(str):RGB値を知りたい文字列
    
    Returns:
       str:右の形で出力されます HGRME
    
    """
    # result = emotion_analyzer.analyze(text)
    try:
        emotion = result["representative"][0]
        # print(emotion)

        return emotion_font_map.get(emotion, "HGRSMP")  
    except:
        return "HGRSMP"  # デフォルトのフォント