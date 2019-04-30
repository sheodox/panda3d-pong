import sys

from direct.gui.DirectButton import DirectButton
from direct.gui.OnscreenText import OnscreenText


class MainMenu:
    def __init__(self, base, start_cb):
        self.base = base
        self.start_cb = start_cb

    def show(self):
        OnscreenText(text='Pong', scale=0.2, pos=(0, 0.5, 0), bg=(0, 0, 0, 0), fg=(1, 1, 1, 1))
        DirectButton(text='Start', scale=0.12, command=self.start_cb)
        DirectButton(text='Quit', scale=0.12, pos=(0, 0, -0.2), command=sys.exit)
