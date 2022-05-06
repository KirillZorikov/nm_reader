from flaskwebgui import FlaskUI
from config.wsgi import application

ui = FlaskUI(application, start_server='django')
ui.run()
