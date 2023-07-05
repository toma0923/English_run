from kivy.app import App, Widget
from kivy.core.window import Window


class MainDisplay(Widget):
    """
    メインレイアウト
    キーボードからの入力を受け取る
    """

    def __init__(self, **kwargs):
        super(MainDisplay, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(f"The key {keycode} has been pressed")
        print(f" - text is {text}")
        print(' - modifiers are %r' % modifiers)


if __name__ == "__main__":
    from kivy.base import runTouchApp
    runTouchApp(MainDisplay())