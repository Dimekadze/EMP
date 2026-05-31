import flet as ft
import flet_audio as fta
import asyncio

from audio.metadata import MetadataTrack
from audio.playlist import Playlist
from audio.ui_update import UIUpdate

class AudioControl:
    def __init__(self, page: ft.Page):
        self._page = page
        self.audio = None
        self.current_track_index = 0
        self.current_track_path = None
        self.is_playing = False
        self.total_duration = 0
        self.is_loading = False
        self.is_repeat = False

        self.metadata = MetadataTrack()
        self.playlist = Playlist(page)
        self.ui = UIUpdate(page)

        self.time_slider = None

    def set_ui_elements(self, track_title, time_slider, current_time_label, total_time_label, 
                        play_pause_button, repeat_button, track_artist=None):
        self.time_slider = time_slider
        self.ui.set_ui_elements(
            track_title, time_slider, current_time_label, total_time_label,
            play_pause_button, repeat_button, track_artist
        )
        
        if self.time_slider:
            self.time_slider.on_change = self.on_slider_change

    def on_duration_change(self, e):
        self.total_duration = e.duration.in_milliseconds
        self.ui.total_duration = self.total_duration
        self.ui.update_time_display(self.total_duration)

    def on_position_change(self, e):
        if self.total_duration > 0:
            self.ui.total_duration = self.total_duration
            self.ui.update_position_display(e.position)

    def on_state_change(self, e):
        self.is_playing = (e.state == fta.AudioState.PLAYING)
        self.ui.update_play_pause_button(self.is_playing)

        if e.state == fta.AudioState.COMPLETED:
            asyncio.create_task(self._handle_track_end())

    async def _handle_track_end(self):
        if self.is_repeat:
            await self.load_track(self.current_track_path)
        else:
            await self.next_track()

    async def load_track(self, track_path):
        if not track_path: 
            return

        self.current_track_path = track_path
        metadata = self.metadata.extract_metadata(track_path)
        self.ui.update_ui_with_metadata(metadata)

        if self.audio:
            await self.audio.release()

        self.audio = fta.Audio(
            src=str(track_path.resolve()),
            autoplay=True,
            volume=1,
            balance=0,
            release_mode=fta.ReleaseMode.STOP,
            on_duration_change=self.on_duration_change,
            on_position_change=self.on_position_change,
            on_state_change=self.on_state_change
        )

        self._page.services.clear()
        self._page.services.append(self.audio)
        self._page.update()

    async def play_track(self):
        if self.audio:
            try:
                await self.audio.resume()
            except:
                await self.audio.play()

    async def pause_track(self):
        if self.audio: 
            await self.audio.pause()

    async def next_track(self):
        if self.is_loading or not self.playlist.music_list: 
            return
        try: 
            await self.audio.pause()
        except: 
            pass
        
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist.music_list)
        await self.load_track(self.playlist.music_list[self.current_track_index])

    async def previous_track(self):
        if self.is_loading or not self.playlist.music_list: 
            return
        try: 
            await self.audio.pause()
        except: 
            pass
            
        self.current_track_index = (self.current_track_index - 1) % len(self.playlist.music_list)
        await self.load_track(self.playlist.music_list[self.current_track_index])

    async def on_slider_change(self, e):
        if self.audio and self.total_duration > 0:
            new_position = int((self.time_slider.value / 100) * self.total_duration)
            await self.audio.seek(new_position)

    async def handle_play_pause(self, e):
        if self.is_loading: 
            return
            
        if self.is_playing:
            await self.pause_track()
        else:
            if self.current_track_path: 
                await self.play_track()
            elif self.playlist.music_list: 
                await self.load_track(self.playlist.music_list[0])

    async def skip_next_button(self, e):
        await self.next_track()

    async def skip_previous_button(self, e):
        await self.previous_track()

    async def handle_repeat(self, e):
        self.is_repeat = not self.is_repeat
        self.ui.update_repeat_button(self.is_repeat)