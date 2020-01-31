from tkinter import *

THEME = 'Light'


def preferences(root, extra: list):
    create_window(root, title='Preferences', extra=extra)


def create_window(root, extra: list, title: str = 'TkinterWindow', geometry: str = '600x420') -> None:
    """
    :param extra: Extra content to style or change
    :param root: Root variable from main window
    :param title: Title for new window
    :param geometry: Set window geometry
    :return: None
    """
    # Create a new toplevel Window
    window = Toplevel(root)
    window.title(title)
    # set geometry
    window.geometry(geometry)
    window.resizable(width=False, height=False)

    if THEME == 'Light':
        window.configure(background='white')
    elif THEME == 'Dark':
        window.configure(background='#263238')

    # Variables
    auto_save = BooleanVar()
    theme = StringVar()

    choices = {'Dark', 'Light'}
    theme.set(THEME)  # set the default option

    # CONFIG OPTIONS
    auto_save_checkbox = Checkbutton(window, text="Auto save File", variable=auto_save)
    popup_theme_menu = OptionMenu(window, theme, *choices)

    # Apply button
    apply_btn = Button(window, text='Apply',
                       command=lambda: apply_preferences(root, window, extra, theme.get(), auto_save.get()))

    # Label for Config Options
    theme_lbl = Label(window, text='Theme: ')
    auto_save_checkbox_lbl = Label(window, text='AutoSave: ')

    # Theme Grid
    theme_lbl.grid(row=0, column=0, padx=10, pady=10)
    popup_theme_menu.grid(row=0, column=1, pady=10)

    # AutoSave Grid
    auto_save_checkbox_lbl.grid(row=1, column=0, padx=10, pady=10)
    auto_save_checkbox.grid(row=1, column=1, pady=10)

    # Apply Button Grid
    row, column = window.grid_size()
    apply_btn.grid(row=row, column=column, pady=10)


def apply_preferences(root, toplevel, extra, theme: str = 'white', autosave: bool = False):
    apply_theme(root, toplevel, extra, theme)

    toplevel.destroy()


def apply_theme(root, toplevel, extra, theme='Light'):
    global THEME

    if theme == 'Light':
        # Change text color
        extra[0].configure(background='white', fg='black')

        # Change BG (ROOT, TOPLEVEL)
        toplevel.configure(background='white')
        root.configure(background='white')

        THEME = 'Light'

    elif theme == 'Dark':
        # Change text color
        extra[0].configure(background='#263238', fg='white')

        # Change BG (ROOT, TOPLEVEL)
        toplevel.configure(background='black')
        root.configure(background='black')

        THEME = 'Dark'
