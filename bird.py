import random

from pico2d import load_image, get_time, load_font
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

import game_world
import game_framework
from state_machine import StateMachine

# Boy의 Run Speed 계산

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.1) # 10 pixel 1 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# By Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14


class Fly:

    def __init__(self, bird):
        self.bird = bird

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.bird.frame = (self.bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.bird.x += self.bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        if (self.bird.x < 50) or (self.bird.x > 1600 - 50):
            self.bird.dir *= -1
            self.bird.face_dir *= -1


    def handle_event(self, event):
        pass

    def draw(self):
        if self.bird.face_dir == 1:
            self.bird.image.clip_composite_draw((int(self.bird.frame) % 5) * 183, (2- int(self.bird.frame) // 5) * 168, 183, 168, 3.141592/10, '', self.bird.x - 25, self.bird.y - 25, 100, 100)
        else:
            self.bird.image.clip_composite_draw((int(self.bird.frame) % 5) * 183, (2 - int(self.bird.frame) // 5) * 168, 183, 168, 3.141592/1, 'v', self.bird.x + 25, self.bird.y - 25, 100, 100)
            # print(f'Frame: {self.bird.frame:.2f}, Clip X: {(int(self.bird.frame) % 5) * 183}, Clip Y: {(2 - int(self.bird.frame) // 5) * 168}')



class Bird:
    def __init__(self):

        self.item = None

        self.x, self.y = random.randrange(100, 400), random.randrange(350, 550)
        self.frame = random.randrange(0, FRAMES_PER_ACTION)
        self.face_dir = 1
        self.dir = 1
        self.image = load_image('bird_animation.png')
        self.font = load_font('ENCR10B.TTF', 16)

        self.FLY = Fly(self)
        self.state_machine = StateMachine(
            self.FLY,
            {}
        )



    def update(self):
        self.state_machine.update()


    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))


    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 80, self.y + 20, f'(Time: {get_time():.2f})', (255, 255, 0))