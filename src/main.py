import random
import japanize_kivy
from kivy.app import App, Widget
from kivy.core.window import Window
from kivy.properties import StringProperty


class MainLayout(Widget):
    """
    メインレイアウト
    キーボードからの入力を受け取る
    """

    input_text = StringProperty("")

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.quiz = Quiz()
        self.switch_shown_text()

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] == 8:
            # バックスペース
            self.input_text = self.input_text[:-2]

        elif keycode[0] == 13:
            truly_input_text = self.input_text.replace(" ", "")
            # Enterが押されたとき、入力が正しければ正解処理に進む
            if self.quiz.check_input(truly_input_text):
                self.switch_shown_text()
            self.input_text = ""

        elif text != None:
            # 文字数制限以下なら文字を追加
            if len(self.input_text) < self.len_current_problem * 2:
                self.input_text += text + " "

        print(f"The key {keycode} has been pressed")
        print(f" - text is {text}")
        print(' - modifiers are %r' % modifiers)

    def switch_shown_text(self):
        """
        表示されている問題文を次に切り替える
        """
        self.quiz.next_problem()
        self.len_current_problem = len(self.quiz.current[0])  # 問題の英単語の文字数
        self.ids.question.text = self.quiz.current[1]  # 問題文(日本語)
        self.ids.under_line.text = "_ " * self.len_current_problem  # アンダーバー


class Quiz:
    def __init__(self):
        """
        英単語をファイルから読み込む
        """
        with open("words.txt", "r") as f:
            self.raw_problems = f.readlines()
            self.raw_problems = [x.strip() for x in self.raw_problems]

        self.problems = []
        for p in self.raw_problems:
            x = p.split(",")
            self.problems.append(x)
        
        self.random_pick_problems(10)

    def random_pick_problems(self, required: int):
        """
        問題となる英単語をランダムで複数ピックアップする
        """
        self.random_problems = random.sample(self.problems, required)
        print(self.random_problems)

    def next_problem(self):
        """
        問題を切り替える
        """
        self.current = self.random_problems.pop(0)

    def check_input(self, input):
        """
        入力が正解かどうか判定する
        """
        if input == self.current[0]:
            return True
        else:
            return False


class TypingApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    TypingApp().run()