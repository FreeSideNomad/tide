#!/usr/bin/env python3

import flet as ft

def main(page: ft.Page):
    page.title = "Minimal Test"
    page.add(ft.Text("Hello World - Minimal Test"))
    print("Minimal app initialized successfully")

if __name__ == "__main__":
    print("Starting minimal Flet app...")
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)