import flet as ft
import asyncio

class PlayerScreen:
    def __init__(self, page: ft.Page, audio_control):
        self.page = page
        self.audio_control = audio_control

        self.track_title = self._track_music_title()
        self.time_slider = self._time_music_slider()
        self.current_time = self._current_time_label()
        self.total_time = self._total_time_label()
        self.play_pause_button = self._create_play_pause_button()
        self.skip_previous_button = self._create_skip_previous_button()
        self.skip_next_button = self._create_skip_next_button()

        self.audio_control.set_ui_elements(
            track_title=self.track_title,
            time_slider=self.time_slider,
            current_time_label=self.current_time,
            total_time_label=self.total_time,
            play_pause_button=self.play_pause_button
        )

        self.time_slider.on_change = self.audio_control.on_slider_change

    def _track_music_title(self): 
        return ft.Text(
        "Choose Track",
        color="#ffffff",
        size=30,
        text_align=ft.TextAlign.CENTER,
        margin=ft.Margin.only(top=30)
    )

    def _time_music_slider(self):
        return ft.Slider(
        min=0,
        max=100,
        width=450,
        active_color="#FFFFFF",
        inactive_color="#696969",
    )

    def _current_time_label(self):
        return ft.Text(
        "0:00", 
        color="#FFFFFF", 
        size=16
    )
    def _total_time_label(self):
        return ft.Text(
        "0:00", 
        color="#FFFFFF", 
        size=16
    )

    def _create_play_pause_button(self):
        return ft.IconButton(
            bgcolor="#FFFFFF",
            icon=ft.Icons.PLAY_ARROW,
            icon_color="#000000",
            icon_size=40,
            on_click=lambda e: asyncio.create_task(
                self.audio_control.handle_play_pause(e)
            ),
        )
    
    def _create_skip_previous_button(self):
        return ft.IconButton(
            bgcolor="#FFFFFF",
            icon=ft.Icons.SKIP_PREVIOUS,
            icon_color="#000000",
            icon_size=40,
            on_click=lambda e: asyncio.create_task(
                self.audio_control.skip_previous_button(e)
            ),
        )

    def _create_skip_next_button(self):
        return ft.IconButton(
            bgcolor="#FFFFFF",
            icon=ft.Icons.SKIP_NEXT,
            icon_color="#000000",
            icon_size=40,
            on_click=lambda e: asyncio.create_task(
                self.audio_control.skip_next_button(e)
            ),
        )

    def player_screen_create(self):
        return ft.Container( 
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=25,
                controls=[
                    self.track_title,

                    ft.Container(
                        border=ft.Border.all(5, "#FFFFFF"),
                        border_radius=15,
                        padding=ft.Padding.symmetric(vertical=20, horizontal=20),
                        content=ft.Image(
                            src="images/logo_by_default.png",
                            height=250
                        )
                    ),

                    ft.Row([
                        self.current_time,
                        self.time_slider,
                        self.total_time,
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=30,
                        controls=[
                            self.skip_previous_button,
                            self.play_pause_button,
                            self.skip_next_button,
                        ]
                    )
                ]
            )
        )