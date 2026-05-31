import flet_audio as fta
import flet as ft
import asyncio

class UIUpdate:
    def __init__(self, page: ft.Page):
        self._page = page
        self.track_title = None
        self.track_artist = None
        self.time_slider = None
        self.current_time_label = None
        self.total_time_label = None
        self.play_pause_button = None
        self.repeat_button = None
        self.total_duration = 0
        self.is_playing = False
        self.is_repeat = False

    def set_ui_elements(self, track_title, time_slider, current_time_label, total_time_label, 
                        play_pause_button, repeat_button, track_artist=None):
        self.track_title = track_title
        self.track_artist = track_artist
        self.time_slider = time_slider
        self.current_time_label = current_time_label
        self.total_time_label = total_time_label
        self.play_pause_button = play_pause_button
        self.repeat_button = repeat_button
        
        # if self.time_slider:
        #     self.time_slider.on_change = self.on_slider_change

    def update_ui_with_metadata(self, metadata):
        if self.track_title:
            self.track_title.value = metadata["title"]
        if self.track_artist:
            self.track_artist.value = metadata["artist"]
        self._page.update()

    def update_time_display(self, ms):
        # self.total_duration = ms.duration.in_milliseconds
        seconds_total = self.total_duration // 1000
        minutes = seconds_total // 60
        seconds = seconds_total % 60

        if self.total_time_label:
            self.total_time_label.value = f"{minutes}:{seconds:02d}"
            self._page.update()

    def update_position_display(self, position_ms):
        if self.total_duration > 0:
            progress = (position_ms / self.total_duration) * 100
            
            if self.time_slider:
                self.time_slider.value = progress

            seconds_total = position_ms // 1000
            minutes = seconds_total // 60
            seconds = seconds_total % 60

            if self.current_time_label:
                self.current_time_label.value = f"{minutes}:{seconds:02d}"
                self._page.update()

    # def on_state_change(self, e):
    #     self.is_playing = (e.state == fta.AudioState.PLAYING)
    #     self.update_play_pause_button()

    #     if e.state == fta.AudioState.COMPLETED:
    #         asyncio.create_task(self._handle_track_end())

    def update_play_pause_button(self, is_playing):
        self.is_playing = is_playing
        if self.play_pause_button:
            if self.is_playing:
                self.play_pause_button.icon = ft.Icons.PAUSE
            else:
                self.play_pause_button.icon = ft.Icons.PLAY_ARROW
            self._page.update()

    def update_repeat_button(self, is_repeat):
        self.is_repeat = is_repeat
        if self.repeat_button:
            if self.is_repeat:
                self.repeat_button.icon = ft.Icons.REPEAT_ONE
            else:
                self.repeat_button.icon = ft.Icons.REPEAT
            self._page.update()