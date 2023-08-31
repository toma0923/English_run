import random
import japanize_kivy
from kivy.app import App, Widget
from kivy.lang import Builder
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ObjectProperty, NumericProperty


class ScreenManagement(ScreenManager):
    pass


class MenuScreen(Screen):
    """
    メニュー画面
    """
    def on_press_select(self):
        self.prep_select_screen()
        self.manager.transition.direction = "left"
        self.manager.current = "select"

    def prep_select_screen(self):
        main_screen = self.manager.get_screen("main")
        select_screen = self.manager.get_screen("select")
        quiz = main_screen.quiz

        for i in range(quiz.len_stage):
            aButton = Button(text=f"STAGE {i+1}              ハイスコア: 0",
                                    on_release=select_screen.on_start)
            aButton.my_id = i
            select_screen.stages.add_widget(aButton)


class SelectScreen(Screen):
    """
    章を選ぶ画面
    """

    def on_start(self, instance):
        selected_stage = instance.my_id
        self.pick_problems(selected_stage)
        self.prep_check_screen()

    def pick_problems(self, selected_stage):
        """
        指定された出題単語数に応じて問題をピックアップするために、random_pick_problems()を呼び出す
        """
        main_screen = self.manager.get_screen("main")
        self.problems = main_screen.quiz.random_pick_problems(selected_stage)

    def prep_check_screen(self):
        """
        単語確認用のスクリーンを用意する
        """
        check_screen = self.manager.get_screen("check")
        check_screen.show_all_problems(self.problems)

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
        main = self.manager.get_screen("main")
        main.bind_keyboard()
        main.on_start()

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "main"   


class ResultScreen(Screen):
    score = NumericProperty(0)
    high_score = NumericProperty(0)

    def on_retry(self):
        menu = self.manager.get_screen("menu")
        menu.prep_check_screen()


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
    time_limit = 60
    limit_timer = NumericProperty(time_limit)
    score = NumericProperty(0)
    speed = NumericProperty(0.5)

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

        self.quiz = Quiz()
        self.input_text = ""
    
    def bind_keyboard(self):
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

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
                self.speed *= 1.2
                self.switch_shown_problem()
            # 不正解ならスピードダウン
            else:
                self.speed *= 0.8
    
        elif text != None:
            # 文字数制限以下なら文字を追加
            if len(self.input_text) < self.len_current_problem:
                self.change_shown_text(add_text=text)

        # print(f"The key {keycode} has been pressed")
        # print(f" - text is {text}")
        # print(' - modifiers are %r' % modifiers)

    def on_start(self):
        self.score = 0
        self.limit_timer = self.time_limit
        self.switch_shown_problem()

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
        self.ids.bg1.move(self.speed)
        self.ids.bg2.move(self.speed)
        self.ids.bg3.move(self.speed)

        if self.manager.current == "main":
            self.limit_timer -= 1 / 80
            self.score += self.speed / 20

            if self.limit_timer < 0:
                self.on_time_up()

    def on_press_menu(self):
        self.quiz.save_high_score(int(self.score))

        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "menu"

    def on_time_up(self):
        self.quiz.save_high_score(self.score)
        result = self.manager.get_screen("result")
        result.score = int(self.score)
        result.high_score = self.quiz.high_score

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "result"


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


class App(App):
    def build(self):
        GUI = Builder.load_file("typing.kv")
        return GUI


if __name__ == "__main__":
    App().run()