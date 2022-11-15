from abc import ABC
import re

import pygame as pg
import pygame_gui as pggui

from client.groups import Level, TanksGroup
from client.sprites import TankSprite, PlayerTank
from client.serverinterface import ServerInterface


class GameState(ABC):
    """
    Отрисовка интерфейса/объектов
    """
    def draw(self):
        pass
    """
    Обработка ввода
    """
    def handle_events(self):
        pass
    """
    Что должно происходить после выхода из цикла
    """
    def stop(self):
        pass

    def init(self):
        pass


class MenuGameState(GameState):

    def __init__(self, game):
        self.game = game
        self.manager = self.game.manager
        self.manager.clear_and_reset()
        self.panel = pggui.elements.UIPanel(pg.Rect((0, 0), (250, 412)), anchors={'center': 'center'},
                                    manager=self.manager, starting_layer_height=50)

        self.logo = pggui.elements.UIImage(pg.Rect((0, 0), (220, 200)),
                                           pg.image.load("resources\\tanks.png"), anchors={"centerx": "centerx"},
                                        manager=self.manager, container=self.panel)

        self.nickname_entry = pggui.elements.UITextEntryLine(pg.Rect((-3, 200), (200, 50)),
                                                             manager=self.manager, anchors={'centerx': 'centerx'},
                                                            container=self.panel, initial_text="Player")
        self.nickname_entry.set_text_length_limit(10)
        self.ip_entry = pggui.elements.UITextEntryLine(pg.Rect((-3, 250),(200, 50)),
                                                       manager=self.manager, anchors={'centerx': 'centerx'},
                                                       container=self.panel, initial_text="127.0.0.1")

        self.port_entry = pggui.elements.UITextEntryLine(pg.Rect((-3, 300), (200, 50)),
                                                         manager=self.manager, anchors={'centerx': 'centerx'},
                                                         container=self.panel, initial_text="25565")
        self.port_entry.set_allowed_characters("numbers")
        self.button = pggui.elements.UIButton(pg.Rect((-3, 350), (200, 50)),
                                              manager=self.manager, anchors={'centerx': 'centerx'},
                                              container=self.panel, text="connect")
    def draw(self):
        self.game.screen.fill((0, 0, 0))
        self.manager.draw_ui(self.game.screen)
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.stop()
            elif event.type == pg.QUIT:
                self.stop()
            if event.type == pggui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button:
                    self.connect()
            self.manager.process_events(event)

    def connect(self):
        try:
            self.game.server = ServerInterface(self.ip_entry.get_text(), int(self.port_entry.get_text()))
            self.game.server.connect(self.nickname_entry.get_text())
            self.game.set_state(InGameState(self.game))
        except:
            pggui.windows.UIMessageWindow(pg.Rect((300-50, 200), (300, 200)),
                                          "Не удалось подключиться к серверу.",
                                          manager=self.manager, window_title="Ошибка",
                                          )

    def stop(self):
        self.game.running = False

    def update(self):
        time_delta = self.game.game_clock.tick(60)/1000.0
        self.manager.update(time_delta)


class InGameState(GameState):

    def __init__(self, game):
        self.game = game
        self.manager = self.game.manager
        self.manager.clear_and_reset()
        self.screen = game.screen
        self.server = self.game.server
        self.client_sprite = PlayerTank(self.server.respawn())
        self.client_tank = pg.sprite.GroupSingle(self.client_sprite)
        self.level = Level((64, 64))
        self.enemy_tanks = None
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.manager.draw_ui(self.screen)
        self.level.draw(self.screen)
        self.client_tank.draw(self.screen)
        self.enemy_tanks.draw(self.screen)

        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            self.client_sprite.handle_input(event)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.stop()
            elif event.type == pg.QUIT:
                self.stop()
    
    def stop(self):
        self.server.disconnect()
        self.game.set_state(MenuGameState(self.game))

    def update(self):
        dt = self.game.game_clock.tick(60)
        self.manager.update(dt/1000.0)
        tanks_data = self.server.get_positions()
        self.enemy_tanks = TanksGroup([TankSprite(nickname, [0, 0]) for nickname in tanks_data])
        self.enemy_tanks.update(tanks_data)

        if self.client_sprite.is_moving():
            self.client_tank.update(dt)
            if (pg.sprite.spritecollide(self.client_sprite, self.level, dokill=False)
                or pg.sprite.spritecollide(self.client_sprite, self.enemy_tanks, dokill=False)):
                self.client_sprite.undo_move()
            self.server.send_position([self.client_sprite.rect.x, self.client_sprite.rect.y], self.client_sprite.angle//90)