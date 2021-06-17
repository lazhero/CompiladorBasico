import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import font
import subprocess
import os
import pathlib

global open_file_name, selected
open_file_name, selected = False, False

class ScrollText(tk.Frame):
    def __init__(self, master, my_menu,*args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(self, bg='#2b2b2b', foreground="#d1dce8", 
                            insertbackground='white',
                            selectbackground="blue", width=120, height=30)

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines = TextLineNumbers(self, width=40, bg='#313335')
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.code_output = Text(height=10)
        file_menu = Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=lambda: self.new_file(False))
        file_menu.add_command(label="Open", command=lambda: self.open_file(False))
        file_menu.add_command(label="Save", command=lambda: self.save_file(False))
        file_menu.add_command(label="Save As", command=lambda: self.save_as_file(False))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        run_menu = Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Compile", command=self.compile)
        run_menu.add_command(label="Run and compile", command=self.run)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()

    def new_file(self,e):
        self.text.delete("1.0", END)
        root.title("New File - Wage IDE")
        global open_file_name
        open_file_name = False
    def root_path(self):
        return os.path.abspath(os.sep)

    def open_file(self,e):
        text_file = filedialog.askopenfilename(initialdir=self.root_path(), title="Open File", filetypes=(("Wage Files", "*.wage"),("Text Files", "*.txt"), ("Python Files", "*.py"),  ("All Files", "*.*")))
        if text_file:
            global open_file_name
            open_file_name = text_file
            self.text.delete("1.0", END)
            name = text_file
            root.title(f'{name} - Wage IDE')
            text_file = open(text_file, 'r')
            text = text_file.read()
            self.text.insert(END, text)
            text_file.close()
            
    def save_as_file(self,e):
        text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir=self.root_path(), title="Save File", filetypes=(("Wage Files", "*.wage"),("Text Files", "*.txt"), ("Python Files", "*.py"),  ("All Files", "*.*")))
        name = text_file
        if text_file:
            text_file = open(text_file, 'w')
            text_file.write(self.text.get(1.0, END))
            text_file.close()
            root.title(f'{name} - Wage IDE')
    def save_file(self,e):
        global open_file_name
        if open_file_name:
            text_file = open(open_file_name, 'w')
            text_file.write(self.text.get(1.0, END))
            text_file.close()
            root.title(f'{open_file_name} - Wage IDE')
        else:
            self.save_as_file(e)

    def run(self):
        global open_file_name
        if open_file_name:
            compiler_route=get_compiler_route()
            
            command = command = ["python",compiler_route,"compile_and_run",open_file_name]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            self.code_output.delete(1.0,END)
            self.code_output.pack()
            self.code_output.insert('1.0', output)
            self.code_output.insert('1.0', error)
            print("El output")
            print(output)
            print("El error")
            print(error)
            
        else:
            self.open_file(FALSE)
    def compile(self):
        global open_file_name
        if open_file_name:
            compiler_route=get_compiler_route()
            
            command = command = ["python",compiler_route,"compile",open_file_name]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            self.code_output.delete(1.0,END)
            self.code_output.pack()
            self.code_output.insert('1.0', output)
            self.code_output.insert('1.0', error)
            print("El output")
            print(output)
            print("El error")
            print(error)
            
        else:
            self.open_file(FALSE)


'''THIS CODE IS CREDIT OF Bryan Oakley (With minor visual modifications on my side): 
https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget'''


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="#606366")
            i = self.textwidget.index("%s+1line" % i)


'''END OF Bryan Oakley's CODE'''
def get_compiler_route():
    init_route=pathlib.Path(__file__).parent.parent
    init_route=init_route /'SoftWare'/ 'LexicalAnalizer'/'compile.py'
    return init_route.absolute()
if __name__ == '__main__':
    root = tk.Tk()
    my_menu = Menu(root)
    scroll = ScrollText(root,my_menu)

    root.config(menu=my_menu)

    scroll.insert(tk.END, "" + 0*'\n')
    scroll.pack()
    scroll.text.focus()
    root.after(200, scroll.redraw())
    root.mainloop()
