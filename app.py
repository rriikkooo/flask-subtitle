from flask import Flask, render_template, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import json
import os
from multiprocessing import Queue
import threading

class SubtitleApp:
    def __init__(self, queue):
        self.queue = queue
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.subtitle_data = []
        self.socketio = SocketIO(self.app)

        # ルートの設定
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/ttf/<path:filename>', 'serve_ttf', self.serve_ttf)

        # ソケットイベントの設定
        self.socketio.on_event('get_subtitles', self.send_latest_subtitle)

    def index(self):
        return render_template('index.html')

    def serve_ttf(self, filename):
        return send_from_directory(os.path.join(self.app.root_path, 'ttf'), filename)

    def send_latest_subtitle(self):
        """
        クライアントからget_subtitlesを受信したら最新の字幕を送信
        """
        if self.subtitle_data:
            emit('update_subtitles', self.subtitle_data[-1])  # 最新の字幕を送信

    def watch_queue(self):
        """
        キューを監視して新しいデータはすぐに送信
        """
        while True:
            try:
                # キューからデータを取得（非ブロッキング）
                json_data = self.queue.get(timeout=1)  # タイムアウト付きで取得
                self.subtitle_data.append(json_data)  # データを保存
                # Flask-SocketIO の emit を使用して非同期でクライアントに送信
                self.socketio.emit('update_subtitles', json_data)
            except Exception as e:
                self.socketio.sleep(0.1)  # 非ブロッキングで少し待機

    def run(self, host="0.0.0.0", port=5000):
        # watch_queueをバックグラウンドタスクとして起動
        self.socketio.start_background_task(target=self.watch_queue)
        # Flask-SocketIOサーバーを起動
        self.socketio.run(self.app, host=host, port=port)

# アプリの実行
if __name__ == "__main__":
    queue = Queue()
    app = SubtitleApp(queue)
    # subtitle.jsonを読み込んでqueueに入れる
    with open("subtitles.json") as f:
        json_data = json.load(f)
    for subtitle in json_data["subtitles"]:
        queue.put(subtitle)
    # Flask起動        
    app.run()
