import pickle
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb


class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        def selectItem(arg):
            global stroka
            curItem = table.focus()
            stroka = table.item(curItem)['values']
            print('выбрана строка', stroka)

        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)


        for row in rows:
            table.insert('', tk.END, values=tuple(row))



        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        table.bind('<<TreeviewSelect>>', selectItem)


class Car:
    def __init__(self, nomer=None, marka=None, tip=None, sostoyanie=None, cvet=None):
        self.marka = marka
        self.tip = tip
        self.nomer = nomer
        self.sostoyanie = sostoyanie
        self.cvet = cvet

    def get_data(self):
        return self.marka, self.tip, self.nomer, self.sostoyanie, self.cvet

    def get_data_bez_nomera(self):
        return self.marka, self.tip, self.sostoyanie, self.cvet


def reload_table():
    global stroka
    global table
    table.destroy()
    stroka = ['']
    table = Table(main_win, headings=('НОМЕР', 'МАРКА', 'ТИП', 'СОСТОЯНИЕ', 'ЦВЕТ'), rows=((key, value[0], value[1], \
                                                                                            value[2], value[3]) for
                                                                                           key, value in baza.items()))
    table.grid(row=1, column=0, columnspan=3, sticky='ns', padx=20, pady=20)


def new_win():
    def saving():
        if entry1.get() == entry2.get() == entry3.get() == entry4.get() == entry5.get() == '':
            mb.showerror(
                "Ошибка",
                "Не были введены значения")
        else:
            car = Car(entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get())
            if car.nomer not in baza:  # проверка на наличие уже такого номера в базе и занесение в словарь
                baza[car.nomer] = car.get_data_bez_nomera()[0], car.get_data_bez_nomera()[1], car.get_data_bez_nomera()[2], \
                                  car.get_data_bez_nomera()[3]


            else:
                mb.showerror(
                    "Ошибка",
                    "Машина с таким номером уже есть в базе")
        new_win.destroy()
        reload_table()
    new_win = tk.Tk()
    new_win.geometry('200x170')
    new_win.title('')
    new_win.resizable(False, False)


    label0 = tk.Label(new_win, text='Добавление элемента')
    label1 = tk.Label(new_win, text='номер:')
    label2 = tk.Label(new_win, text='марка:')
    label3 = tk.Label(new_win, text='тип:')
    label4 = tk.Label(new_win, text='состояние:')
    label5 = tk.Label(new_win, text='цвет:')

    btn1 = tk.Button(new_win, text='Сохранить', command=saving)

    entry1 = tk.Entry(new_win)
    entry2 = tk.Entry(new_win)
    entry3 = tk.Entry(new_win)
    entry4 = tk.Entry(new_win)
    entry5 = tk.Entry(new_win)




    label0.grid(row=0, column=0, columnspan=2)
    label1.grid(row=1, column=0)
    label2.grid(row=2, column=0)
    label3.grid(row=3, column=0)
    label4.grid(row=4, column=0)
    label5.grid(row=5, column=0)
    entry1.grid(row=1, column=1)
    entry2.grid(row=2, column=1)
    entry3.grid(row=3, column=1)
    entry4.grid(row=4, column=1)
    entry5.grid(row=5, column=1)
    btn1.grid(row=6, column=0, columnspan=2)


    new_win.mainloop()


def edit_search_win():
    def edit_auto():
        poisk = search.get()
        def savingedit():
            if entry2.get() == entry3.get() == entry4.get() == entry5.get() == '':
                mb.showerror(
                    "Ошибка",
                    "Не были введены значения")
            else:
                car = Car(poisk, entry2.get(), entry3.get(), entry4.get(), entry5.get())
                if car.nomer in baza:  # проверка на наличие уже такого номера в базе и занесение в словарь
                    baza[car.nomer] = car.get_data_bez_nomera()[0], car.get_data_bez_nomera()[1], \
                                      car.get_data_bez_nomera()[2], \
                                      car.get_data_bez_nomera()[3]
                edit_autowin.destroy()
                reload_table()
        def delete_car():
            answer = mb.askokcancel('Удаление', 'Вы действительно хотите удалить информацию о машине?')
            if answer:
                baza.pop(poisk)
            edit_autowin.destroy()
            reload_table()

        if search.get() == '':
            mb.showerror(
                "Ошибка",
                "Не были введены значения")

        elif search.get() in baza:
            marka, tip, sostoyanie, cvet = baza[search.get()]
            edit_autowin = tk.Tk()
            edit_autowin.title('')

            label0 = tk.Label(edit_autowin, text='Редактирование элемента')
            label1 = tk.Label(edit_autowin, text='номер:')
            label2 = tk.Label(edit_autowin, text='марка:')
            label3 = tk.Label(edit_autowin, text='тип:')
            label4 = tk.Label(edit_autowin, text='состояние:')
            label5 = tk.Label(edit_autowin, text='цвет:')
            label6 = tk.Label(edit_autowin, text=search.get())

            edit_search_win.destroy() #закрытие окна поиска

            btn1 = tk.Button(edit_autowin, text='Сохранить', command=savingedit)
            btn2 = tk.Button(edit_autowin, text='Удалить', command=delete_car)

            entry2 = tk.Entry(edit_autowin)
            entry3 = tk.Entry(edit_autowin)
            entry4 = tk.Entry(edit_autowin)
            entry5 = tk.Entry(edit_autowin)

            label0.grid(row=0, column=0, columnspan=2)
            label1.grid(row=1, column=0)
            label2.grid(row=2, column=0)
            label3.grid(row=3, column=0)
            label4.grid(row=4, column=0)
            label5.grid(row=5, column=0)
            label6.grid(row=1, column=1)
            entry2.grid(row=2, column=1)
            entry3.grid(row=3, column=1)
            entry4.grid(row=4, column=1)
            entry5.grid(row=5, column=1)

            entry2.insert(0, marka)
            entry3.insert(0, tip)
            entry4.insert(0, sostoyanie)
            entry5.insert(0, cvet)

            btn1.grid(row=6, column=0, padx=20)
            btn2.grid(row=6, column=1)


            edit_autowin.grid_rowconfigure(6,minsize=50)

            edit_autowin.mainloop()
        else:
            mb.showerror(
                "Ошибка",
                "В каталоге нет машины с таким номером")



    edit_search_win = tk.Tk()
    edit_search_win.geometry('200x70')
    edit_search_win.title('')
    edit_search_win.resizable(False, False)

    btn = tk.Button(edit_search_win, text='найти', command=edit_auto)
    search = tk.Entry(edit_search_win)
    label1 = tk.Label(edit_search_win, text='введите номер авто:')

    label1.pack()
    search.pack()
    btn.pack()

    edit_search_win.mainloop()


def edit_win_str():

    def savingedit():
        if entry2.get() == entry3.get() == entry4.get() == entry5.get() == '':
            mb.showerror(
                "Ошибка",
                "Не были введены значения")
        else:
            car = Car(str(stroka[0]), entry2.get(), entry3.get(), entry4.get(), entry5.get())
            if car.nomer in baza:  # проверка на наличие уже такого номера в базе и занесение в словарь
                baza[car.nomer] = car.get_data_bez_nomera()[0], car.get_data_bez_nomera()[1], \
                                  car.get_data_bez_nomera()[2], \
                                  car.get_data_bez_nomera()[3]

        edit_autowin.destroy()
        reload_table()

    def delete_car():
        answer = mb.askokcancel('Удаление', 'Вы действительно хотите удалить информацию о машине?')
        if answer:
            baza.pop(str(stroka[0]))
        edit_autowin.destroy()
        reload_table()

    # редактирование при выделении строки
    if stroka == ['']:
        mb.showerror(
            "Ошибка",
            "Не выделена строка")

    elif str(stroka[0]) in baza:
        marka, tip, sostoyanie, cvet = baza[str(stroka[0])]
        edit_autowin = tk.Tk()
        edit_autowin.title('')

        label0 = tk.Label(edit_autowin, text='Редактирование элемента')
        label1 = tk.Label(edit_autowin, text='номер:')
        label2 = tk.Label(edit_autowin, text='марка:')
        label3 = tk.Label(edit_autowin, text='тип:')
        label4 = tk.Label(edit_autowin, text='состояние:')
        label5 = tk.Label(edit_autowin, text='цвет:')
        label6 = tk.Label(edit_autowin, text=stroka[0])

        btn1 = tk.Button(edit_autowin, text='Сохранить', command=savingedit)
        btn2 = tk.Button(edit_autowin, text='Удалить', command=delete_car)

        entry2 = tk.Entry(edit_autowin)
        entry3 = tk.Entry(edit_autowin)
        entry4 = tk.Entry(edit_autowin)
        entry5 = tk.Entry(edit_autowin)

        label0.grid(row=0, column=0, columnspan=2)
        label1.grid(row=1, column=0)
        label2.grid(row=2, column=0)
        label3.grid(row=3, column=0)
        label4.grid(row=4, column=0)
        label5.grid(row=5, column=0)
        label6.grid(row=1, column=1)
        entry2.grid(row=2, column=1)
        entry3.grid(row=3, column=1)
        entry4.grid(row=4, column=1)
        entry5.grid(row=5, column=1)

        entry2.insert(0, marka)
        entry3.insert(0, tip)
        entry4.insert(0, sostoyanie)
        entry5.insert(0, cvet)

        btn1.grid(row=6, column=0, padx=20)
        btn2.grid(row=6, column=1)

        edit_autowin.grid_rowconfigure(6, minsize=50)

        edit_autowin.mainloop()


stroka = [''] #массив который обновляется время каждого тыка на строку

# чтение из файла
with open('baza.pickle', 'rb') as f:
    baza = pickle.load(f)

main_win = tk.Tk()
main_win.iconbitmap('auto.ico')
main_win.title('каталог автомобилей')


main_win.resizable(False, False)
table = Table(main_win, headings=('НОМЕР', 'МАРКА', 'ТИП', 'СОСТОЯНИЕ', 'ЦВЕТ'), rows=((key, value[0], value[1], \
                                                                                        value[2], value[3]) for
                                                                                       key, value in baza.items()))

btn1 = tk.Button(main_win, text='Добавить', command=new_win)
btn2 = tk.Button(main_win, text='Редачить строку', command=edit_win_str)
btn3 = tk.Button(main_win, text='Редачить по номеру', command=edit_search_win)



btn1.grid(row=0, column=0)
btn2.grid(row=0, column=1)
btn3.grid(row=0, column=2)


table.grid(row=1, column=0, columnspan=3, sticky='ns', padx=20, pady=20)

main_win.grid_rowconfigure(0, minsize=80)
main_win.grid_rowconfigure(1, minsize=300)


main_win.mainloop()

# сохранение в файл
with open('baza.pickle', 'wb') as f:
    pickle.dump(baza, f)

print('выбрана строка:', stroka)







