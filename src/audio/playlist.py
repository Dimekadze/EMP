import getpass
from pathlib import Path

class Playlist:
    def __init__(self, page):
        self._page = page
        self._extensions = ["mp3", "flac", "ogg", "m4a", "wav"]
        self.username = getpass.getuser()
        self.music_folder = Path(f"/home/{self.username}/Music")
        self.music_list = self._music_scan()

    def _music_scan(self):
        return [
            path for ext in self._extensions 
            for path in self.music_folder.rglob(f"*.{ext}")
        ]