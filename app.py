import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates
import pygame_gui
import face_recognition
import os
import cv2
import time
from transitions import Machine
from main import bey
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)


class Bipolar:
    def __init__(self,machine_name):
        self.states = ['MachineActive', 'MachineInactive']
        self.machine = Machine(model=self, states=self.states, initial='MachineInactive')
        self.machine.add_transition(trigger='identified', source = 'MachineInactive', dest = 'MachineActive')
        self.machine.add_transition(trigger='not_identified', source = 'MachineActive', dest = 'MachineInactive')
def show_image2():
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    X = 800
    Y = 600
    pygame.display.set_caption('Facial Recognition')
    font = pygame.font.Font('freesansbold.ttf', 32)


    window_surface = pygame.display.set_mode((800, 600))

    background = pygame.Surface((800, 600))
    background.fill(pygame.Color('#000000'))

    manager = pygame_gui.UIManager((800, 600))

    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((325, 350), (100, 50)),text='Capture', manager=manager)
    clock = pygame.time.Clock()
    is_running = True

    display_width = 800
    display_height = 600
    hello_button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 350), (200, 50)),text='Click when ready!', manager=manager)
    gameDisplay = pygame.display.set_mode((display_width,display_height*2))

    black = (0,0,0)
    white = (255,255,255)

    clock = pygame.time.Clock()
    crashed = False
    carImg = pygame.image.load('cam.jpg')

    def car(x,y):
        gameDisplay.blit(carImg, (x,y))

    x =  (display_width*0.08)
    y = (display_height*0.01)
    
    
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    gameDisplay.fill(white)
    car(x,y)

            
    pygame.display.update()
    clock.tick(60)
    recog()
    pygame.quit()


def recog():
        KNOWN_FACES_DIR = 'known_faces'
        UNKNOWN_FACES_DIR = 'unknown_faces'
        TOLERANCE = 0.6
        FRAME_THICKNESS = 3
        FONT_THICKNESS = 2
        MODEL = 'cnn'

        print('Loading known faces...')
        known_faces = []
        known_names = []

        for name in os.listdir(KNOWN_FACES_DIR):    
            for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
                image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
                encoding = face_recognition.face_encodings(image)[0]
                known_faces.append(encoding)
                known_names.append(name)


        print('Processing unknown faces...')
        for filename in os.listdir(UNKNOWN_FACES_DIR): 
            print(f'Filename {filename}', end='')
            # image = face_recognition.load_image_file(f'{UNKNOWN_FACES_DIR}/{filename}')
            cap = cv2.VideoCapture(0)
            while cap.isOpened():
                ret,frame = cap.read()
                image = frame
                locations = face_recognition.face_locations(image, model=MODEL)
                encodings = face_recognition.face_encodings(image, locations)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                print(f', found {len(encodings)} face(s)')
                
                for face_encoding, face_location in zip(encodings, locations):
                    results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
                    match = None
                    if True in results:
                        match = known_names[results.index(True)]
                        print(f"Match Found: {match}")
                        top_left = (face_location[3], face_location[0])
                        bottom_right = (face_location[1], face_location[2])            
                        color = [0, 255, 0]         
                        cv2.rectangle(frame, top_left, bottom_right, color, FRAME_THICKNESS)

                        top_left = (face_location[3], face_location[2])
                        bottom_right = (face_location[1], face_location[2] + 22)           
                        cv2.rectangle(frame, top_left, bottom_right, color, cv2.FILLED)
                        cv2.putText(frame, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), 2)

                    cv2.imshow(filename, frame)
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - the gamestate change associated with this button
        """
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player:

    def __init__(self, score=0, lives=3, current_level=1):
        self.score = score
        self.lives = lives
        self.current_level = current_level


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            player = Player()
            game_state = play_level(screen, player)

        if game_state == GameState.NEXT_LEVEL:
            player.current_level += 1
            show_image2()

        if game_state == GameState.QUIT:
            bey()
            return


def title_screen(screen):
    start_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Recognize",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(400, 500),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Bored?",
        action=GameState.QUIT,
    )

    buttons = RenderUpdates(start_btn, quit_btn)

    return game_loop(screen, buttons)


def play_level(screen, player):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    nextlevel_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text=f"Capture",
        action=GameState.NEXT_LEVEL,
    )

    buttons = RenderUpdates(return_btn, nextlevel_btn)

    return game_loop(screen, buttons)


def game_loop(screen, buttons):
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXT_LEVEL = 2


if __name__ == "__main__":
    main()
