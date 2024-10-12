

import pandas as pd
import tkinter as tk


def save_csv(name, year):
    data.append({'Name': name, 'Year': year})
    data_frame = pd.DataFrame(data)
    data_frame.to_csv(r'C:\Piton\for_Sasha\table.csv', index=False, encoding='utf-8')


def save_data(name, year):
    save_csv(str(name), int(year))


read_file = pd.read_csv(r'C:\Piton\for_Sasha\table.csv', encoding='utf-8')

data = []
for i in range(len(read_file)):
    data.append({'Name': read_file.loc[i]['Name'],
                 'Year': read_file.loc[i]['Year']})

win = tk.Tk()
win.geometry('800x600')
win.title('Таблица')
win.config(bg='#E9E7E7')
name_label = tk.Label(win, text="Имя:")
name_label.grid(row=1, column=0)
name_entry = tk.Entry(win)
name_entry.grid(row=1, column=1)

year_label = tk.Label(win, text="Год:")
year_label.grid(row=2, column=0)
year_entry = tk.Entry(win)
year_entry.grid(row=2, column=1)
save_btn = tk.Button(win, text="Сохранить", command=lambda:
                     save_data(name_entry.get(), year_entry.get()))
save_btn.grid(row=3, column=1)

win.mainloop()
read_file = pd.read_csv(r'C:\Piton\for_Sasha\table.csv', encoding='cp1251')

print(read_file)
