import pygame as pg
import config

class View:
    def __init__(self):
        self.screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pg.display.set_caption("MonsterRunner")
        self.font = pg.font.Font(None, 50)

    def draw_ground(self, session):
        for segment in session.ground.segment_list:
            screen_pos = session.camera.apply(segment["pos"])
            pg.draw.rect(self.screen, config.GREEN, (screen_pos.x, screen_pos.y, segment["width"], segment["height"]))

    def draw_player(self, session):
        player = session.player
        screen_pos = session.camera.apply(session.player.pos)
        pg.draw.rect(self.screen, config.BLUE, (screen_pos.x, screen_pos.y, player.width, player.height))

    def draw_obstacles(self, session):
        for obstacle in session.obstacles.obstacle_list:
            screen_pos = session.camera.apply(obstacle["pos"])
            pg.draw.rect(self.screen, config.RED, (screen_pos.x, screen_pos.y, obstacle["width"], obstacle["height"]))

    def render(self, session):
        self.screen.fill(config.WHITE)

        self.draw_ground(session)
        self.draw_player(session)
        self.draw_obstacles(session)

        pg.display.flip()
