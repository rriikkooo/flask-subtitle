import pyopenjtalk
from jiwer import cer

class CERTextMatcher:
    def __init__(self, filepath, cer_threshold):
        """
        初期化時にファイルを読み込み、各行をアルファベット化して保存。
        filepath: テキストファイルのパス。
        """
        self.cer_threshold = cer_threshold
        self.data = []
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                original_text = line.strip()
                if original_text:  # 空行は無視
                    alphabet_text = pyopenjtalk.g2p(original_text).replace(" ", "")
                    self.data.append((original_text, alphabet_text))

    def find_best_match(self, input_text):
        """
        入力テキストに最も近いテキストを探索し、閾値以下ならそのテキストを返す。
        閾値以下のマッチがなければ入力テキストを返す。
        input_text: 入力されたテキスト。
        cer_threshold: CERスコアの閾値。
        """
        try:
            input_alphabet = pyopenjtalk.g2p(input_text).replace(" ", "")
            best_match = None
            best_score = float("inf")

            for original_text, alphabet_text in self.data:
                score = cer(input_alphabet, alphabet_text)
                if score < best_score:
                    best_score = score
                    best_match = original_text

            if best_score <= self.cer_threshold:
                return best_match
            else:
                return input_text  # マッチが見つからなければ入力テキストをそのまま返す
        except:
            return input_text

# 使用例
if __name__ == "__main__":
    # テキストファイルを準備（各行にテキストを記載）
    filepath = "output.txt"
    cer_threshold = 0.2
    matcher = CERTextMatcher(filepath, cer_threshold)

    input_text = "後者の広島は選手がえっとーオールケーキと強うなるで"

    result = matcher.find_best_match(input_text)
    print("結果:", result)
