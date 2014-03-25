import sys
from bs4 import BeautifulSoup
import urllib

hero_names=['Anti-mage','Drow Ranger','Juggernaut','Mirana','Morphling','Phantom Lancer','Vengeful Spirit','Riki','Sniper','Templar Assassin','Luna','Bountry Hunter','Ursa','Gyrocopter','Lone Druid','Naga Siren','Troll Warlord','Ember Spirit']
for name in hero_names:
    url="http://dota2.gamepedia.com/File:%s.png" % name.replace(' ','_')
    filename=url.rsplit('/', 1)[1].replace('File:','')
    urllib.urlretrieve(url, filename)
