import pygame as pg
import pygame_gui as pggui

from client.gamestate import GameState, MenuGameState


class Game:
    
    def __init__(self):
        pg.init()
        self.server = None
        self.screen = pg.display.set_mode([800, 600])
        self.manager = pggui.UIManager([800, 600])
        self.game_clock = pg.time.Clock()
        self.running = False
        self.state = MenuGameState(self)

    def process_events(self):
        self.state.handle_events()

    def update(self):
        self.state.update()

    def start(self):
        self.running = True
        # self.connect_and_get_state()
        while self.running:
            self.process_events()
            self.update()
            self.draw()
        self.state.stop()
        pg.quit()

    def draw(self):
        self.state.draw()

    def stop(self):
        self.running = False

    def set_state(self, state: GameState):
        self.state = state

    def get_state(self) -> GameState:
        return self.state
        

if __name__ == "__main__":
    game = Game()
    game.start()