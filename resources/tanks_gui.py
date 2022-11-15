import pygame
import pygame_gui

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((400, 400))

# surf = pygame.Surface((400, 400))
background = pygame.Surface((400, 400))
background.fill(pygame.Color('orange'))



manager = pygame_gui.UIManager((400, 400))

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 200),
                                                                      (120, 50)),
                                            text='Start Game',
                                            manager=manager)
quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 260),
                                                                     (120, 50)),
                                            text='Quit Game',
                                            manager=manager)

clock = pygame.time.Clock()
is_running = True


while is_running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                print('Приложение должно запуститься')
            elif event.ui_element == quit_button:
                print('Закрываем приложение')
                is_running = False
        manager.process_events(event)
    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()