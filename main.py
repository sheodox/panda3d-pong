import sys
from direct.showbase.ShowBase import ShowBase, loadPrcFileData
from game import Game
win_w = 1440
win_h = 900
win_aspect = win_w / win_h
loadPrcFileData('', f'win-size {win_w} {win_h}')


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept("escape", sys.exit)  # Escape quits
        self.set_background_color(0, 0, 0)
        self.game = Game(self)

app = MyApp()
app.run()
