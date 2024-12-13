




class Score:
    def __init__(self):
        self.score = 0
        self.highscores = self.load_highscores()
        
    def load_highscores(self):
        try:
            with open("highscores.bin", "rb") as file:
                return [int.from_bytes(file.read(4), 'big') for _ in range(10)]
        except FileNotFoundError:
            return [0] * 10

    def save_highscores(self):
        with open("highscores.bin", "wb") as file:
            for score in self.highscores:
                file.write(score.to_bytes(4, 'big'))

    def set_score(self, new_score):
        print(f"New score: {new_score}") # デバッグ用プリント文
        if new_score > min(self.highscores):
            self.highscores.append(new_score)
            self.highscores = sorted(self.highscores, reverse=True)[:10]
            self.save_highscores()  # ハイスコアが更新された場合にファイルに書き出す
            print(f"Updated highscores: {self.highscores}") # デバッグ用プリント文

    def clear_highscores(self):
        self.highscores = [0] * 10
        self.save_highscores()

