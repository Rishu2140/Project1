import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up Pygame constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Set up Kivy constants
kivy.config.Config.set('graphics', 'width', str(WIDTH))
kivy.config.Config.set('graphics', 'height', str(HEIGHT))
kivy.config.Config.write()

# Load sounds
coin_sound = SoundLoader.load('coin.wav')
game_over_sound = SoundLoader.load('game_over.wav')

class Player(Widget):
    pass

class Coin(Widget):
    pass

class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.player = Player()
        self.coins = []
        self.score = 0
        self.high_score = 0
        self.game_over_label = Label(text='', font_size=40, pos=(WIDTH/2, HEIGHT/2), anchor_x='center', anchor_y='center')
        self.add_widget(self.player)
        self.add_widget(self.game_over_label)
        self.is_game_over = False

    def update(self, dt):
        if not self.is_game_over:
            self.player.y += 5  # Adjust speed as needed

            # Check for collisions with coins
            for coin in self.coins:
                if self.player.collide_widget(coin):
                    self.score += 1
                    coin_sound.play()
                    self.remove_widget(coin)
                    self.coins.remove(coin)
                    self.spawn_coin()

            # Check for game over condition
            if self.player.y < 0 or self.player.y > HEIGHT:
                self.end_game()

    def spawn_coin(self):
        coin = Coin(pos=(random.randint(0, WIDTH-50), HEIGHT))
        self.coins.append(coin)
        self.add_widget(coin)

    def start_game(self, *args):
        self.clear_widgets()
        self.player = Player()
        self.coins = []
        self.score = 0
        self.is_game_over = False
        self.game_over_label.text = ''
        self.add_widget(self.player)
        self.spawn_coin()
        Clock.schedule_interval(self.update, 1.0 / FPS)

    def end_game(self):
        self.is_game_over = True
        game_over_sound.play()
        self.game_over_label.text = f'GAME OVER\nScore: {self.score}\nHigh Score: {self.high_score}'
        if self.score > self.high_score:
            self.high_score = self.score

# Create the main application
class RunningGameApp(App):
    def build(self):
        game = Game()
        play_button = Button(text='Play', font_size=40, pos=(WIDTH/2, HEIGHT/2), on_press=game.start_game)
        game.add_widget(play_button)
        return game

if __name__ == '__main__':
    RunningGameApp().run()
