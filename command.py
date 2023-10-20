import sqlalchemy as db
import tkinter as tk
import datetime
from tkinter import messagebox
marker = []
marker_path = []
def setting_db():
    engine = db.create_engine('sqlite:///users.db')
    connection = engine.connect()
    metadata = db.MetaData()
    insp = db.inspect(engine)
    if not insp.has_table('users_info'):
        users = db.Table('users_info', metadata,
                        db.Column('user_id', db.Integer, primary_key=True),
                        db.Column('name', db.String),
                        db.Column('time', db.DateTime),
                        db.Column('latitude', db.Float),
                        db.Column('longtitude', db.Float))
        metadata.create_all(engine)
    else:
        users = db.Table('users_info', metadata, autoload=True, autoload_with=engine)
    return users, connection
def add_person(users, connection):
    def add_person_in_db(users):
        name = name_entry.get()
        try:
            time = datetime.datetime.strptime(datetime_entry.get(), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат времени. Используйте 'ГГГГ-ММ-ДД ЧЧ:ММ:СС'.")
            return
        latitude = float(latitude_entry.get())
        longitude = float(longitude_entry.get())
        insert_query = users.insert().values(name=name, time = time, latitude = latitude, longtitude=longitude)
        connection.execute(insert_query)
        select_all_query = db.select(users)
        select_all_result = connection.execute(select_all_query)
        print(select_all_result.fetchall())
    top = tk.Toplevel()
    top.title("Добавить данные")
    name = tk.Label(top, text="Имя персонажа:")
    name.pack()
    name_entry = tk.Entry(top)
    name_entry.pack()
    
    datetime_label = tk.Label(top, text="Дата и время (в формате 'ГГГГ-ММ-ДД ЧЧ:ММ:СС'):")
    datetime_label.pack()
    datetime_entry = tk.Entry(top)
    datetime_entry.pack()
    
    latitude_label = tk.Label(top, text="Широта:")
    latitude_label.pack()
    latitude_entry = tk.Entry(top)
    latitude_entry.pack()
    
    longitude_label = tk.Label(top, text="Долгота:")
    longitude_label.pack()
    longitude_entry = tk.Entry(top)
    longitude_entry.pack()
    save_button = tk.Button(top, text="Сохранить", command=lambda: add_person_in_db(users))
    save_button.pack()
def get_visible_coordinate(users, connection, map_widget):
    query = db.select([users.c.name, db.func.max(users.c.time).label("max_time"), users.c.latitude, users.c.longtitude]).group_by(users.c.name)
    result = connection.execute(query).fetchall()
    if result:
        for row in result:
            character_name = row["name"]
            max_time = row["max_time"]
            latitude = row["latitude"]
            longitude = row["longtitude"]
            marker.append(map_widget.set_marker(latitude, longitude, text = character_name))
            
def get_path(users, connection, map_widget):
    def show_path():
        name = name_entry.get()
        try:
            start_time = datetime.datetime.strptime(start_time_entry.get(), "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(end_time_entry.get(), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат времени. Используйте 'ГГГГ-ММ-ДД ЧЧ:ММ:СС'.")
            return
        top.grab_release()
        query = db.select([users.c.latitude, users.c.longtitude, users.c.time]).where(
            (users.c.name == name) & (users.c.time >= start_time) & (users.c.time <= end_time)
        )
        result = connection.execute(query).fetchall()
        print(result)
        marker_path = []
        if result:
            for row in result:
                latitude = row["latitude"]
                longitude = row["longtitude"]
                time = row["time"]
                marker_path.append(map_widget.set_marker(latitude, longitude, text = time))
            print(len(marker_path))
            if len(marker_path) > 1:
                
                path = map_widget.set_path([i.position for i in marker_path])
    top = tk.Toplevel()
    top.title("Посмотреть путь для...")
    name_label = tk.Label(top, text="Имя персонажа:")
    name_label.pack()
    name_entry = tk.Entry(top)
    name_entry.pack()
    
    start_time_label = tk.Label(top, text="Начальное время (ГГГГ-ММ-ДД ЧЧ:ММ:СС):")
    start_time_label.pack()
    start_time_entry = tk.Entry(top)
    start_time_entry.pack()

    end_time_label = tk.Label(top, text="Конечное время (ГГГГ-ММ-ДД ЧЧ:ММ:СС):")
    end_time_label.pack()
    end_time_entry = tk.Entry(top)
    end_time_entry.pack()

    show_button = tk.Button(top, text="Отобразить маршрут", command=show_path)
    show_button.pack()

def delete(map_widget):
    map_widget.delete_all_marker()
