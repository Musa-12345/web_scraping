import pandas as pd
import sqlite3

# Excel dosyasının adı
excel_file_path = 'urun_fiyat_listesi.xlsx'

# SQLite veritabanı dosyasının adı
database_file_path = 'your_database.db'

# Excel dosyasındaki veriyi bir pandas DataFrame'e yükleme
df = pd.read_excel(excel_file_path)

# SQLite veritabanına bağlanma
conn = sqlite3.connect(database_file_path)

# DataFrame'i SQLite veritabanına yazma
df.to_sql('evdeeczane.com veriler', conn, index=False, if_exists='replace')

# Bağlantıyı kapatma
conn.close()

print(f"Veriler {database_file_path} veritabanına başarıyla aktarıldı.")
