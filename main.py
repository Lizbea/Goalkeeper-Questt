import random
from pygame import Rect
import pgzrun

WIDTH = 800
HEIGHT = 480

game_state = 'menu'
music_on = True
score = 0

# Sons
kick_sound = sounds.kick # type: ignore
save_sound = sounds.save # type: ignore
fail_sound = sounds.fail # type: ignore

# Música
music.set_volume(0.4) # type: ignore
music.play('bg_music') # type: ignore

# Menu botões
menu_buttons = {
    'start': Rect(300, 140, 200, 50),
    'music': Rect(300, 220, 200, 50),
    'exit': Rect(300, 300, 200, 50)
}

# Heroi: o goleiro
class Goalkeeper(Actor): # type: ignore
    def __init__(self):
        super().__init__('keeper_idle1', (WIDTH // 2, 400))
        self.positions = [200, 400, 600]
        self.index = 1
        self.anim_frame = 0
        self.idle_images = ['keeper_idle1', 'keeper_idle2']
        self.dive_left = 'keeper_dive_left1'
        self.dive_right = 'keeper_dive_right1'

    def move_left(self):
        if self.index > 0:
            self.index -= 1
            self.image = self.dive_left
            self.x = self.positions[self.index]

    def move_right(self):
        if self.index < 2:
            self.index += 1
            self.image = self.dive_right
            self.x = self.positions[self.index]

    def idle(self):
        self.anim_frame = (self.anim_frame + 1) % 20
        if self.anim_frame < 10:
            self.image = self.idle_images[0]
        else:
            self.image = self.idle_images[1]

# Inimigo: bola chutada
class Ball(Actor): # type: ignore
    def __init__(self):
        lane = random.choice([200, 400, 600])
        super().__init__('ball1', (lane, -50))
        self.speed = random.uniform(3, 6)
        self.anim = ['ball1', 'ball2']
        self.frame = 0

    def update(self):
        self.y += self.speed
        self.frame += 1
        if self.frame % 10 == 0:
            self.image = self.anim[self.frame // 10 % 2]

goalkeeper = Goalkeeper()
balls = []

def update():
    global game_state, balls, score
    if game_state == 'playing':
        goalkeeper.idle()
        for ball in balls:
            ball.update()
            if ball.y > 370 and abs(ball.x - goalkeeper.x) < 40:
                if music_on:
                    save_sound.play()
                balls.remove(ball)
                score += 1
            elif ball.y > 450:
                if music_on:
                    fail_sound.play()
                game_state = 'menu'
                balls.clear()
                score = 0
        if random.randint(0, 50) == 0:
            if music_on:
                kick_sound.play()
            balls.append(Ball())

def draw():
    screen.clear() # type: ignore
    if game_state == 'menu':
        screen.draw.text("GOALKEEPER QUEST", center=(WIDTH // 2, 80), fontsize=60) # type: ignore
        screen.draw.filled_rect(menu_buttons['start'], 'green') # type: ignore
        screen.draw.text("Start Game", center=menu_buttons['start'].center, fontsize=30) # type: ignore
        screen.draw.filled_rect(menu_buttons['music'], 'blue') # type: ignore
        txt = "Music: ON" if music_on else "Music: OFF"
        screen.draw.text(txt, center=menu_buttons['music'].center, fontsize=30) # type: ignore
        screen.draw.filled_rect(menu_buttons['exit'], 'red') # type: ignore
        screen.draw.text("Exit", center=menu_buttons['exit'].center, fontsize=30) # type: ignore
    elif game_state == 'playing':
        goalkeeper.draw()
        for ball in balls:
            ball.draw()
        screen.draw.text(f"Saves: {score}", (10, 10), fontsize=40, color="white") # type: ignore

def on_key_down(key):
    if game_state == 'playing':
        if key == keys.LEFT: # type: ignore
            goalkeeper.move_left()
        elif key == keys.RIGHT: # type: ignore
            goalkeeper.move_right()

def on_mouse_down(pos):
    global game_state, music_on
    if game_state == 'menu':
        if menu_buttons['start'].collidepoint(pos):
            game_state = 'playing'
        elif menu_buttons['music'].collidepoint(pos):
            music_on = not music_on
            if music_on:
                music.play('bg_music') # type: ignore
            else:
                music.stop() # type: ignore
        elif menu_buttons['exit'].collidepoint(pos):
            exit()

pgzrun.go()
