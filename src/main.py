import random
import japanize_kivy
from kivy.app import App, Widget
from kivy.lang import Builder
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ObjectProperty, NumericProperty


class ScreenManagement(ScreenManager):
    pass


class MenuScreen(Screen):
    """
    メニュー画面
    """
    # 入力された出題単語数を受け取る変数
    question_nums = 30

    def on_press_start(self):
        # 指定された出題単語数に応じて問題をピックアップする
        if self.input.text != "":
            self.question_nums = int(self.input.text)
        main_screen = self.manager.get_screen("main")
        problems = main_screen.quiz.random_pick_problems(self.question_nums)
        
        check_screen = self.manager.get_screen("check")
        check_screen.show_all_problems(problems)

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "check"


class ForCheckScreen(Screen):
    """
    出題英単語を確認するための画面
    """
    def show_all_problems(self, problems):
        for p in problems:
            english_label = ScrollLabel(text=p[0])
            japanese_label = ScrollLabel(text=p[1])

            self.scroll.add_widget(english_label)
            self.scroll.add_widget(japanese_label)

    def on_press_start(self):
        self.manager.get_screen("main").switch_shown_problem()

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "main"   


class ScrollLabel(Label):
    bg_color = (245/255, 239/255, 61/255, 1)
    color = (0, 0, 0, 1)
    font_size = 30
    def __init__(self, **kwargs):
        super(ScrollLabel, self).__init__(**kwargs)


class MainLayout(Screen):
    """
    メインレイアウト
    キーボードからの入力を受け取る
    """

    shown_text = StringProperty("")
    limit_timer = NumericProperty(60)

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

        self.quiz = Quiz()
        self.input_text = ""

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.manager.current != "main":
            return

        if keycode[0] == 8:
            # バックスペース
            self.input_text = self.input_text[:-1]
            self.change_shown_text()

        elif keycode[0] == 13:
            # Enterが押されたとき、入力が正しければスピードを上げ正解処理に進む
            if self.quiz.check_input(self.input_text):
                self.quiz.speed *= 1.2
                self.switch_shown_problem()
            # 不正解ならスピードダウン
            else:
                self.quiz.speed *= 0.6

        elif text != None:
            # 文字数制限以下なら文字を追加
            if len(self.input_text) < self.len_current_problem:
                self.change_shown_text(add_text=text)

        # print(f"The key {keycode} has been pressed")
        # print(f" - text is {text}")
        # print(' - modifiers are %r' % modifiers)

    def switch_shown_problem(self):
        """
        表示されている問題文を次に切り替える
        """
        self.quiz.next_problem()
        # 問題の英単語の文字数
        self.len_current_problem = len(self.quiz.current[0]) 
        # 問題文(日本語)
        self.ids.question.text = self.quiz.current[1]
        # アンダーバーと入力された文字を初期化
        self.underline = "_" * self.len_current_problem
        self.input_text = ""

        self.change_shown_text()

    def change_shown_text(self, add_text=""):
        self.input_text += add_text
        self.shown_text = " ".join(self.input_text + self.underline[len(self.input_text):])

    def update(self, dt):
        self.ids.bg1.move(self.quiz.speed)
        self.ids.bg2.move(self.quiz.speed)
        self.ids.bg3.move(self.quiz.speed)

        if self.manager.current == "main":
            self.limit_timer -= 1 / 80


class Background(Widget):
    def move(self, speed):
        """
        背景画像を横に動かす
        """
        self.x -= speed
        # print(self.pos)
        if self.x <= -self.width / 1.2:
            self.x = self.width / 1.1


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
        
        self.init_game_stat()

    def init_game_stat(self):
        """
        ゲーム内のステータスを初期化する
        """
        self.speed = 0.5

    def random_pick_problems(self, required: int):
        """
        問題となる英単語をランダムで複数ピックアップする
        """
        self.random_problems = random.sample(self.problems, required)
        print(self.random_problems)
        return self.random_problems

    def next_problem(self):
        """
        問題を切り替える
        """
        self.current = self.random_problems.pop(0)

    def check_input(self, input):
        """
        入力が正解かどうか判定する
        """
        # print(input, self.current[0])
        if input == self.current[0]:
            return True
        else:
            return False


class App(App):
    def build(self):
        GUI = Builder.load_file("typing.kv")
        return GUI


if __name__ == "__main__":
    App().run()