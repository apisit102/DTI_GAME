import csv
from csv import reader

def import_csv_layout(path):
    terrain_map = []  # กำหนดตัวแปร terrain_map ให้เป็นลิสต์ว่าง
    with open(path) as level_map:
        layout = csv.reader(level_map, delimiter = ",")  # ใช้ csv.reader
        for row in layout:
            terrain_map.append(list(row))  # เพิ่มแถวลงใน terrain_map
        return terrain_map
