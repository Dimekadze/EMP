import flet as ft

from interface.main_screen import MainScreen
from interface.player_screen import PlayerScreen
from interface.playlist_screen import PlaylistScreen
from interface.settings_screen import SettingsScreen

from audio.audio_control import AudioControl

class AllScreens:
    def __init__(self, page: ft.Page):
        self.page = page

        # controls
        self.audio_control = AudioControl(page)

        # interfaces
        self.main_screen = MainScreen(page)
        self.player_screen = PlayerScreen(page, self.audio_control)
        self.playlist_screen = PlaylistScreen(page)
        self.settings_screen = SettingsScreen(page)

    # merge screens
    def merging_screens(self):
        return self.player_screen.player_screen_create()