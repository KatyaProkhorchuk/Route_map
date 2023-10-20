import tkinter as tk
import tkintermapview
from command import *
root = tk.Tk()
root.title("Geo")
root.geometry("800x800")
db, connection = setting_db()
main_menu = tk.Menu(root)
root.config(menu=main_menu)
command_menu = tk.Menu(main_menu, tearoff = False)
main_menu.add_cascade(label = 'Действие', menu=command_menu)
command_menu.add_command(label='Добавить нового персонажа', command = lambda: add_person(db, connection))
command_menu.add_command(label='Включить координаты всех персонажей', command = lambda: get_visible_coordinate(db, connection, map_widget))
command_menu.add_command(label="Посмотреть траекторию", command=get_path)

map_widget = tkintermapview.TkinterMapView(root, width=800, height=800, corner_radius=0)
map_widget.place(x = 0, y = 0)
map_widget.set_position(55.751244, 37.618423) 
map_widget.set_zoom(5)

root.mainloop()