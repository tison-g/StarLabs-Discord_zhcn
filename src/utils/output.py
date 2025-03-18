import os
from rich.console import Console
from rich.text import Text
from tabulate import tabulate
from rich.table import Table
from rich import box
from typing import List
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, Window, HSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

def show_logo():
    """显示STARLABS的艺术标志"""
    # 清屏
    os.system("cls" if os.name == "nt" else "clear")

    console = Console()

    # 创建带有样式的星空背景标志
    logo_text = """
✦ ˚ . ⋆   ˚ ✦  ˚  ✦  . ⋆ ˚   ✦  . ⋆ ˚   ✦ ˚ . ⋆   ˚ ✦  ˚  ✦  . ⋆   ˚ ✦  ˚  ✦  . ⋆ ✦ ˚ 
. ⋆ ˚ ✧  . ⋆ ˚  ✦ ˚ . ⋆  ˚ ✦ . ⋆ ˚  ✦ ˚ . ⋆  ˚ ✦ . ⋆ ˚  ✦ ˚ . ⋆  ˚ ✦ . ⋆  ˚ ✦ .✦ ˚ . 
·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ⋆｡⋆｡. ★ ·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ·˚ ★ ·˚
✧ ⋆｡˚✦ ⋆｡  ███████╗████████╗ █████╗ ██████╗ ██╗      █████╗ ██████╗ ███████╗[...]
★ ·˚ ⋆｡˚   ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔══██╗██╔══██╗██╔══[...]
⋆｡✧ ⋆ ★    ███████╗   ██║   ███████║██████╔╝██║     ███████║██████╔╝███████╗  [...]
˚· ★ ⋆｡    ╚════██║   ██║   ██╔══██║██╔══██╗██║     ██╔══██║██╔══██╗╚════██║   [...]
✧ ⋆｡ ˚·    ███████║   ██║   ██║  ██║██║  ██║███████╗██║  ██║██████╔╝███████║   ★[...]
★ ·˚ ✧     ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝   ｡⋆ [...]
·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ⋆｡⋆｡. ★ ·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚·˚ ⋆｡⋆｡.
. ⋆ ˚ ✧  . ⋆ ˚  ✦ ˚ . ⋆  ˚ ✦ . ⋆ ˚  ✦ ˚ . ⋆  ˚ ✦ . ⋆ ˚  ✦ ˚ . ⋆  ˚ ✦ . ⋆  ˚ ✦ .. ⋆  ˚ 
✦ ˚ . ⋆   ˚ ✦  ˚  ✦  . ⋆ ˚   ✦  . ⋆ ˚   ✦ ˚ . ⋆   ˚ ✦  ˚  ✦  . ⋆   ˚ ✦  ˚  ✦  . ⋆  ✦"""

    # 创建渐变文本效果
    gradient_logo = Text(logo_text)
    gradient_logo.stylize("bold bright_cyan")

    # 输出带有边距的标志
    console.print(gradient_logo)
    print()

def show_dev_info():
    """显示开发信息和版本信息"""
    console = Console()

    # 创建美观的表格
    table = Table(
        show_header=False,
        box=box.DOUBLE,
        border_style="bright_cyan",
        pad_edge=False,
        width=49,
        highlight=True,
    )

    # 添加列
    table.add_column("Content", style="bright_cyan", justify="center")

    # 添加联系信息行
    table.add_row("✨ StarLabs Discord Bot 2.0 ✨")
    table.add_row("─" * 43)
    table.add_row("")
    table.add_row("⚡ GitHub: [link]https://github.com/moncici007[/link]")
    table.add_row(" Chat: [link]https://x.com/moncici_is_girl[/link]")
    table.add_row("")

    # 输出带有边距的表格
    print("   ", end="")
    print()
    console.print(table)
    print()

def show_menu(options: List[str]) -> str:
    """
    显示带编号的菜单并返回所选选项字符串
    """
    print("😎  选择你的选项 😎\n")

    # 显示带编号的选项
    for i, option in enumerate(options, 1):
        print(f"[{i}] {option}")

    while True:
        try:
            print("\n")
            choice = int(input("你的选择: "))
            if 1 <= choice <= len(options):
                selected_index = choice - 1
                return options[selected_index]
            else:
                print(f"     ❌ 请输入1到{len(options)}之间的数字")
        except ValueError:
            print("     ❌ 请输入有效的数字")