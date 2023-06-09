import pymysql
import os
from PIL import Image

conobj = pymysql.connect(host='192.168.1.13', port=3306, user='swarnava', password='root', database='indrive')
curobj = conobj.cursor()

curobj.execute("SELECT reg_no, img, phase FROM indrive")
rows = curobj.fetchall()

for row in rows:
    folder_name = row[0]
    image_data = row[1]
    main = row[2]

    folder_path = os.path.join(".", main)
    os.makedirs(folder_path, exist_ok=True)

    folder_path = os.path.join(folder_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    image_path = os.path.join(folder_path, "image.jpg")
    with open(image_path, "wb") as file:
        file.write(image_data)

conobj.commit()
conobj.close()
print('Success!')
