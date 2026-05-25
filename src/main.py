import flet as ft
import flet_audio as fta
from pathlib import Path
import getpass

def main(page: ft.Page):
    page.title = "EMP"
    page.icon = "icons/app_icon.ico"
    page.bgcolor = "#000000"

    # window size settings
    page.window.height = 600
    page.window.width = 700

    page.window.min_width = 600
    page.window.min_height = 700
    
    page.window.max_width = 600
    page.window.max_height = 700
    
    page.window.resizable = True
    # page.window.always_on_top = True

    # getting username
    username = getpass.getuser()

    music_folder = Path(f"/home/{username}/Music")
    music_list = list(music_folder.glob("*.mp3"))

    current_track_index = 0
    current_track_path = None
    is_playing = False
    total_duration = 0
    is_loading = False
    track_loaded = False

    track_music_title = ft.Text(
        "Choose Track",
        color="#ffffff",
        size=30,
        text_align=ft.TextAlign.CENTER,
        margin=ft.Margin.only(top=30)
    )

    time_music_slider = ft.Slider(
        min=0, 
        max=100,
        width=450,
        active_color="#FFFFFF",
        inactive_color="#696969",
    )

    current_time_label = ft.Text(
        "0:00", 
        color="#FFFFFF", 
        size=16
    )
    total_time_label = ft.Text(
        "0:00", 
        color="#FFFFFF", 
        size=16
    )

    def on_duration_change(e):
        nonlocal total_duration

        total_duration = e.duration.in_milliseconds
        seconds_total = total_duration // 1000
        minutes = seconds_total // 60
        seconds = seconds_total % 60

        total_time_label.value = f"{minutes}:{seconds:02d}"

        page.update()

    def on_position_change(e):
        if total_duration > 0:
            position = e.position
            progress = (position / total_duration) * 100
            time_music_slider.value = progress

            seconds_total = position // 1000
            minutes = seconds_total // 60
            seconds = seconds_total % 60

            current_time_label.value = f"{minutes}:{seconds:02d}"

            page.update()

    def on_state_change(e):
        nonlocal is_playing
        is_playing = (e.state == fta.AudioState.PLAYING)

    def on_loaded(e):
        nonlocal track_loaded
        track_loaded = True
        print("Loaded")

    audio = None

    async def load_track(track_path):
        nonlocal current_track_path
        nonlocal audio

        try:
            current_track_path = track_path

            if audio:
                try: 
                    await audio.release()
                except Exception as e: 
                    print("RELEASE ERROR:", e)

            audio = fta.Audio(
                src=str(track_path.resolve()),
                autoplay=True,
                volume=1,
                balance=0,
                release_mode=fta.ReleaseMode.STOP,
                on_loaded=on_loaded,
                on_duration_change=on_duration_change,
                on_position_change=on_position_change,
                on_state_change=on_state_change,
                on_seek_complete=lambda _: print("Seek complete"),
            )

            page.services.clear()
            page.services.append(audio)
            
            track_music_title.value = track_path.stem

            page.update()

        except Exception as e: 
            print("LOAD ERROR:", e)

    async def play_track():
        if audio:
            try:
                await audio.resume()
            except:
                await audio.play()

    async def pause_track():
        if audio: 
            await audio.pause()

    async def next_track():
        nonlocal current_track_index, is_loading
        if is_loading or not music_list: 
            return
        
        try: 
            await audio.pause()
        except: 
            pass
        
        current_track_index = (current_track_index + 1) % len(music_list)
        await load_track(music_list[current_track_index])

    async def previous_track():
        nonlocal current_track_index, is_loading
        if is_loading or not music_list: 
            return
        
        try: 
            await audio.pause()
        except: 
            pass
            
        current_track_index = (current_track_index - 1) % len(music_list)
        await load_track(music_list[current_track_index])

    async def resume():
        await audio.resume()

    async def release():
        await audio.release()

    async def seek_2s():
        await audio.seek(2000)

    async def on_slider_change(e):
        if audio and total_duration > 0:
            try:
                new_position = int((time_music_slider.value / 100) * total_duration)
                await audio.seek(ft.Duration(milliseconds=new_position))

            except Exception as e:
                print("SEEK ERROR:", e)

    async def play_pause_button(e):
        if is_loading: 
            return
            
        if is_playing: 
            await pause_track()
        else:
            if current_track_path: 
                await play_track()
            elif music_list: 
                await load_track(music_list[0])

    async def skip_next_button(e):
        await next_track()

    async def skip_previous_button(e):
        await previous_track()

    def TopArrowButton(e):
        print("hide")
        page.window.minimized = True

    page.add(
        ft.Container( 
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=25,
                controls=[
                    track_music_title,

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
                        current_time_label,
                        time_music_slider,
                        total_time_label,
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=30,
                        controls=[
                            ft.Container( 
                                content=ft.IconButton(
                                    bgcolor="#FFFFFF",
                                    icon=ft.Icons.SKIP_PREVIOUS,
                                    icon_color="#000000",
                                    icon_size=40,
                                    on_click=skip_previous_button,
                                    disabled=False
                                )
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    bgcolor="#FFFFFF",
                                    icon=ft.Icons.PLAY_ARROW,
                                    icon_color="#000000",
                                    icon_size=40,
                                    on_click=play_pause_button,
                                )
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    bgcolor="#FFFFFF",
                                    icon=ft.Icons.SKIP_NEXT,
                                    icon_color="#000000",
                                    icon_size=40,
                                    on_click=skip_next_button,
                                    disabled=False
                                )
                            )
                        ]
                    )
                ]
            )
        )
    )

    time_music_slider.on_change = on_slider_change

if __name__ == "__main__":
    ft.run(main)