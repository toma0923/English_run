import random

class Quiz:

    def __init__(self):
        # 英単語をファイルから読み込む
        with open("db/words.txt", "r") as f:
            self.raw_problems = f.readlines()
            self.raw_problems = [x.strip() for x in self.raw_problems]

        # ハイスコア用ファイルがなければ新規作成する
        try:
            with open("db/high_score.txt", "x+") as f:
                f.write("0\n")
        except FileExistsError:
            pass

        self.problems = []
        N = 30  # 一章ごとの単語数
        for p in self.raw_problems:
            x = p.split(",")
            self.problems.append(x)
        # 問題をそれぞれの章ごとに分割する
        self.problems = [self.problems[i: i+N] for i in range(0, len(self.problems), N)]
        self.len_stage = len(self.problems)


    def random_pick_problems(self, stage: int):
        """
        問題となる英単語をランダムで複数ピックアップする
        """
        self.raw_random_problems = self.problems[stage][:]
        self.random_problems = self.raw_random_problems[:]
        random.shuffle(self.random_problems)
        print(self.random_problems)
        return self.problems[stage][:]

    def next_problem(self):
        """
        問題を切り替える
        """
        self.current = self.random_problems.pop(0)
        # 問題が最後までいったとき
        if len(self.random_problems) == 0:
            self.random_problems = self.raw_random_problems[:]

    def show_correct(self):
        """
        不正解時に正しい問題を表示する
        """

    def check_input(self, input):
        """
        入力が正解かどうか判定する
        """
        # print(input, self.current[0])
        if input == self.current[0]:
            return True
        else:
            return False
        
    def save_high_score(self, score):
        """
        ハイスコアかどうかを判断して保存する
        """
        with open("db/high_score.txt", "r") as f:
            self.high_score = f.read()
            self.high_score = int(self.high_score) if self.high_score.isdecimal() else 0

        if score > self.high_score:
            with open("db/high_score.txt", "w") as f:
                f.write(str(int(score)))
