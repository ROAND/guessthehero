__version__ = '0.8.0'
import kivy
from kivy.utils import platform
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.clock import Clock
from threading import Thread
import hero_voices
import random
import time
import os
import logging
logger = logging.getLogger('spam_application')
fh = logging.FileHandler('data/guessthehero.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
try:
    from urllib.request import urlretrieve
except:
    from urllib import urlretrieve

hero_names_rads = ['Earthshaker', 'Sven', 'Tiny', 'Kunkka', 'Beastmaster', 'Dragon_Knight', 'Clockwerk', 'Omniknight', 'Huskar', 'Alchemist', 'Brewmaster',
                   'Treant_Protector', 'Io', 'Centaur_Warrunner', 'Timbersaw', 'Bristleback', 'Tusk', 'Elder_Titan', 'Legion_Commander', 'Earth_Spirit', 'Phoenix']
hero_names_rada = ['Anti-Mage', 'Drow_Ranger', 'Juggernaut', 'Mirana', 'Morphling', 'Phantom_Lancer', 'Vengeful_Spirit', 'Riki',
                   'Sniper', 'Templar_Assassin', 'Luna', 'Bounty_Hunter', 'Ursa', 'Gyrocopter', 'Lone_Druid', 'Naga_Siren', 'Troll_Warlord', 'Ember_Spirit']
hero_names_radi = ['Crystal_Maiden', 'Puck', 'Tinker', 'Windranger', 'Zeus', 'Storm_Spirit', 'Lina', 'Shadow_Shaman', 'Natures_Prophet',
                   'Enchantress', 'Jakiro', 'Chen', 'Silencer', 'Ogre_Magi', 'Rubick', 'Disruptor', 'Keeper_of_the_Light', 'Skywrath_Mage']
hero_names_dirs = ['Axe', 'Pudge', 'Sand_King', 'Slardar', 'Tidehunter', 'Wraith_King', 'Lifestealer',
                   'Night_Stalker', 'Doom', 'Spirit_Breaker', 'Lycan', 'Chaos_Knight', 'Undying', 'Magnus', 'Abaddon']
hero_names_dira = ['Bloodseeker', 'Shadow_Fiend', 'Razor', 'Venomancer', 'Faceless_Void', 'Phantom_Assassin',
                   'Viper', 'Clinkz', 'Broodmother', 'Weaver', 'Spectre', 'Meepo', 'Nyx_Assassin', 'Slark', 'Medusa', 'Terrorblade']
hero_names_diri = ['Bane', 'Lich', 'Lion', 'Witch_Doctor', 'Enigma', 'Necrophos', 'Warlock', 'Queen_of_Pain', 'Death_Prophet',
                   'Pugna', 'Dazzle', 'Leshrac', 'Dark_Seer', 'Batrider', 'Ancient_Apparition', 'Invoker', 'Outworld_Devourer', 'Shadow_Demon', 'Visage']

# All heroes separated by category
all_heroes = [hero_names_rads, hero_names_rada, hero_names_radi,
              hero_names_dirs, hero_names_dira, hero_names_diri]
deletables = []
base_points = 10
base_lose_points = 40


class MenuUI(FloatLayout):

    def __init__(self, **kwargs):
        super(MenuUI, self).__init__(**kwargs)

    def start_game(self):
        self.ids.sg_button.opacity = 0
        self.ids.sg_button.disabled = True

        self.main = MainUI(self)
        self.add_widget(self.main)

    def remove_instance(self):
        self.remove_widget(self.main)
        self.main = None
        self.__init__()

kill_phrases = ['Ownage!', 'Double Tap!',
                'Killing Spree!', 'Ultra Kill', 'Rampage!']

platform = platform()

if platform == 'android':
    import gs_android
    achievementKillingSpree="CgkI--nlpJAYEAIQAg"
    achievementDominating="CgkI--nlpJAYEAIQAw"
    achievementMegaKill="CgkI--nlpJAYEAIQBA"
    achievementUnstoppable="CgkI--nlpJAYEAIQBQ"
    achievementWickedSick="CgkI--nlpJAYEAIQBg"
    achievementMonsterKill="CgkI--nlpJAYEAIQBw"
    achievementGodlike="CgkI--nlpJAYEAIQCA"
    achievementBeyondGodlike="CgkI--nlpJAYEAIQCQ"
    leaderboardScore="CgkI--nlpJAYEAIQAA"
    achievements = {'Killing_Spree':achievementKillingSpree,
                    'Dominating':achievementDominating,
                    'Mega_Kill':achievementMegaKill,
                    'Unstoppable':achievementUnstoppable,
                    'Wicked_Sick':achievementWickedSick,
                    'Monster_Kill':achievementMonsterKill,
                    'Godlike':achievementGodlike,
                    'Beyond_Godlike':achievementGodlike}

class GooglePlayPopup(Popup):
    def __init__(self, main_ui, **kwargs):
        super(GooglePlayPopup, self).__init__(**kwargs)
        self.main_ui = main_ui

    def activate_google_play(self):
        self.main_ui.activate_google_play()
        


class MainUI(FloatLayout):

    def __init__(self, menu, **kwargs):
        super(MainUI, self).__init__(**kwargs)
        self.previous_buttons = list()
        self.seconds = 10
        self.score = 0
        self.time = 0
        self.wins = 0
        self.lives = 3
        self.sound = SoundLoader.load('data/sounds/match_ready_no_focus.wav')
        self.prepare_clock()
        self.next_selected, self.next_winner = self.choose_hero(
            random.choice(all_heroes))
        self.download_next_sound()
        self.menu = menu
        # self.ids.label_lives.text=str(self.lives+1)
        self.show_lives()
        self.use_google_play = 0#1

        if platform == 'android':
            #self.use_google_play = self.config.getint('play', 'use_google_play')
            if self.use_google_play:
                gs_android.setup(self)
            else:
                Clock.schedule_once(self.ask_google_play, .5)

    def gs_show_leaderboard(self):
        if platform == 'android':
            if self.use_google_play:
                gs_android.show_leaderboard(leaderboardScore)
            else:
                self.ask_google_play()

    def ask_google_play(self, *args):
        popup = GooglePlayPopup(self)
        popup.open()

    def activate_google_play(self):
        self.use_google_play = 1
        gs_android.setup(self)

    def upload_score(self, score):
        if platform == 'android' and self.use_google_play:
            gs_android.leaderboard(leaderboardScore, score)

    def show_lives(self):
        self.ids.box_lives.clear_widgets()
        for i in range(self.lives):
            life = Image(
                source='data/images/heart_of_tarrasque.png', size_hint=(0.8, 0.8))
            self.ids.box_lives.add_widget(life)

    def prepare_clock(self):
        self.time = 3
        Clock.schedule_once(self.start, 3)
        Clock.schedule_interval(self.update_time, 0.1)
        self.ids.winlose_label.text = 'Preparing...'

    def start(self, *args):
        self.load_next(True)
        Clock.schedule_interval(self.load_next, self.seconds)
        Clock.unschedule(self.update_time)
        Clock.schedule_interval(self.update_time, 0.1)

    def update_time(self, *args):
        self.time = self.time - 0.1
        if self.time >= 0:
            self.ids.label_time.text = str(self.time)
            self.ids.pbar.value = self.time

    def stop_time(self, *args):
        Clock.unschedule(self.update_time)
        Clock.unschedule(self.load_next)

    def download_next_sound(self):
        for hero_voice in hero_voices.voices:
            if self.next_winner in hero_voice['name']:
                link = random.choice(hero_voice['voices'])
                name = link.rsplit('/', 1)[1]
                if name != deletables[0:]:
                    deletables.append(name)
                print(deletables)
                try:
                    if len(deletables) >= 4:
                        os.remove(
                            os.path.join('data/sounds/voices/', deletables[0]))
                        deletables[0] = None
                        del(deletables[0])
                    urlretrieve(
                        link, os.path.join('data/sounds/voices/', name))
                except Exception as e:
                    logger.error(
                        '%s - Error downloading file, most likely without internet connection' % time.asctime())

    def load_next(self, *args):
        for arg in args:
            if arg == True:
                pass
            else:
                # Downgrades score when not clicking anything
                self.downgrade_score()
                # This method does not actually destroy the instance unless the
                # lives are under 0
                self.destroy_instance()

        self.ids.winlose_label.text = ''
        if self.previous_buttons:
            for button in self.previous_buttons:
                self.ids.options_layout.remove_widget(button)
                del button

        self.winner = self.next_winner
        self.selected = self.next_selected
        self.next_selected, self.next_winner = self.choose_hero(
            random.choice(all_heroes))
        self.tr = Thread(
            target=self.download_next_sound, name='Download_Thread')
        self.tr.start()
        self.create_buttons()

        self.play_winner_sound()
        self.time = self.seconds
        self.ids.question_image.source = 'data/images/question_mark.png'

    def show_popup(self, title, text):
        popup = Popup(
            title=title, content=Label(text=text), size_hint=(0.6, 0.4))
        popup.open()

    def update_score(self):
        self.ids.label_score.text = str(self.score)

    def destroy_instance(self):
        if self.lives < 0:
            self.show_popup('GG', 'GAME OVER')
            self.stop_time()
            self.tr.join()
            self.menu.remove_instance()

    def button_click(self, name):
        # Right:
        if self.winner == name:
            self.wins = self.wins + 1
            # Should implement: the faster you click, more points (multiply
            # remaining time by standard points)
            self.ids.question_image.source = 'data/images/%s.png' % self.winner
            if self.time > 0:
                self.upgrade_score()
            else:
                self.score = self.score + base_points
            self.update_score()
            #self.show_popup('Yay!', 'You win!')
            for bt in self.previous_buttons:
                bt.disabled = True
            if self.sound:
                self.sound.play()
            self.stop_time()
            self.prepare_clock()
        # Wrong:
        else:
            # TODO: set error sound and implement a nicer error punishment
            # engine (something like the time goes down a couple of seconds
            # every time the wrong hero is selected
            self.ids.winlose_label.text = 'NO!'
            self.downgrade_score()
            self.wins = 0
            self.update_score()
            self.destroy_instance()

    def upgrade_score(self):
        self.score = self.score + (base_points * self.time)
        self.update_score()

    def downgrade_score(self):
        self.score = self.score - (base_lose_points * (10 - self.time))
        self.lives = self.lives - 1
        self.show_lives()
        #self.ids.box_lives.clear_widgets()
        if self.score < 0:
            self.score = 0
        self.update_score()

    def play_winner_sound(self):
        for hero_voice in hero_voices.voices:
            if self.winner in hero_voice['name']:
                try:
                    #link = random.choice(hero_voice['voices'])
                    #name = link.rsplit('/', 1)[1]
                    name = deletables[len(deletables) - 2]
                    if name:
                        sound_path = os.path.join(
                            'data/sounds/voices/', name)
                        sound = SoundLoader.load(sound_path)
                except Exception as e:
                    self.show_popup('Error', e.message)
                    logger.error(e.message)
                    link = random.choice(hero_voice['voices'])
                    sound = SoundLoader.load(link)

                if sound:
                    try:
                        sound.play()
                    except Exception as e:
                        logger.error(e.message)

    def create_buttons(self):
        #---------- Change buttons ----------------
        self.previous_buttons = []
        for name in self.selected:
            bt = Button(text=name.replace(
                '_', ' '), background_normal='data/images/button_off.png', background_down='data/images/button_on.png')
            bt.bind(on_press=lambda x, hero=name: self.button_click(hero))
            self.previous_buttons.append(bt)
            self.ids['options_layout'].add_widget(bt)
        #------------------------------------------

    def choose_hero(self, hero_names):
        # Select winner ------------
        selected = random.sample(hero_names, 4)
        winner = random.choice(selected)
        return selected, winner


class GuessTheHeroApp(App):

    def build(self):
        self.icon = 'data/images/dota_icon.png'
        self.menu = MenuUI()
        return self.menu

    def on_pause(self):
        if self.menu.main:
            self.menu.main.stop_time()
        return True

    def on_resume(self):
        if self.menu.main:
            self.menu.main.start()

if __name__ == '__main__':
    GuessTheHeroApp().run()
