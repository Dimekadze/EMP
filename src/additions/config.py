import flet as ft
import getpass
from pathlib import Path

class Config:
    def __init__(self, page: ft.Page):
        self.page = page

    # window size settings
    def app_configurations(self):
        self.page.title = "EMP"
        self.page.icon = "src/assets/icons/app_icon.ico"
        self.page.bgcolor = "#000000"

        self.page.window.height = 600
        self.page.window.width = 700

        self.page.window.min_width = 600
        self.page.window.min_height = 700
        
        self.page.window.max_width = 600
        self.page.window.max_height = 700
        
        self.page.window.resizable = True
        # self.page.window.always_on_top = True

