import flet as ft
from app import App

def main(page: ft.Page):
    app = App(page)
    app.app_create()

if __name__ == "__main__":
    ft.run(main)