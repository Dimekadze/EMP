import flet as ft
import flet_audio as fta
import getpass
from pathlib import Path
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.mp4 import MP4

class AudioControl:
    def __init__(self, page: ft.Page):
        self._page = page
        self.audio = None
        self.current_track_index = 0
        self.current_track_path = None
        self.is_playing = False
        self.total_duration = 0
        self.is_loading = False

        self.track_title = None
        self.track_album = None
        self.track_artist = None
        self.time_slider = None
        self.current_time_label = None
        self.total_time_label = None
        self.play_pause_button = None

        self._extensions = ["mp3", "flac", "ogg", "m4a", "wav"]
        self.username = getpass.getuser()
        self.music_folder = Path(f"/home/{self.username}/Music")
        self.music_list = [
            path for ext in self._extensions 
            for path in self.music_folder.rglob(f"*.{ext}")
        ]
        
    def set_ui_elements(self, track_title, time_slider, current_time_label, total_time_label, 
                    play_pause_button, track_artist=None, track_album=None):
        self.track_title = track_title
        self.track_artist = track_artist
        self.track_album = track_album
        self.time_slider = time_slider
        self.current_time_label = current_time_label
        self.total_time_label = total_time_label
        self.play_pause_button = play_pause_button
        
        if self.time_slider:
            self.time_slider.on_change = self.on_slider_change

    # get track metadata
    def extract_metadata(self, file_path):
        metadata = {
            "title": file_path.stem,
            "artist": "Unknown Artist",
            "album": "Unknown Album",
            "duration": 0
        }
        try:
            audio = File(file_path)
            
            if audio is None:
                return metadata
            
            # MP3
            if isinstance(audio, MP3):
                tags = ID3(file_path)
                
                if tags.get('TIT2'):
                    metadata["title"] = str(tags.get('TIT2'))
                
                if tags.get('TPE1'):
                    metadata["artist"] = str(tags.get('TPE1'))
                
                if tags.get('TALB'):
                    metadata["album"] = str(tags.get('TALB'))
            
            # FLAC
            elif isinstance(audio, FLAC):
                metadata["title"] = audio.get("title", [metadata["title"]])[0]
                metadata["artist"] = audio.get("artist", [metadata["artist"]])[0]
                metadata["album"] = audio.get("album", [metadata["album"]])[0]
            
            # OGG Vorbis
            elif isinstance(audio, OggVorbis):
                metadata["title"] = audio.get("title", [metadata["title"]])[0]
                metadata["artist"] = audio.get("artist", [metadata["artist"]])[0]
                metadata["album"] = audio.get("album", [metadata["album"]])[0]
            
            # M4A/MP4
            elif isinstance(audio, MP4):
                metadata["title"] = audio.get("\xa9nam", [metadata["title"]])[0]
                metadata["artist"] = audio.get("\xa9ART", [metadata["artist"]])[0]
                metadata["album"] = audio.get("\xa9alb", [metadata["album"]])[0]
            
            metadata["duration"] = audio.info.length
              
        except Exception as e:
            print(f"Metadata error: {e}")
        
        return metadata
    
    def update_ui_with_metadata(self, metadata):
        if self.track_title:
            self.track_title.value = metadata["title"]
        
        if self.track_artist:
            self.track_artist.value = metadata["artist"]
        
        if self.track_album:
            self.track_album.value = metadata["album"]
        
        self._page.update()

    # sound control
    def on_duration_change(self, e):
        self.total_duration = e.duration.in_milliseconds
        seconds_total = self.total_duration // 1000
        minutes = seconds_total // 60
        seconds = seconds_total % 60

        self.total_time_label.value = f"{minutes}:{seconds:02d}"
        self._page.update()

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
                self._page.update()

    def on_state_change(self, e):
        self.is_playing = (e.state == fta.AudioState.PLAYING)
        self.update_play_pause_button()

    async def load_track(self, track_path):
        self.current_track_path = track_path
        metadata = self.extract_metadata(track_path)
        self.update_ui_with_metadata(metadata)

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

    async def on_slider_change(self, e):
        if self.audio and self.total_duration > 0:
            new_position = int((self.time_slider.value / 100) * self.total_duration)
            await self.audio.seek(new_position)

    # buttons control
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

    def update_play_pause_button(self):
        if self.play_pause_button:
            if self.is_playing:
                self.play_pause_button.icon = ft.Icons.PAUSE
            else:
                self.play_pause_button.icon = ft.Icons.PLAY_ARROW
            self._page.update()

    async def skip_next_button(self, e):
        await self.next_track()

    async def skip_previous_button(self, e):
        await self.previous_track()