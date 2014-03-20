import kivy
from kivy import platform
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
#if platform == 'android':
#    from jnius import autoclass
import random
#from kivy.core.window import WindowBase, Window

hero_names_rads=['Earthshaker','Sven','Tiny','Kunkka','Beastmaster','Dragon_Knight','Clockwerk','Omniknight','Huskar','Alchemist','Brewmaster','Treant_Protector','Io','Centaur_Warrunner','Timbersaw','Bristleback','Tusk','Elder_Titan','Legion_Commander','Earth_Spirit','Phoenix']
hero_names_rada=['Anti-Mage', 'Drow_Ranger','Juggernaut','Mirana','Morphling','Phantom_Lancer', 'Vengeful_Spirit','Riki','Sniper','Templar_Assassin','Luna','Bounty_Hunter','Ursa','Gyrocopter','Lone_Druid','Naga_Siren','Troll_Warlord','Ember_Spirit']
hero_names_radi=['Crystal_Maiden','Puck','Tinker','Windranger','Zeus','Storm_Spirit','Lina','Shadow_Shaman','Natures_Prophet','Enchantress','Jakiro','Chen','Silencer','Ogre_Magi','Rubick','Disruptor','Keeper_of_the_Light','Skywrath_Mage']
hero_names_dirs=['Axe','Pudge','Sand_King','Slardar','Tidehunter','Wraith_King','Lifestealer','Night_Stalker','Doom','Spirit_Breaker','Lycan','Chaos_Knight','Undying','Magnus','Abaddon']
hero_names_dira=['Bloodseeker','Shadow_Fiend','Razor','Venomancer','Faceless_Void','Phantom_Assassin','Viper','Clinkz','Broodmother','Weaver','Spectre','Meepo','Nyx_Assassin','Slark','Medusa','Terrorblade']
hero_names_diri=['Bane','Lich','Lion','Witch_Doctor','Enigma','Necrophos','Warlock','Queen_of_Pain','Death_Prophet','Pugna','Dazzle','Leshrac','Dark_Seer','Batrider','Ancient_Apparition','Invoker','Outworld_Devourer','Shadow_Demon','Visage']


class MainUI(FloatLayout):

    def __init__(self, **kwargs):
        super(MainUI, self).__init__(**kwargs)
        all_heroes = [hero_names_rads, hero_names_rada, hero_names_radi, hero_names_dirs, hero_names_dira, hero_names_diri]
        self.colocar_botoes(random.choice(all_heroes))
        if platform == 'android':
            self.sound = SoundLoader.load('data/sounds/match_ready_no_focus.wav')
            #MediaPlayer = autoclass('android.media.MediaPlayer')
            #self.asound = MediaPlayer()
            #self.asound.setDataSource('data/sounds/match_ready_no_focus.wav')
            #self.asound.prepare()
        else:
            self.sound = SoundLoader.load('data/sounds/match_ready_no_focus.wav')

    def button_click(self, name):
        if platform == 'android':
            #self.asound.play() 
            self.sound.play()
        else:
            if self.sound:
                self.sound.play()

    def colocar_botoes(self, hero_names):
        selected = random.sample(hero_names, 4)
        self.winner = random.choice(selected)
        for name in selected:
            bt = Button(text=name.replace('_',' '), background_normal='data/images/button_off.png', background_down='data/images/button_on.png')
            bt.bind(on_press=lambda x, hero=name: self.button_click(hero))
            self.ids['options_layout'].add_widget(bt)
   
class GuessTheHeroApp(App):

    def build(self):
        self.icon = 'data/images/dota_icon.png'
        return MainUI()

if __name__=='__main__':
    GuessTheHeroApp().run()
