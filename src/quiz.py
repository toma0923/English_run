import random

class Quiz:

    def __init__(self):
        # 英単語をファイルから読み込む
        with open("db/words.txt", "r") as f:
            self.raw_problems = f.readlines()
            self.raw_problems = [x.strip() for x in self.raw_problems]


        self.problems = []
        N = 30  # 一章ごとの単語数
        for p in self.raw_problems:
            x = p.split(",")
            self.problems.append(x)
        # 問題をそれぞれの章ごとに分割する
        self.problems = [self.problems[i: i+N] for i in range(0, len(self.problems), N)]
        self.len_stage = len(self.problems)

        # ハイスコア用ファイルがなければ新規作成する
        try:
            with open("db/high_score.txt", "x+") as f:
                t = ("0," * self.len_stage)[:-1]
                f.write(f"{t}\n")
        except FileExistsError:
            pass


    def random_pick_problems(self, stage: int):
        """
        問題となる英単語をランダムで複数ピックアップする
        """
        self.stage = stage
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
        self.correct_answer = self.current[0]
        # 問題が最後までいったとき
        if len(self.random_problems) == 0:
            self.random_problems = self.raw_random_problems[:]

    def check_input(self, input):
        """
        入力が正解かどうか判定する
        """
        # print(input, self.current[0])
        if input == self.correct_answer:
            return True
        else:
            return False
        
    def read_high_score(self):
        with open("db/high_score.txt", "r") as f:
            high_score_list = f.read().split(",")
        return high_score_list

    def save_high_score(self, score):
        """
        ハイスコアかどうかを判断して保存する
        """
        self.high_score_list = self.read_high_score()
        self.high_score = self.high_score_list[self.stage]
        self.high_score = int(self.high_score) if self.high_score.isdecimal() else 0

        if score > self.high_score:
            self.high_score_list[self.stage] = str(int(score))
            with open("db/high_score.txt", "w") as f:
                f.write(",".join(self.high_score_list))
