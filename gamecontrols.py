from direct.showbase import DirectObject
from math import sin, cos, pi
from panda3d.core import WindowProperties, KeyboardButton


class GameControls(DirectObject.DirectObject):
    def __init__(self, sb, move_fn, mouse_magnitude=30):
        self.base = sb
        self.mouse_magnitude = mouse_magnitude
        self.move_fn = move_fn

        props = WindowProperties()
        props.set_cursor_hidden(True)
        props.set_mouse_mode(WindowProperties.MRelative)
        self.base.win.requestProperties(props)

        tm = self.base.task_mgr
        tm.add(self.mouse_move, 'fp-mouse-move')

    def mouse_move(self, task):
        mw = self.base.mouseWatcherNode
        dy = 0
        if mw.hasMouse():
            dy = mw.getMouseY()
            # re-center
            props = self.base.win.getProperties()
            self.base.win.movePointer(0, int(props.getXSize() / 2), int(props.getYSize() / 2))

        self.move_fn(dy * self.mouse_magnitude)

        return task.cont

