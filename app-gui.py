import position
from Detector import main_app
from Detect import main_appp
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, PhotoImage


names = set()

class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("JAKI Face Control")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive, PageSix, PageSeven):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Выход", "Вы уверены?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            render = PhotoImage(file='facecontrol.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=0, rowspan=4, sticky="nsew")
            label = tk.Label(self, text=" Добро пожаловать! \nJAKI Face Control", font=('Times New Roman','25'), fg='White', bg='#00467b')
            label.place(x=100, y=100)
            button1 = tk.Button(self, text="Добавить пользователя", font=('Times New Roman','14'), fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text="Проверить пользователя", font=('Times New Roman','14'), fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageTwo"))
            button3 = tk.Button(self, text="Запустить", fg="#ffffff", font=('Times New Roman','14'), bg="green",  activebackground='#ff0000', command=lambda: self.controller.show_frame("PageThree"))
            button4 = tk.Button(self, text="Выйти", fg="#ffffff", font=('Times New Roman','14'), bg="red", command=self.on_closing)
            button1.place(x=120, y=220, width=250, height=35)
            button2.place(x=120, y=270, width=250, height=35)
            button3.place(x=120, y=340, width=250, height=35)
            button4.place(x=120, y=390, width=250, height=35)


        def on_closing(self):
            if messagebox.askokcancel("Выход", "Вы уверены?"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        render = PhotoImage(file='facecontrol.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=0, rowspan=4, sticky="nsew")
        tk.Label(self, text="Введите имя", fg="#263942", font=('Times New Roman','14')).place(x=80, y=170,width=150, height=35)
        self.user_name = tk.Entry(self, borderwidth=7, bg="lightgrey", font=('Times New Roman','14'))
        self.user_name.place(x=240, y=170)
        self.buttoncanc = tk.Button(self, text="Назад", font=('Times New Roman','14'), bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Далее", font=('Times New Roman','14'), fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttoncanc.place(x=150, y=290, width=150, height=35)
        self.buttonext.place(x=150, y=240, width=150, height=35)
    def start_training(self):
        global names
        if len(self.user_name.get()) == 0:
            messagebox.showerror("ОШИБКА", "Имя не может быть пустым!")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("ОШИБКА", "Пользователь уже существует!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageFour")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        render = PhotoImage(file='facecontrol.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=0, rowspan=4, sticky="nsew")
        tk.Label(self, text="Выберите пользователя:", fg="#263942", font=('Times New Roman','14')).place(x=80, y=170,width=250, height=35)
        self.buttoncanc = tk.Button(self, text="Назад", font=('Times New Roman','14'), command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey", borderwidth=6, font=('Times New Roman','14'))
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Далее", font=('Times New Roman','14'), command=self.nextfoo, fg="#ffffff", bg="#263942")
        self.dropdown.place(x=350, y=170)
        self.buttoncanc.place(x=150, y=290, width=150, height=35)
        self.buttonext.place(x=150, y=240, width=150, height=35)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ОШИБКА", "Имя не может быть 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageSix")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        render = PhotoImage(file='facecontrol.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=0, rowspan=4, sticky="nsew")
        tk.Label(self, text="Выберите пользователя:", fg="#263942", font=('Times New Roman','14')).place(x=80, y=170,width=250, height=35)
        self.buttoncanc = tk.Button(self, text="Назад", font=('Times New Roman','14'), command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey", borderwidth=6, font=('Times New Roman','14'))
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Далее", font=('Times New Roman','14'), command=self.nextfoo, fg="#ffffff", bg="#263942")
        self.dropdown.place(x=350, y=170)
        self.buttoncanc.place(x=150, y=290, width=150, height=35)
        self.buttonext.place(x=150, y=240, width=150, height=35)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ОШИБКА", "Имя не может быть 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFive")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        render = PhotoImage(file='facecontrol.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.numimglabel = tk.Label(self, text="Количество изображений = 0", font=('Times New Roman','18'), fg="#263942")
        self.numimglabel.place(x=65, y=180, width=410, height=35)
        self.capturebutton = tk.Button(self, text="Сделать снимки", font=('Times New Roman','14'), fg="#ffffff", bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Обучить модель", font=('Times New Roman','14'), fg="#ffffff", bg="#263942",command=self.trainmodel)
        self.capturebutton.place(x=80, y=240, width=180, height=35)
        self.trainbutton.place(x=280, y=240, width=180, height=35)
        self.buttoncanc = tk.Button(self, text="Назад", font=('Times New Roman','14'), bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("PageOne"))
        self.buttoncanc.place(x=80, y=290, width=180, height=35)
        self.buttonfirst = tk.Button(self, text="На главную странцу", font=('Times New Roman','14'), bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonfirst.place(x=280, y=290, width=180, height=35)

    def capimg(self):
        self.numimglabel.config(text=str("Снятых изображений = 0 "))
        messagebox.showinfo("ВНИМАНИЕ!", "Сейчас сделаем 100 снимков вашего лица.\nМедленно крутите голову, чтобы снять полностью ваше лицо.\nМожете делать различные мимики😃😆☺️😉😚🙁😫😣")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Количество сделанных снимков = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 100:
            messagebox.showerror("ОШИБКА", "Недостаточно данных, сделайте не менее 100 снимков!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("ОТЛИЧНО", "Модель успешно обучена!")
        self.controller.show_frame("PageSeven")


class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        render = PhotoImage(file='facecontrol.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=0, rowspan=4, sticky="nsew")
        label = tk.Label(self, text="Распознавание лица", font=('Times New Roman','18'))
        label.place(x=100, y=170,width=250, height=35)
        button1 = tk.Button(self, text="Запустить", fg="#ffffff", font=('Times New Roman','14'), bg="green",  activebackground='#ff0000', command=self.openwebcam)
        button4 = tk.Button(self, text="На главную страницу", font=('Times New Roman','14'), command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.place(x=130, y=240, width=190, height=35)
        buttoncanc = tk.Button(self, text="Назад", font=('Times New Roman', '14'),
                                    command=lambda: controller.show_frame("PageThree"), bg="#ffffff", fg="#263942")
        buttoncanc.place(x=130, y=290, width=190, height=35)
        button4.place(x=130, y=340, width=190, height=35)

    def openwebcam(self):
        position.looping_func(self.controller.active_name)
        # return True
        # main_app(self.controller.active_name)

class PageSix(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        render = PhotoImage(file='facecontrol.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=0, rowspan=4, sticky="nsew")
        label = tk.Label(self, text="Распознавание лица", font=('Times New Roman', '14'))
        label.place(x=100, y=170, width=250, height=35)
        button1 = tk.Button(self, text="Проверить", command=self.openwebcam, font=('Times New Roman', '14'),
                                fg="#ffffff", bg="#263942")
        button2 = tk.Button(self, text="На главную страницу", font=('Times New Roman', '14'),
                                command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        buttoncanc = tk.Button(self, text="Назад", font=('Times New Roman', '14'),
                                    command=lambda: controller.show_frame("PageTwo"), bg="#ffffff", fg="#263942")
        button1.place(x=130, y=240, width=190, height=35)
        button2.place(x=130, y=340, width=190, height=35)
        buttoncanc.place(x=130, y=290, width=190, height=35)

    def openwebcam(self):
        main_appp(self.controller.active_name)


class PageSeven(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        render = PhotoImage(file='facecontrol.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=0, rowspan=4, sticky="nsew")
        label = tk.Label(self, text="Распознавание лица", font=('Times New Roman','18'))
        label.place(x=100, y=170,width=250, height=35)
        button1 = tk.Button(self, text="Запустить", fg="#ffffff", font=('Times New Roman','14'), bg="green",  activebackground='#ff0000', command=self.openwebcam)
        button2 = tk.Button(self, text="Проверить", command=self.openwebcamm, font=('Times New Roman', '14'),
                                fg="#ffffff", bg="#263942")
        button3 = tk.Button(self, text="На главную страницу", font=('Times New Roman','14'), command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.place(x=130, y=240, width=190, height=35)
        button2.place(x=130, y=290, width=190, height=35)
        buttoncanc = tk.Button(self, text="Назад", font=('Times New Roman', '14'),
                                    command=lambda: controller.show_frame("PageFour"), bg="#ffffff", fg="#263942")
        buttoncanc.place(x=130, y=340, width=190, height=35)
        button3.place(x=130, y=390, width=190, height=35)

    def openwebcam(self):
        main_app(self.controller.active_name)

    def openwebcamm(self):
        main_appp(self.controller.active_name)


app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='icon.ico'))
app.mainloop()

