import random
from kivy.app import App, Widget
from kivy.core.window import Window
from kivy.properties import StringProperty


class Keyboard(Widget):
    """
    メインレイアウト
    キーボードからの入力を受け取る
    """

    input_text = StringProperty("")

    def __init__(self, **kwargs):
        super(Keyboard, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] == 8:
            # バックスペース
            self.input_text = self.input_text[:-1]
        elif len(self.input_text) < 30:
            self.input_text += text + " "

        # print(f"The key {keycode} has been pressed")
        # print(f" - text is {text}")
        # print(' - modifiers are %r' % modifiers)
        # print(self.input_text)


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

    def random_pick_problems(self, required: int):
        """
        問題となる英単語をランダムで複数ピックアップする
        """
        self.random_problems = random.sample(self.problems, required)
        print(self.random_problems)


class TypingApp(App):
    def build(self):
        quiz = Quiz()
        quiz.random_pick_problems(10)
        return Keyboard()


if __name__ == "__main__":
    TypingApp().run()