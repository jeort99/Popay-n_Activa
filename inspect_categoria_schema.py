import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popayanactiva.settings')
import django
django.setup()
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='Categorias'")
    for row in cursor.fetchall():
        print(row)
