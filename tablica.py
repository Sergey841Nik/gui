"""
Оконное приложение создано для школьного проекта по истории.
Сравнительная таблица событий происходивших в различных государствах до нашей эры.
Можно доболять и удалять строки и столбцы.
Удалив всю внесённую информацию можно использоать для других целей
"""


from tkinter import WORD, Tk, Menu, Text
import tkinter.ttk as ttk
from tkinter.font import Font
from functools import partial

import pandas as pd




class WindTreeview(Tk):
    def __init__(self, title=None, geometry=None):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.load()
        self.menu()

    def load(self):
        self.data_pd = pd.read_csv("table_do_NE.csv", encoding="utf-8")
        self.value = [list(self.data_pd.loc[id]) for id in self.data_pd.index]
        self.columns = list(self.data_pd.columns)
        return self.value, self.columns

    def buttons(self):
        self.btn_save = ttk.Button(self, text="Сохранить", command=self.save_file)
        self.btn_save.grid(row=0, column=0)

    def adjust_newlines(self, val, width, pad=10):
        f = Font(font='TkDefaultFont')
        if not isinstance(val, str):
            return val
        else:
            words = val.split()
            lines = [[],]
            for word in words:
                line = lines[-1] + [word,]
                if f.measure(' '.join(line)) < (width - pad):
                    lines[-1].append(word)
                else:
                    lines[-1] = ' '.join(lines[-1])
                    lines.append([word,])

            if isinstance(lines[-1], list):
                lines[-1] = ' '.join(lines[-1])

            return '\n'.join(lines)

    def motion_handler(self, event):
        if event is None or self.tree.identify_region(event.x, event.y) == "separator":
            # print(tree.identify_column(event.x))

            col_widths = [self.tree.column(cid)['width'] for cid in self.tree['columns']]

            for iid in self.tree.get_children():
                new_vals = []
                for (v,w) in zip(self.tree.item(iid)['values'], col_widths):
                    new_vals.append(self.adjust_newlines(v, w))
                self.tree.item(iid, values=new_vals)

    def auto_format(self):
        col_widths = [self.tree.column(cid)['width'] for cid in self.tree['columns']]
        # print((col_widths))
        n = 0
        for iid in self.value:
            # print(iid)
            n += 1
            new_vals = []
            for v,w in zip(iid, col_widths):
                new_vals.append(self.adjust_newlines(v, w))
            if n%2 != 0:
                self.tree.insert('', 'end', values=new_vals, tag='krsivo')
                self.tree.tag_configure('krsivo', background='lightblue')
            else:
                self.tree.insert('', 'end', values=new_vals)

    def treeview(self):
        self.tree = ttk.Treeview(
            self, columns=self.columns, height=12, show="headings", selectmode="browse", padding=20
        )
        self.tree.grid(columnspan=100, row=1, sticky="nsew")
        self.stayl = ttk.Style(self)
        self.stayl.configure('Treeview', rowheight=50, font=("Helvetica", 9))
        self.stayl.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        self.stayl.map("Treeview", background=[("selected", "black")], foreground=[("selected", "white")])

        self.tree.heading(self.columns[0], text=self.columns[0], command=lambda: self.sort(0, False))
        self.tree.column(self.columns[0], anchor="n", width=130)
      
        for i in self.columns[1:]:
            self.tree.heading(i, text=i)
            self.tree.column(i, anchor="nw", width=400)

        # for k in self.value:
        #     self.tree.insert("", "end", values=k)
        self.auto_format()

        self.main_menu_Btn3 = Menu(self, tearoff=0)
        self.main_menu_Btn3.add_command(label="Удалить строку", command=self.delete_row)
        self.main_menu_Btn3.add_command(label="Добавить строку", command=self.new_row)
        self.main_menu_Btn3.add_command(
            label="Редактировать ячейку", command=self.set_value_1
        )
        self.main_menu_Btn3.add_command(label="Добавить государство", command=self.new_column)
        self.main_menu_Btn3.add_command(label="Удалить государство", command=self.delete_column)
        self.tree.bind("<Double-1>", func=self.set_value_1)
        self.tree.bind("<Button-1>", func=self.select_row)
        self.tree.bind("<Button-3>", func=self.button_3)
        self.tree.bind('<B1-Motion>', partial(self.motion_handler))
        # self.motion_handler(self.tree, None)   # Perform initial wrapping

        self.scrolbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrolbar.set)
        self.scrolbar.grid(column=101, row=1, sticky="ns")
        self.scrolbarX = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrolbar.set)
        self.scrolbarX.grid(columnspan=100, row=2, sticky="ew")

    def set_value_1(self, event=None):
        self.win = WindTreeview("Ввод текста")

        if self.column == "#1":
            self.edit = ttk.Entry(self.win)
            self.edit.insert(0, self.tree.set(self.row, self.column))
            self.edit.pack()
        else:
            self.edit = Text(self.win, wrap=WORD, width=50)
            self.edit.insert(1.0, self.tree.set(self.row, self.column))
            self.edit.pack()

        def save_edit():
            if self.column == "#1":
                self.tree.set(self.row, column=self.column, value=self.edit.get())
                self.win.destroy()
            else:
                self.tree.set(
                    self.row, column=self.column, value=self.edit.get(1.0, "end")
                )
                self.win.destroy()

        self.btn_OK = ttk.Button(
            self.win, text="OK", width=10, command=save_edit)
        self.btn_OK.pack()

    def sort(self, col, reverse):
            l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
            l.sort(reverse=reverse)
            for index,  (_, k) in enumerate(l):
                self.tree.move(k, "", index)
            self.tree.heading(col, command=lambda: self.sort(col, not reverse))

    def menu(self):
        self.main_menu = Menu(self)
        self.fail_menu = Menu(self, tearoff=0)
        self.fail_menu.add_command(label="Вся таблица и редактор", command=self.all)
        self.fail_menu.add_command(label="Сортировка по годам", command=self.sort_year)
        self.fail_menu.add_command(label="Сортировка по странам", command=self.sort_countries)

        self.main_menu.add_cascade(label="Меню", menu=self.fail_menu)
        self.config(menu=self.main_menu)

    def all(self):
        self.clear_wind()
        self.load()
        self.menu()
        self.treeview()
        self.buttons()

    def sort_year(self):
        self.clear_wind()
        self.menu()
        data_pd = pd.read_csv("table_do_NE.csv", encoding="utf-8")
        columns_year, *_ = data_pd.columns
        combo_year = [data_pd.loc[id][columns_year] for id in data_pd.index]
        year_lable_ot = ttk.Label(text="От")
        year_combobox_ot = ttk.Combobox(self, values=combo_year, width=10)
        year_lable_ot.grid(column=0, row=0)
        year_combobox_ot.grid(column=1, row=0)
        year_lable_do = ttk.Label(text="До")
        year_combobox_do = ttk.Combobox(self, values=combo_year, width=10)
        year_lable_do.grid(column=2, row=0)
        year_combobox_do.grid(column=3, row=0)
        def sort():
            if int(year_combobox_do.get()) > int(year_combobox_ot.get()):
                lbl = ttk.Label(text="Год 'от' должен быть больше года 'до'")
                lbl.grid(columnspan=100,row=1)
            else:
                self.columns = list(data_pd.columns)
                self.value = [[data_pd.loc[id][column] for column in self.columns] for id in data_pd.index 
                            if int(year_combobox_do.get())<=int(data_pd.loc[id][columns_year])<=int(year_combobox_ot.get())]
                self.treeview()
                # print(self.columns, "\n", self.value)
        btn_year = ttk.Button(self, text="Ok", command=sort)
        btn_year.grid(column=4, row=0)

    def sort_countries(self):
        self.clear_wind()
        self.menu()
        data_pd = pd.read_csv("table_do_NE.csv", encoding="utf-8")
        columns_year, *columns_countri = data_pd.columns
        combo_countri = columns_countri
        countri_combobox = ttk.Combobox(self, values=combo_countri, width=10)
        countri_combobox.grid(column=0, row=0)
        def sort():
            self.columns = [columns_year, countri_combobox.get()]
            self.value = []
            value = [[data_pd.loc[id][column] for column in self.columns] for id in data_pd.index]
            for i in value:
                if i[1] != "-" and i[1] != "-\n" and i[1] != "-\n\n":
                    self.value.append(i)
            # print(self.value)
            self.treeview()
        btn_count = ttk.Button(self, text="Ok", command=sort)
        btn_count.grid(column=1, row=0)
        
    def save_file(self):
        self.data_save = [
            self.tree.item(i, "values") for i in self.tree.get_children("")
        ]
        self.data_frame = pd.DataFrame(self.data_save, columns=self.columns)
        return self.data_frame.to_csv("table_do_NE.csv", index=False, encoding="utf-8")

    def button_3(self, event):
        self.main_menu_Btn3.post(event.x_root, event.y_root)
        self.row = self.tree.identify_row(event.y)
        self.column = self.tree.identify_column(event.x)
        # print(self.row, self.column)
        return self.row, self.column
    
    def new_column(self):
        self.win = WindTreeview("Ввод государства")
        self.edit = ttk.Entry(self.win)
        self.edit.pack()
        def save_edit():
            self.columns.append(self.edit.get())
            self.value = [list(self.tree.item(i, 'values')) for i in self.tree.get_children('')]
            for i in range(len(self.value)):
                self.value[i].append('-')
            self.treeview()
            self.tree.update()
            self.save_file()
            self.win.destroy()
        self.btn_Ok_1 = ttk.Button(self.win, text='OK', width=18, command=save_edit)
        self.btn_Ok_1.pack()

    def new_row(self):
        self.data_pd = pd.read_csv("table_do_NE.csv", encoding="utf-8")
        self.value = [self.tree.item(i, "values") for i in self.tree.get_children("")]
        add_element_value = tuple(("-" for i in range(len(self.value[0]))))
        self.value.append(add_element_value)
        self.treeview()
        self.tree.update()

    def select_row(self, event):
        self.row = self.tree.identify_row(event.y)
        self.column = self.tree.identify_column(event.x)
        # print(self.row, self.column)
        return self.column, self.row
    
    def delete_column(self):
        self.data_pd = pd.read_csv("table_do_NE.csv", encoding="utf-8")
        _ = self.data_pd.pop(self.data_pd.columns[-1])
        self.data_pd.to_csv("table_do_NE.csv", index=False, encoding="utf-8")
        self.value = [list(self.data_pd.loc[id]) for id in self.data_pd.index]
        self.columns = list(self.data_pd.columns)
        self.treeview()
        self.tree.update()

    def delete_row(self):
        self.tree.delete(self.row)

    def clear_wind(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = WindTreeview()
    # root.buttons()
    # root.treeview()

    root.mainloop()
