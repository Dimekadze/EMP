import flet as ft

from interface.all_screens import AllScreens
from additions.config import Config

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.config = Config(page)
        self.screens = AllScreens(page)

    def app_create(self):
        self.config.app_configurations()
        self.page.add(self.screens.merging_screens())
        self.page.update()
