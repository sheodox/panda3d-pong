from direct.gui.DirectButton import DirectButton
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBaseGlobal import aspect2d
from panda3d.core import TextNode


class Scores:
    def __init__(self, game_end_cb, game_quit_cb, game_restart_cb):
        self.game_end_cb = game_end_cb
        self.game_quit_cb = game_quit_cb
        self.game_restart_cb = game_restart_cb
        self.win_score = 5
        self.scores = {
            'player': 0,
            'ai': 0
        }

        def make_text(name, align, pos):
            tn = TextNode(name)
            tn.set_text_scale(0.07)
            tn.set_align(align)
            aspect2d.attachNewNode(tn).set_pos(pos)
            return tn
        self.ai_text = make_text('ai-text', TextNode.ARight, (0.7, 0, 0.9))
        self.player_text = make_text('player-text', TextNode.ALeft, (-0.7, 0, 0.9))

        self.update_ui()

    def reset(self):
        self.scores['player'] = 0
        self.scores['ai'] = 0
        self.update_ui()

    def check_for_winner(self):
        def show_winner(winner):
            OnscreenText(text=f'{winner} won!', scale=0.2, bg=(0, 0, 0, 0), fg=(1, 1, 1, 1))
            restart_btn = DirectButton(text=('Restart'), command=self.game_restart_cb)
            restart_btn.set_pos((0, 0, -0.2))
            restart_btn.set_scale(0.1)
            quit_btn = DirectButton(text=('Quit'), command=self.game_quit_cb)
            quit_btn.set_pos((0, 0, -0.4))
            quit_btn.set_scale(0.1)

        if self.scores['ai'] >= self.win_score:
            show_winner('AI')
        elif self.scores['player'] >= self.win_score:
            show_winner('You')
        else:
            return
        self.game_end_cb()

    def update_ui(self):
        self.ai_text.set_text(str(self.scores['ai']))
        self.player_text.set_text(str(self.scores['player']))

    def player_scored(self):
        self.scores['player'] += 1
        self.update_ui()
        self.check_for_winner()

    def ai_scored(self):
        self.scores['ai'] += 1
        self.update_ui()
        self.check_for_winner()
