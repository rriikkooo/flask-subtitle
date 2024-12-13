from flask import Flask, render_template, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import json
import os
from multiprocessing import Queue
import json
import datetime

class SubtitleApp:
    def __init__(self, queue):
        self.queue = queue
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.subtitle_data = []
        # self.app.config['DEBUG'] = False
        self.socketio = SocketIO(self.app)

        # ルートの設定
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/ttf/<path:filename>', 'serve_ttf', self.serve_ttf)

        # ソケットイベントの設定
        self.socketio.on_event('get_subtitles', self.handle_get_subtitles)

    def index(self):
        return render_template('index.html')

    def serve_ttf(self, filename):
        return send_from_directory(os.path.join(self.app.root_path, 'ttf'), filename)

    def handle_get_subtitles(self):
        if not self.queue.empty():
            json_data = self.queue.get()
            self.subtitle_data.append(json_data)
            self.socketio.sleep(0.05)
        emit('subtitle', self.subtitle_data[-1])

    def run(self, host="0.0.0.0", port=5000):
        self.socketio.run(self.app, host=host, port=port)

# アプリの実行
if __name__ == "__main__":
    queue = Queue()
    app = SubtitleApp(queue)
    # subtitle.jsonを読み込んでqueueに入れる
    json_data = {}
    with open("subtitles.json") as f:
        json_data = json.load(f)
    print("subtitles", json_data["subtitles"][0])
    queue.put(json_data["subtitles"][0])
    app.run()

