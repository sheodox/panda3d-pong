from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath


def clamp(mn, mx, num):
    return min(mx, (max(mn, num)))


def sign(num):
    return (1, -1)[num < 0]


class PongAI:
    def __init__(self, base: ShowBase, paddle: NodePath, ball: NodePath, max_y_travel: float):
        self.base = base
        self.paddle = paddle
        self.ball = ball
        self.max_y_travel = max_y_travel - 5

        self.move_speed = 0.15

        self.base.taskMgr.add(self.update, 'ai-move')

    def stop(self):
        self.base.task_mgr.remove('ai-move')

    def update(self, task):
        ball_pos = self.ball.get_pos()
        paddle_pos = self.paddle.get_pos()
        delta_pos = ball_pos - paddle_pos

        # clamp y delta this task iteration to the maximum movement speed
        next_y_delta = sign(delta_pos.y) * clamp(0, self.move_speed, abs(delta_pos.y))
        self.paddle.set_y(clamp(-1 * self.max_y_travel, self.max_y_travel, paddle_pos.y + next_y_delta))
        return task.cont
