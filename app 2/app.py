from flaskwebgui import FlaskUI
import WebPages as webp
from pyshortcuts import make_shortcut

make_shortcut('/Users/Charlie/Desktop/PillPackDispenser/app/app.py', name='Pill Pack Dispenser', icon='/Users/Charlie/Desktop/PillPackDispenser/app/app_icon')
if __name__ == '__main__':
    webp.ui.run()

 
