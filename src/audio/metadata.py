from pathlib import Path
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.mp4 import MP4

class MetadataTrack():
    @staticmethod
    def extract_metadata(file_path: Path) -> dict:
        metadata = {
            "title": file_path.stem,
            "artist": "Unknown Artist",
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
            
            # FLAC
            elif isinstance(audio, FLAC):
                metadata["title"] = audio.get("title", [metadata["title"]])[0]
                metadata["artist"] = audio.get("artist", [metadata["artist"]])[0]
            
            # OGG Vorbis
            elif isinstance(audio, OggVorbis):
                metadata["title"] = audio.get("title", [metadata["title"]])[0]
                metadata["artist"] = audio.get("artist", [metadata["artist"]])[0]
            
            # M4A/MP4
            elif isinstance(audio, MP4):
                metadata["title"] = audio.get("\xa9nam", [metadata["title"]])[0]
                metadata["artist"] = audio.get("\xa9ART", [metadata["artist"]])[0]
            
            metadata["duration"] = audio.info.length
              
        except Exception as e:
            print(f"Metadata error: {e}")
        
        return metadata
