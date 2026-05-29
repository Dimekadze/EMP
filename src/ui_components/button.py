import flet as ft

class UIComponents:
    def __init__(self, page: ft.Page):
        self.page = page

    def button_create(self, bgcolor, icon, icon_color, icon_size, on_click):
        return ft.IconButton(
            bgcolor = bgcolor,
            icon=icon,
            icon_color=icon_color,
            icon_size=icon_size,
            on_click=on_click,
        )

    def image_create(self):
        pass