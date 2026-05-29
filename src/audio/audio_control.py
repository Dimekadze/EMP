import flet as ft
import flet_audio as fta
import getpass
from pathlib import Path

class AudioControl:
    def __init__(self, page: ft.Page):
        self._page = page
        self.audio = None
        self.current_track_index = 0
        self.current_track_path = None
        self.is_playing = False
        self.total_duration = 0
        self.is_loading = False
        self.track_loaded = False

        self.track_title = None
        self.time_slider = None
        self.current_time_label = None
        self.total_time_label = None
        self.play_pause_button = None

        self.username = getpass.getuser()
        self.music_folder = Path(f"/home/{self.username}/Music")
        self.music_list = list(self.music_folder.glob("*.mp3"))

    def set_ui_elements(self, track_title, time_slider, current_time_label, total_time_label, play_pause_button):
        self.track_title = track_title
        self.time_slider = time_slider
        self.current_time_label = current_time_label
        self.total_time_label = total_time_label
        self.play_pause_button = play_pause_button
        
        if self.time_slider:
            self.time_slider.on_change = self.on_slider_change

    @property
    def page(self):
        return self._page

    def update_play_pause_button(self):
        if self.play_pause_button:
            if self.is_playing:
                self.play_pause_button.icon = ft.Icons.PAUSE
            else:
                self.play_pause_button.icon = ft.Icons.PLAY_ARROW
            self.page.update()

    def on_duration_change(self, e):
        self.total_duration = e.duration.in_milliseconds
        seconds_total = self.total_duration // 1000
        minutes = seconds_total // 60
        seconds = seconds_total % 60

        self.total_time_label.value = f"{minutes}:{seconds:02d}"

        self.page.update()

    def on_position_change(self, e):
        if self.total_duration > 0:
            position = e.position
            progress = (position / self.total_duration) * 100
            
            if self.time_slider:
                self.time_slider.value = progress

            seconds_total = position // 1000
            minutes = seconds_total // 60
            seconds = seconds_total % 60

            if self.current_time_label:
                self.current_time_label.value = f"{minutes}:{seconds:02d}"
                self.page.update()

    def on_state_change(self, e):
        self.is_playing = (e.state == fta.AudioState.PLAYING)
        self.update_play_pause_button()

    def on_loaded(self):
        self.track_loaded = True

    async def load_track(self, track_path):
        try:
            self.current_track_path = track_path
            if self.audio:
                await self.audio.release()

            self.audio = fta.Audio(
                src=str(track_path.resolve()),
                autoplay=True,
                volume=1,
                balance=0,
                release_mode=fta.ReleaseMode.STOP,
                on_loaded=self.on_loaded,
                on_duration_change=self.on_duration_change,
                on_position_change=self.on_position_change,
                on_state_change=self.on_state_change,
                on_seek_complete=lambda _: print("Seek complete"),
            )

            self.page.services.clear()
            self.page.services.append(self.audio)
            
            if self.track_title:
                self.track_title.value = track_path.stem

            self.page.update()

        except Exception as e: 
            print("LOAD ERROR:", e)

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
        if self.is_loading or not self.music_list: 
            return
        try: 
            await self.audio.pause()
        except: 
            pass
        
        self.current_track_index = (self.current_track_index + 1) % len(self.music_list)
        await self.load_track(self.music_list[self.current_track_index])

    async def previous_track(self):
        if self.is_loading or not self.music_list: 
            return
        try: 
            await self.audio.pause()
        except: 
            pass
            
        self.current_track_index = (self.current_track_index - 1) % len(self.music_list)
        await self.load_track(self.music_list[self.current_track_index])

    # async def resume(self):
    #     await self.audio.resume()

    # async def release(self):
    #     await self.audio.release()

    # async def seek_2s(self):
    #     await self.audio.seek(2000)

    async def on_slider_change(self, e):
        if self.audio and self.total_duration > 0:
            try:
                # Используем self.time_slider (не time_music_slider)
                new_position = int((self.time_slider.value / 100) * self.total_duration)
                await self.audio.seek(new_position)
                print(f"Seek to: {new_position} ms")
            except Exception as e:
                print("SEEK ERROR:", e)

    async def handle_play_pause(self, e):
        if self.is_loading: 
            return
            
        if self.is_playing:
            await self.pause_track()
        else:
            if self.current_track_path: 
                await self.play_track()
            elif self.music_list: 
                await self.load_track(self.music_list[0])

    async def skip_next_button(self, e):
        await self.next_track()

    async def skip_previous_button(self, e):
        await self.previous_track()

    

