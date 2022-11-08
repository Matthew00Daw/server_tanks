from abc import ABC

import pygame as pg
import pygame_gui as pggui

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

class MenuGameState(GameState):

    def __init__(self, game):
        self.manager = game.ui_manager
        self.panel = pggui.elements.UIPanel(pg.Rect((100, 50), (250, 150)), anchors={'left': 'left',
                   'right': 'right',
                   'top': 'top',
                   'bottom': 'bottom'}, manager=self.manager)

        self.nickname_entry = pggui.elements.UITextEntryLine(pg.Rect((100, 50),
                                                       (250, 150)), manager=self.manager,
                                                       container=self.panel, initial_text="Player")
        self.ip_entry = pggui.elements.UITextEntryLine(pg.Rect((0, 0),
                                                       (250, 150)), manager=self.manager,
                                                       container=self.panel, initial_text="127.0.0.1")

        self.port_entry = pggui.elements.UITextEntryLine(pg.Rect((0, 0),
                                                       (250, 150)), manager=self.manager,
                                                       container=self.panel, initial_text="25565")
        self.button = pggui.elements.UIButton(pg.Rect((0, 0),
                                                       (250, 150)), manager=self.manager,
                                                       container=self.panel, text="25565")
    
    def draw(self):
        pass

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.stop()
            elif event.type == pg.QUIT:
                self.stop()

    def stop(self):
        pass


class InGameState(GameState):

    def __init__(self):
        pass
    
    def draw():
        pass

    def handle_events(self):
        for event in pg.event.get():
            self.client_sprite.handle_input(event)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.stop()
            elif event.type == pg.QUIT:
                self.stop()