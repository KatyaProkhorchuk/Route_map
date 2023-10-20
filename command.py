import sqlalchemy as db
import tkinter as tk
import datetime
marker = []
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
        time = datetime.datetime.strptime(datetime_entry.get(), "%Y-%m-%d %H:%M:%S")
        latitude = float(latitude_entry.get())
        longitude = float(longitude_entry.get())
        insert_query = users.insert().values(name=name, time = time, latitude = latitude, longtitude=longitude)
        connection.execute(insert_query)
        select_all_query = db.select(users)
        select_all_result = connection.execute(select_all_query)
        print(select_all_result.fetchall())
    top = tk.Toplevel()
    top.title("Добавить персонажа")
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
            # Отобразите последние координаты на карте
            # mar.add_marker(latitude, longitude, character_name)

def get_path():
    pass