from tablica import WindTreeview

columns = ["Год, до н.э.", "Египет", "Вавилон"]
value = [[2500, "Что то", "И тут что то"], [1500, "Опять что происходит", "Тут на удивление всё спокойно"]]


def add_column():
    columns.append('Название страны')
    wind.tree.update()
    print(columns)


wind = WindTreeview()
wind.treeview(columns=columns, value=value)
wind.button(text='Добавить колонку', func=add_column, column=0, row=1)
wind.mainloop()



