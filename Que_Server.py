import time
import sqlite3
from PyQt5 import uic
from PyQL import PyQL


MP = 10


def count_intervals(min_val, max_val):
    dif = max_val - min_val
    if min_val == 0:
        min_val = 1
    rel_dif = dif / min_val
    point_dif = rel_dif * MP
    if point_dif > MP:
        point_dif = MP

    left = (MP - point_dif) / 2
    right = left + point_dif
    return (point_dif, (left, right))


# This is server!

time_interval = 10

conn = sqlite3.connect("Que.db")
PQLE = PyQL(conn, "Que")

while True:
    data = PQLE.select("cashboxes")
    clicks = list(map(lambda x: x[1], data))
    points = []
    
    min_value = min(clicks)
    max_value = max(clicks)
    value_dif = max_value - min_value

    point_dif, interval = count_intervals(min_value, max_value)

    for cashbox in data:
        click = cashbox[1]
        if value_dif == 0:
            value_dif = 1
        points.append(interval[0] + point_dif * (click - min_value) / (value_dif))
            

    for i in range(len(points)):
        point = points[i]
        PQLE.update("cashboxes", "status", round(point), [f"id = {data[i][0]}"])

    PQLE.update("cashboxes", "clicks", 0)
    PQLE.commit()

    time.sleep(time_interval)


conn.close()
