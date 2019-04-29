from direct.showbase.ShowBase import ShowBase
from math import sin
from panda3d.core import NodePath


class PongAI:
    def __init__(self, base: ShowBase, paddle: NodePath, ball: NodePath, max_y_travel: float):
        self.base = base
        self.paddle = paddle
        self.ball = ball
        self.max_y_travel = max_y_travel - 5

        self.move_speed = 0.05

        self.base.taskMgr.add(self.update, 'ai-move')

    def stop(self):
        self.base.task_mgr.remove('ai-move')

    def update(self, task):
        ball_pos = self.ball.get_pos()
        paddle_pos = self.paddle.get_pos()
        delta_pos = ball_pos - paddle_pos
        self.paddle.set_y(
            min(self.max_y_travel, max(-1 * self.max_y_travel, paddle_pos.y + sin(-1 * delta_pos.y)))
        )
        return task.cont
