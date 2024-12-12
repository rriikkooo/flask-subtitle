# flask-subtitle
1. Pythonをインストール(devも必要)

1. ソースコードをダウンロード
```https://github.com/F-Naru/flask-subtitle```

1. 仮想環境を作成
```python -m venv venv```

1. 仮想環境を有効化
```source venv/bin/activate```

1. パッケージをインストール
```pip install -r requirements.txt```

1. アプリケーションを起動
```python app.py```

# 注意点
1. mlaskの__init__.pyを修正
```/home/uni7ru/Desktop/subtitle/venv/lib/python3.12/site-packages/mlask/__init__.py```
2. unidicをダウンロード
```python -m unidic download```
3. modelをダウンロード
```https://drive.google.com/drive/folders/1m6GMidvSFkqOmZ35PmFaVR7bIBE15j3M?usp=drive_link```

# メモ
- main.py
    - speech_recognition.py (音声認識)
        - emorecognition.py (？)
            - judge_text_emo_new.py (感情分析 単語ごとver)
        - speaker_recognition.py (話者分析)
    - app.py (Flask GUI Webサーバー)

# 修正箇所
1. jsonファイルを単語ごとに色を管理できるように修正
2. jsonファイルを読み込んでGUIが単語ごとに色を付けられるように修正
3. speech_recognition.pyが単語ごとのjsonファイルに対応できるように修正
