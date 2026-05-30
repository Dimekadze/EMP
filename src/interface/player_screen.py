import flet as ft
import asyncio

class PlayerScreen:
    def __init__(self, page: ft.Page, audio_control):
        self.page = page
        self.audio_control = audio_control

        self.track_title = self._create_track_title()
        self.track_artist = self._create_track_artist()
        self.track_album = self._create_track_album()
        self.time_slider = self._create_time_slider()
        self.current_time = self._create_current_time_label()
        self.total_time = self._create_total_time_label()
        self.play_pause_button = self._create_play_pause_button()
        self.skip_previous_button = self._create_skip_previous_button()
        self.skip_next_button = self._create_skip_next_button()
        self.album_image = self._create_album_image()

        self.audio_control.set_ui_elements(
            track_title=self.track_title,
            track_artist=self.track_artist,
            track_album=self.track_album,
            time_slider=self.time_slider,
            current_time_label=self.current_time,
            total_time_label=self.total_time,
            play_pause_button=self.play_pause_button,
        )

        self.time_slider.on_change = self.audio_control.on_slider_change

    def _create_track_title(self): 
        return ft.Text(
            "Unknown",
            color="#ffffff",
            size=30,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD
        )

    def _create_track_artist(self):
        return ft.Text(
            "Unknown",
            color="#696969",
            size=20,
            text_align=ft.TextAlign.CENTER
        )
    
    def _create_track_album(self):
        return ft.Text(
            "Unknown",
            color="#696969",
            size=14,
            text_align=ft.TextAlign.CENTER
        )

    def _create_time_slider(self):
        return ft.Slider(
            min=0,
            max=100,
            width=450,
            active_color="#FFFFFF",
            inactive_color="#696969",
        )

    def _create_current_time_label(self):
        return ft.Text(
            "0:00", 
            color="#FFFFFF", 
            size=16
        )
    def _create_total_time_label(self):
        return ft.Text(
            "0:00", 
            color="#FFFFFF", 
            size=16
        )

    def _create_play_pause_button(self):
        return ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,
            on_click=lambda e: asyncio.create_task(
                self.audio_control.handle_play_pause(e)
            ),
            style=ft.ButtonStyle(
                icon_size=40,
                icon_color="#FFFFFF",
                bgcolor="#000000",
                side=ft.BorderSide(width=2, color="#FFFFFF"),
                mouse_cursor=ft.MouseCursor.CLICK
            )
        )
    
    def _create_skip_previous_button(self):
        return ft.IconButton(
            icon=ft.Icons.SKIP_PREVIOUS,
            on_click=lambda e: asyncio.create_task(
                self.audio_control.skip_previous_button(e)
            ),
            style=ft.ButtonStyle(
                icon_size=40,
                icon_color="#FFFFFF",
                bgcolor="#000000",
                side=ft.BorderSide(width=2, color="#FFFFFF"),
                mouse_cursor=ft.MouseCursor.CLICK
            )
        )

    def _create_skip_next_button(self):
        return ft.IconButton(
            icon=ft.Icons.SKIP_NEXT,
            on_click=lambda e: asyncio.create_task(
                self.audio_control.skip_next_button(e)
            ),
            style=ft.ButtonStyle(
                icon_size=40,
                icon_color="#FFFFFF",
                bgcolor="#000000",
                side=ft.BorderSide(width=2, color="#FFFFFF"),
                mouse_cursor=ft.MouseCursor.CLICK
            )
        )
    
    def _create_album_image(self):
        return ft.Container(
            border=ft.Border.all(5, "#FFFFFF"),
            border_radius=15,
            padding=20,
            content=ft.Image(
                src="src/assets/images/logo_by_default.png",
                height=250
            )
        )

    def player_screen_create(self):
        return ft.Column( 
            expand=True,
            alignment=ft.Alignment.CENTER,
            margin=ft.Margin.only(top=30),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                self.album_image,

                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    margin=ft.Margin.only(top=10),
                    controls=[
                        self.track_title,
                        self.track_artist,
                    ]
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.current_time,
                        self.time_slider,
                        self.total_time,
                    ]
                ),

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
        