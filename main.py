import os
import time
import tkinter.scrolledtext as ScrolledText
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog

import pandas as pd

import builtin.preferences

dirpath = os.path.dirname(os.path.realpath(__file__))


class database:
    def __init__(self):
        self.last = None


class Application:

    def __init__(self):

        # defines the app
        self.root = Tk()

        # set default extension file
        self.extension = 'txt'

        self.current_file = [None, False]

        # set options (title, geometry, icon)
        self.root.title('Text Editor - New Document')
        self.root.geometry('1080x720')
        self.root.iconbitmap(dirpath + '\\icon-1.ico')

        # text area to code / write
        self.text = ScrolledText.ScrolledText(self.root, width=120, height=80, pady=20, padx=10, tabs=36, font=('Arial', '10'))
        self.text.pack(expand=YES, fill=BOTH)

        # set the menus
        self.menubar = Menu(self.root)
        filemenu = Menu(self.menubar, tearoff=0)
        editmenu = Menu(self.menubar, tearoff=0)
        toolsmenu = Menu(self.menubar, tearoff=0)
        pd_menu = Menu(self.menubar, tearoff=0)
        terminal = Menu(self.menubar, tearoff=0)

        pd_menu.add_command(label='Mean of', command=self.mean_csv)
        pd_menu.add_command(label='Max value', command=self.max_csv)
        pd_menu.add_command(label='Min value', command=self.min_csv)

        runmenu = Menu(self.menubar, tearoff=False)
        runmenu.add_command(label='Run Code', command=self.run_without_saving)
        runmenu.add_command(label='Save and run', command=self.run)
        terminal.add_cascade(label='Run', menu=runmenu)

        terminal.add_command(label='Open Terminal', command=self.terminal)
        terminal.add_command(label='Open Python', command=self.terminal_python)
        terminal.add_separator()
        terminal.add_command(label='Shutdown', command=self.shutdown)
        filemenu.add_command(label='New File', command=self.new_file)
        filemenu.add_command(label='Open File', command=self.open_file)

        savemenu = Menu(self.menubar, tearoff=False)
        savemenu.add_command(label='Save', command=self.save)
        savemenu.add_command(label='Save as', command=self.save_file)
        filemenu.add_cascade(label='Save', menu=savemenu)
        filemenu.add_command(label='Preferences',
                             command=lambda: builtin.preferences.preferences(self.root, [self.text]))

        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)

        editmenu.add_command(label='Cut', command=self.cut)
        editmenu.add_command(label='Copy', command=self.copy)
        editmenu.add_command(label='Paste', command=self.paste)
        editmenu.add_separator()
        editmenu.add_command(label='Clear', command=self.clear)

        toolsmenu.add_command(label='Count Words', command=self.count_words)
        toolsmenu.add_command(label='Find Words', command=self.find)

        self.menubar.add_cascade(label='File', menu=filemenu)
        self.menubar.add_cascade(label='Edit', menu=editmenu)
        self.menubar.add_cascade(label='Options', menu=toolsmenu)
        self.menubar.add_cascade(label='Pandas Menu', menu=pd_menu)
        self.menubar.add_cascade(label='Terminal', menu=terminal)

        self.root.config(menu=self.menubar)
        self.root.mainloop()

    terminal = lambda self: os.system('start cmd')
    terminal_python = lambda self: os.system('start Python')
    shutdown = lambda self: None if not (
        messagebox.askyesno("Are you sure?", "Unsaved work will be lost. Continue?")) else os.system('shutdown -p')

    def run_without_saving(self):
        """
        Runs code without saving the file
        """

        location_path = r'process\run_process.py'

        if len(self.text.get('1.0', END)) > 1:

            f = open(location_path, 'w').close()

            f = open(r"process\model.txt", 'r')
            content = f.readlines()
            f.close()
            content.insert(8, ''.join(map(lambda x: '\n' + ' ' * 8 + x, self.text.get('1.0', END).splitlines())))
            content = ''.join(content)

            f = open(location_path, 'w')
            f.write(content)
            f.close()
            os.system(f'start python {location_path}')

        else:
            label = messagebox.showinfo('Warning', 'Please write a longer code.')

    def run(self):
        """
        Runs code by saving it before
        """
        # check if there's a document opened and check if the extension of it's py
        if self.current_file[1] and self.extension.lower() == 'py':
            f = open(self.current_file[0], 'r')

            # check if the text of the current file is equal to the text in Text Editor
            if f.read() == self.text.get('1.0', END):
                f.close()

                # if total length of code is as more as 0, it will be executed
                if len(self.text.get('1.0', END)) > 0:
                    os.system(f'start python {self.current_file[0]}')

            else:
                f = open(self.current_file[0], 'w')
                f.write(self.text.get('1.0', END))
                f.close()

        # if no document was saved, the text will be saved
        elif not self.current_file[1]:

            # If (save file) is True, then proceed to save the entire text into a Python file
            if messagebox.askyesno("Save file?", "You need to save your file to run it, save file?"):
                self.current_file[0] = self.root.filename = filedialog.asksaveasfilename(initialdir=dirpath,
                                                                                         title="Save file", filetypes=(
                        ("Python files", "*.py"), ("text files", "*.txt")), defaultextension=".py")
                self.extension = self.current_file[0].split('/')[-1].split('.')[-1].lower()

                try:
                    f = open(self.current_file[0], 'w')
                    f.write(self.text.get('1.0', END) + "\ninput()")
                    new_title = self.current_file[0].split('/').pop()
                    self.root.title('Text Editor - ' + new_title)
                    self.current_file[1] = True

                except:
                    print('Something went wrong saving your file!')

                finally:
                    f.close()
                    if self.current_file[1] and self.extension.lower() == 'py':
                        if len(self.text.get('1.0', END)) > 0:
                            os.system(f'start python {self.current_file[0]}')

    def new_file(self):
        """
        Creates a new file
        """
        if messagebox.askyesno("Message", "Unsaved work will be lost. Continue?"):
            self.text.delete('1.0', END)
            self.root.title('Text Editor - New Document')

    def save(self):
        if self.current_file[1]:
            # check if there's a document opened
            f = open(self.current_file[0], 'r')

            # check if the text of the current file is equal to the text in Text Editor
            if f.read() == self.text.get('1.0', END):
                f.close()

            else:
                f = open(self.current_file[0], 'w')
                f.write(self.text.get('1.0', END))
                f.close()

                new_title = self.current_file[0].split('/')[-1]

                self.root.title('Saving...')
                time.sleep(1.5)
                self.root.title('Text Editor - ' + new_title)

    def save_file(self):
        """
        Saves file
        """
        self.savefile = self.root.filename = filedialog.asksaveasfilename(initialdir=dirpath, title="Save file",
                                                                          filetypes=(
                                                                              ("text files", "*.txt"),
                                                                              ("commas separated values", "*.csv"),
                                                                              ("all files", "*.*")),
                                                                          defaultextension=".txt")

        try:
            f = open(self.root.filename, 'a+')
            check = f.write(str(self.text.get('1.0', END)))

            if check == len(str(self.text.get('1.0', END))):
                new_title = self.savefile.split('/').pop()
                self.current_file = [self.savefile, True]
                self.extension = self.savefile.split('/')[-1].split('.')[-1]
                self.root.title('Saving...')
                time.sleep(1.5)
                self.root.title('Text Editor - ' + new_title)

        except:
            print('Something went wrong saving your file!')

        finally:
            f.close()

    def open_file(self):
        """
        Open a file
        """
        try:
            self.current_file[0] = filedialog.askopenfilename(
                filetypes=(("text files", "*.txt"), ("comma separated values", "*.csv"), ("python files", "*.py"),
                           ("all files", "*.*")))
            self.extension = self.current_file[0].split('/')[-1].split('.')[1]

            # if file type is csv
            if self.extension == 'csv':
                try:
                    self.text_vls = pd.read_csv(self.current_file[0])
                    exc = False

                # except gives some error due opening csv file
                except:
                    print('csv DataDrame has no columns')
                    self.text_vls = ''
                    exc = False
                    self.current_file[1] = True

            else:
                f = open(self.current_file[0], 'r')
                self.text_vls = f.read()
                exc = True

            self.text.delete('1.0', END)
            self.text.insert(END, self.text_vls)
            new_title = self.current_file[0].split('/').pop()
            self.current_file[1] = True
            self.root.title('Text Editor - ' + new_title)

            if exc:
                f.close()

        except:
            # print('Something went wrong opening your file!')
            raise

    def mean_csv(self):
        """
        Get mean of a csv file, gets values of DataFrame using Pandas
        """
        if self.extension == 'csv':
            try:
                x = simpledialog.askstring(
                    'Enter Title', 'Please provide a title to get an average of values')
                if len(x) <= 0:
                    label = messagebox.showinfo(
                        "Title error", "You must provide at least one caracter!")
                else:
                    result = self.text_vls[x].mean()
                    label = messagebox.showinfo(
                        "Results", f"The average mean of {x} is {result}")
            except (AttributeError, KeyError):
                label = messagebox.showinfo(
                    "Error while founding!", f"Please provide a correct title, '{x}' doesn't exists.")
                raise
        else:
            label = messagebox.showinfo(
                "Open a CSV file!", "Please open the correct file (extension: csv).")

    def max_csv(self):
        """
        Get max value of DataFrame values
        """
        if self.extension == 'csv':
            try:
                x = simpledialog.askstring(
                    'Enter Title', 'Please provide a title to get the max value.')
                if len(x) <= 0:
                    label = messagebox.showinfo(
                        "Title error", "You must provide at least one caracter!")
                else:
                    result = self.text_vls[x].max()
                    label = messagebox.showinfo(
                        "Results", f"The max value of {x} is {result}")
            except (AttributeError, KeyError):
                label = messagebox.showinfo(
                    "Error while founding!", f"Please provide a correct title, '{x}' doesn't exists.")
                raise

        else:
            label = messagebox.showinfo(
                "Open a CSV file!", "Please open the correct file (extension: csv).")

    def min_csv(self):
        """
        Get max value of DataFrame values
        """
        if self.extension == 'csv':
            try:
                x = simpledialog.askstring(
                    'Enter Title', 'Please provide a title to get the min value.')
                if len(x) <= 0:
                    label = messagebox.showinfo(
                        "Title error", "You must provide at least one caracter!")
                else:
                    result = self.text_vls[x].min()
                    label = messagebox.showinfo(
                        "Results", f"The max value of {x} is {result}")
            except (AttributeError, KeyError):
                label = messagebox.showinfo(
                    "Error while founding!", f"Please provide a correct title, '{x}' doesn't exists.")
                raise
        else:
            label = messagebox.showinfo(
                "Open a CSV file!", "Please open the correct file (extension: csv).")

    def copy(self):
        """
        Copy selected text and add it to clipboard
        """
        try:
            self.text.clipboard_clear()
            self.text.clipboard_append(self.text.selection_get())

        except:
            pass

    def cut(self):
        """
        Cut selected text and add it to clipboard
        """
        try:
            self.copy()
            self.text.delete(SEL_FIRST, SEL_LAST)

        except:
            pass

    def paste(self):
        """
        Paste clipboard text to textarea
        """
        try:
            self.text.insert(INSERT, self.text.clipboard_get())
            result = self.root.selection_get(selection="CLIPBOARD")
            self.text.insert(self.text.index, result)

        except:
            pass

    def clear(self):
        """
        Clear textarea
        """
        self.text.delete('1.0', END)

    def count_words(self):
        """
        Count how many words have the textarea
        """
        number_of_words = len(self.text.get('1.0', END).split())
        messagebox.showinfo(
            'Word Count', 'Number of words:  ' + str(number_of_words))

    def find(self):
        """
        Find string in textarea
        """
        find = simpledialog.askstring("Find", "Enter Text:")
        textData = self.text.get('1.0', END)

        if len(find) <= 0:
            label = messagebox.showinfo(
                "Find Error", "You must provide at least one caracter!")

        else:
            if find.lower() in textData.lower():
                messagebox.showinfo('Search Successful', f'We could found it:{find}')
            else:
                label = messagebox.showinfo("Find Error", "We can found it!")


app = Application()
