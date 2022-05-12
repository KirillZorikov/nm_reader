from django.apps import AppConfig

class ParsersConfig(AppConfig):
    name = 'parsers'
    verbose_name = 'Parsers'

    def ready(self):
        ''' run the browser when the server starts '''
        from utils.browser import get_browser

        # get_browser()