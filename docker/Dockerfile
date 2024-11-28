# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係のコピー
COPY requirements.txt .

# 依存関係のインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコピー
COPY . .

# アプリケーションの起動コマンド
CMD ["python", "app.py"]
