import flet as ft
import flet_audio as fta
from pathlib import Path
import getpass

from interface.all_screens import AllScreens
from additions.config import Config

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.config = Config(page)
        self.audio_player = AllScreens(page)

    def app_create(self):
        self.config.app_configurations()
        screen = self.audio_player.merging_screens()
        self.page.add(screen)
        self.page.update()
