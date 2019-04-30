import sys
from direct.showbase.ShowBase import ShowBase, loadPrcFileData, NodePath
from game import Game
from mainmenu import MainMenu

win_w = 1440
win_h = 900
win_aspect = win_w / win_h
loadPrcFileData('', f'win-size {win_w} {win_h}')


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.root_node = None
        self.clean_up()
        self.set_background_color(0, 0, 0)
        self.game = Game(self, self.main_menu)
        self.mm = MainMenu(self, self.start_game)
        self.main_menu()

    def clean_up(self):
        self.ignore_all()
        if self.root_node is not None:
            self.root_node.remove_node()
        for child in self.aspect2d.get_children():
            child.remove_node()
        self.root_node = NodePath('root_node')
        self.root_node.reparent_to(self.render)
        self.accept("escape", sys.exit)  # Escape quits

    def start_game(self):
        self.clean_up()
        self.game.run(self.root_node, self.start_game)

    def main_menu(self):
        self.clean_up()
        self.mm.show()

app = MyApp()
app.run()
