from direct.showbase.ShowBaseGlobal import aspect2d
from panda3d.core import TextNode


class Scores:
    def __init__(self):
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

    def update_ui(self):
        self.ai_text.set_text(str(self.scores['ai']))
        self.player_text.set_text(str(self.scores['player']))

    def player_scored(self):
        self.scores['player'] += 1
        self.update_ui()

    def ai_scored(self):
        self.scores['ai'] += 1
        self.update_ui()
