import flet as ft
import flet_audio as fta
from pathlib import Path
import mutagen as mg
import os

def main(page: ft.Page):
    page.title = "EMP"
    page.icon = "icons/app_icon.ico"
    page.bgcolor = "#000000"

    # page.window.resizable = False
    # page.window.width = 600
    # page.window.height = 400

    # page.window.max_width = 600
    # page.window.max_height = 400

    # page.window.min_width = 400
    # page.window.min_height = 200


    def TopArrowButton():
        print("hide")

    audio = fta.Audio(
        autoplay=False,
        volume=1,
        balance=0,
        release_mode=fta.ReleaseMode.STOP,
        on_loaded=lambda _: print("Loaded"),
        on_duration_change=on_duration_change,
        on_position_change=on_position_change,
        on_state_change=on_state_change,
        on_seek_complete=lambda _: print("Seek complete"),
    )
    page.services.append(audio)

    def on_duration_change(e): 
        nonlocal total_duration
        total_duration = e.duration

        minutes = int(total_duration // 60)
        seconds = int(total_duration % 60)
        total_time_label.value = f"{minutes}:{seconds:02d}"

        page.update()

    def on_position_change(e):
        if total_duration > 0:
            progress = (e.position / total_duration) * 100
            time_music_slider.value = progress

            minutes = int(e.position // 60)
            seconds = int(e.position % 60)
            current_time_label.value = f"{minutes}:{seconds:02d}"

            page.update()

    def on_state_change(e):
        nonlocal is_playing
        is_playing = (e.state == fta.AudioState.PLAYING)

        # page.update()


    async def load_track(track_path):
        nonlocal current_track_path
        current_track_path = track_path
        audio.src = track_path.resolve().as_uri()

        track_name = track_path.stem
        track_title_text.value = track_name

        page.update()

        await audio.load()
        await audio.play()

    async def play_track():
        await audio.play()

    async def pause_track():
        await audio.pause()

    async def next_track():
        nonlocal current_track_index
        if music_list:
            current_track_index = (current_track_index + 1) % len(music_list)
            await load_track(music_list[current_track_index])

    async def previous_track():
        nonlocal current_track_index
        if music_list:
            current_track_index = (current_track_index - 1) % len(music_list)
            await load_track(music_list[current_track_index])

    async def repeat():
        None

    async def resume():
        await audio.resume()

    async def release():
        await audio.release()

    def set_volume(value: float):
        audio.volume += value

    def set_balance(value: float):
        audio.balance += value

    async def seek_2s():
        await audio.seek(ft.Duration(seconds=2))

    async def get_duration():
        duration = await audio.get_duration()
        print("Duration:", duration)

    async def on_get_current_position():
        position = await audio.get_current_position()
        print("Current position:", position)

    # music folder and list of songs
    music_folder = Path("/home/dimekadze/Music")
    music_list = [i.name for i in music_folder.iterdir() if i.is_file() and i.suffix.lower in [".mp3", ".wav"]]
    current_track_index = 0
    current_track_path = None
    is_playing = False
    total_duration = 0


    choose_music_title = ft.Text(
        "Choose Track",
        color="#ffffff",
        size=30,
        text_align=ft.TextAlign.CENTER
    )

    time_music_slider = ft.Slider(
        min=0, 
        max=100,
        width=450,
        active_color="#FFFFFF",
        inactive_color="#696969",
    )

    current_time_label = ft.Text("0:00", color="#FFFFFF", size=12)
    total_time_label = ft.Text("0:00", color="#FFFFFF", size=12)




    page.add(
        ft.Container(
            content=ft.ListView(
                controls=[ft.Text(f"{i + 1}. {e}") for i, e in enumerate(music_list)],)    
        ),




        ft.Container(
            margin=ft.Margin.symmetric(vertical=10, horizontal=10),
            padding=ft.Padding.symmetric(vertical=10, horizontal=10),
            border_radius=40,
            width=650,
            alignment=ft.Alignment.CENTER_LEFT,
            bgcolor="#696969",
            content=ft.IconButton(
                bgcolor="#FFFFFF",
                icon=ft.Icons.ARROW_DROP_DOWN_CIRCLE,
                icon_color="#000000",
                icon_size=40,
                on_click=TopArrowButton,
                disabled=False,
            )
        ),
        ft.Container( 
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30,
                controls=[
                    ft.Text(
                        "The Neighborhood - Sweater Weather",
                        color="#FFFFFF",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        font_family="Tahoma",
                        text_align=ft.TextAlign.CENTER
                    ),

                    ft.Container(
                        border=ft.Border.all(5, "#FFFFFF"),
                        border_radius=15,
                        padding=ft.Padding.symmetric(vertical=20, horizontal=20),
                        content=ft.Image(
                            src="images/neighborhood.jpg",
                            # width=300,
                            height=350
                        )
                    ),

                    ft.Slider(
                        min=0, 
                        max=100,
                        width=450,
                        active_color="#FFFFFF",
                        inactive_color="#696969",
                    ),

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
                                    on_click=previous_track,
                                    disabled=False
                                )
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    bgcolor="#FFFFFF",
                                    icon=ft.Icons.PLAY_ARROW,
                                    icon_color="#000000",
                                    icon_size=40,
                                    on_click=play_track,
                                    # style=ft.ButtonStyle(
                                    #     color={
                                    #         ft.ControlState.SELECTED: ft.Colors.GREEN,
                                    #         ft.ControlState.DEFAULT: ft.Colors.RED,
                                    #     }
                                    # ),
                                )
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    bgcolor="#FFFFFF",
                                    icon=ft.Icons.SKIP_NEXT,
                                    icon_color="#000000",
                                    icon_size=40,
                                    on_click=next_track,
                                    disabled=False
                                )
                            )
                        ]
                    )
                ]
            )
        )
    )

if __name__ == "__main__":
    ft.run(main)