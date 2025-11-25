import flet as ft
import difflib


FONT_SIZE=12
CONTAINER_HEIGHT=FONT_SIZE+32

def main(page: ft.Page):
    page.title = "Diff Checker"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1000
    page.window_height = 700

    input1 = ft.TextField(label="Text 1", multiline=True, expand=True, min_lines=20,border_color=ft.Colors.LIGHT_BLUE_ACCENT_100)
    input2 = ft.TextField(label="Text 2", multiline=True, expand=True, min_lines=20,border_color=ft.Colors.LIGHT_BLUE_ACCENT_100)

    input_panel = ft.Row([input1, input2], expand=True)
    diff_panel = ft.Row([], expand=True)
    container = ft.Column(controls=[], expand=True)

    def show_input():
        container.controls.clear()
        container.controls.append(input_panel)
        container.controls.append(
                ft.Row(
                    controls=[
                    ft.ElevatedButton("Compare", on_click=compare_diff, scale=1.3)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    height=80
                    )
                )
        page.update()

    def show_diff():
        container.controls.clear()
        container.controls.append(ft.ElevatedButton("Back", on_click=lambda e: show_input()))
        container.controls.append(diff_panel)
        page.update()

    def compare_diff(e):
        diff_panel.controls.clear()
        diff_area_left = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        diff_area_right = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

        text1_lines = input1.value.splitlines()
        text2_lines = input2.value.splitlines()

        diff = list(difflib.ndiff(text1_lines, text2_lines))

        line_num_left = 1
        line_num_right = 1

        def make_line(text, num, bgcolor):
            return ft.Container(
                height=CONTAINER_HEIGHT,
                bgcolor=bgcolor,
                padding=0,
                content=ft.Row([
                    ft.Text(f"{num:>3}", width=30, color=ft.Colors.GREY,style=ft.TextStyle(size=FONT_SIZE, height=1.2)),
                    ft.Text(text, selectable=True, no_wrap=True, style=ft.TextStyle(size=FONT_SIZE, height=1.2)),
                ])
            )

        def make_empty_line():
            return ft.Container(height=CONTAINER_HEIGHT)

        for line in diff:
            if line.startswith("-"):
                diff_area_left.controls.append(make_line(line, line_num_left, "#D20103"))
                #diff_area_right.controls.append(make_empty_line())
                line_num_left += 1
            elif line.startswith("+"):
                diff_area_right.controls.append(make_line(line, line_num_right, "#52A730"))
                #diff_area_left.controls.append(make_empty_line())
                line_num_right += 1
            elif line.startswith(" "):
                diff_area_left.controls.append(make_line(line, line_num_left, None))
                diff_area_right.controls.append(make_line(line, line_num_right, None))
                line_num_left += 1
                line_num_right += 1

        diff_panel.controls.append(ft.Column([
            ft.Text("Removals", color=ft.Colors.RED),
            diff_area_left
        ], expand=1))

        diff_panel.controls.append(ft.Column([
            ft.Text("Additions", color=ft.Colors.GREEN_ACCENT_400),
            diff_area_right
        ], expand=1))

        show_diff()

    show_input()
    page.add(container)


ft.app(target=main)
