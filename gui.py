import pygame
import pygame_gui
import face_recognition
import os
import cv2
import time
from transitions import Machine

pygame.init()



class Bipolar:
    def __init__(self,machine_name):
        self.states = ['MachineActive', 'MachineInactive']
        self.machine = Machine(model=self, states=self.states, initial='MachineInactive')
        self.machine.add_transition(trigger='identified', source = 'MachineInactive', dest = 'MachineActive')
        self.machine.add_transition(trigger='not_identified', source = 'MachineActive', dest = 'MachineInactive')

    def start(self):
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)

        X = 800
        Y = 600
        pygame.display.set_caption('Facial Recognition')
        font = pygame.font.Font('freesansbold.ttf', 32)

        # while True:
        # 	display_surface.blit(text, textRect)

        window_surface = pygame.display.set_mode((800, 600))

        background = pygame.Surface((800, 600))
        background.fill(pygame.Color('#000000'))

        manager = pygame_gui.UIManager((800, 600))

        hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((325, 350), (100, 50)),text='Capture', manager=manager)
        # click = pygame.mouse.get_pressed()
        clock = pygame.time.Clock()
        is_running = True
        i=0
        while is_running:
            text = font.render('Start Recognizing!!', True, green, blue)
            textRect = text.get_rect()
            textRect.center = (X // 2, Y // 2)
            time_delta = clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == hello_button:
                            self.show_image2()
                            
                manager.process_events(event)

            manager.update(time_delta)

            # window_surface.blit(background, (0, 0))
            window_surface.blit(text, textRect)
            manager.draw_ui(window_surface)

            pygame.display.update()  




    def recog(self):
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
                        cv2.putText(frame, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 2)

                    cv2.imshow(filename, frame)
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
        # i=1
        # return i
    def show_image2(self):
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)

        X = 800
        Y = 600
        pygame.display.set_caption('Facial Recognition')
        font = pygame.font.Font('freesansbold.ttf', 32)

        # while True:
        # 	display_surface.blit(text, textRect)

        window_surface = pygame.display.set_mode((800, 600))

        background = pygame.Surface((800, 600))
        background.fill(pygame.Color('#000000'))

        manager = pygame_gui.UIManager((800, 600))

        hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((325, 350), (100, 50)),text='Capture', manager=manager)
        # click = pygame.mouse.get_pressed()
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
        self.recog()
        pygame.quit()

  
    
    

    
    
if __name__=="__main__":
    bipolar = Bipolar("Face Recognition in Pygame")
    bipolar.start()
