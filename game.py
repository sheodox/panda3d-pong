import sys
from direct.showbase.ShowBase import ShowBase, loadPrcFileData
from panda3d.core import CollisionSphere, CollisionNode, CollisionBox, CollisionTraverser, CollisionHandlerEvent, \
    LVector3f, OrthographicLens, CollisionPlane, Plane, LPoint3f

from gamecontrols import GameControls
from flymove import FlyMove
win_w = 1440
win_h = 900
win_aspect = win_w / win_h
loadPrcFileData('', f'win-size {win_w} {win_h}')


class Game:
    def __init__(self, base):
        self.base = base
        self.base.accept("escape", sys.exit)  # Escape quits
        self.base.camera.set_pos(0, 0, 90)
        self.base.camera.set_hpr(0, -90, 0)
        lens = OrthographicLens()
        lens.set_film_size(40 * win_aspect, 40)
        self.base.cam.node().setLens(lens)
        self.gc = GameControls(self.base, self.move_player, mouse_magnitude=3)

        self.base.disable_mouse()
        # debug camera movement
        # self.fm = FlyMove(self)
        # self.camera.set_pos(-20, 0, 10)
        # self.camera.set_hpr(-90, -50, 0)

        self.base.cTrav = CollisionTraverser()
        self.coll_hand_event = CollisionHandlerEvent()
        self.coll_hand_event.addInPattern('into-%in')

        paddle_path = 'models/paddle'
        self.player_paddle = pp = self.load_and_render(paddle_path)
        pp.set_pos(-20, 0, 0)
        pp.set_hpr((90, 0, 0))
        self.ai_paddle = aip = self.load_and_render(paddle_path, copy=True)
        aip.set_pos(20, 0, 0)
        aip.set_hpr((90, 0, 0))

        self.ball = self.load_and_render('models/ball')
        collision_ball = CollisionSphere(0, 0, 0, 1)
        cnodePath = self.ball.attachNewNode(CollisionNode('ball'))
        cnodePath.node().addSolid(collision_ball)
        self.base.cTrav.add_collider(cnodePath, self.coll_hand_event)

        # ball movement
        self.ball_v = LVector3f(-.7, 1, 0)
        self.ball_speed_scale = 0.15
        self.base.task_mgr.add(self.ball_move_task, 'ball-move')

        # set up boundaries on the top and bottom
        self.border_distance = border_distance = 20
        self.top_boundary = self.load_and_render(paddle_path, copy=True)
        self.top_boundary.set_sx(5)
        self.top_boundary.set_y(border_distance)
        self.bottom_boundary = self.load_and_render(paddle_path, copy=True)
        self.bottom_boundary.set_sx(5)
        self.bottom_boundary.set_y(-1 * border_distance)

        horizontal_distance = 30
        self.player_side_plane = CollisionPlane(Plane(LVector3f(1, 0, 0), LPoint3f(-1 * horizontal_distance, 0, 0)))
        self.player_side_cnode = self.base.render.attachNewNode(CollisionNode('pplane'))
        self.player_side_cnode.node().add_solid(self.player_side_plane)
        self.ai_side_plane = CollisionPlane(Plane(LVector3f(-1, 0, 0), LPoint3f(horizontal_distance, 0, 0)))
        self.ai_side_cnode = self.base.render.attachNewNode(CollisionNode('aiplane'))
        self.ai_side_cnode.node().add_solid(self.ai_side_plane)

        # add collision to paddles and walls, everything the ball can reflect off of
        for np in [pp, aip, self.bottom_boundary, self.top_boundary]:
            cs = CollisionBox((0, 0, 0), 5, 0.25, 8)
            cnodePath = np.attachNewNode(CollisionNode('wall'))
            cnodePath.node().addSolid(cs)
            self.base.cTrav.add_collider(cnodePath, self.coll_hand_event)
        self.base.accept('into-wall', self.ball_collision)
        self.base.accept('into-pplane', self.player_side_goal)
        self.base.accept('into-aiplane', self.ai_side_goal)

    def player_side_goal(self, entry):
        print('ai scored')
        print(entry)

    def ai_side_goal(self, entry):
        print('player scored')
        print(entry)

    def ball_collision(self, entry):
        norm = entry.get_surface_normal(self.base.render) * -1
        in_vec = self.ball_v / self.ball_v.length()
        self.ball_v = (norm * norm.dot(in_vec * -1) * 2) + in_vec

    def ball_move_task(self, task):
        self.ball.set_pos(self.ball.get_pos() + self.ball_v * self.ball_speed_scale)
        return task.cont

    def load_and_render(self, model_path, copy=False):
        if copy:
            model = self.base.loader.loadModelCopy(model_path)
        else:
            model = self.base.loader.loadModel(model_path)
        model.reparent_to(self.base.render)
        return model

    def move_player(self, dy):
        self.player_paddle.set_y(
            max(-1 * self.border_distance, min(self.border_distance, self.player_paddle.get_y() + dy))
        )
