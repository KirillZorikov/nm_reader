from flaskwebgui import FlaskUI
from config.wsgi import application

chrome_path = r'/home/kirill/test/translate_api/chrome-linux/chrome'
chrome_path = r'/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
ui = FlaskUI(application, start_server='django', browser_path=chrome_path)
ui.run()
