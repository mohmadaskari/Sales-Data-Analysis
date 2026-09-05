import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. اتصال به دیتابیس و ساخت جدول
conn = sqlite3.connect("company_sales.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    category TEXT,
    price REAL,
    quantity INTEGER,
    city TEXT,
    order_date TEXT
)
''')

# 2. ورود داده‌های نمونه
data = [
    ("Laptop", "Electronics", 1200.0, 2, "Berlin", "2026-01-10"),
    ("Mouse", "Electronics", 25.0, 5, "Duisburg", "2026-01-12"),
    ("Monitor", "Electronics", 300.0, 3, "Essen", "2026-01-15"),
    ("Desk Chair", "Furniture", 180.0, 4, "Duisburg", "2026-02-01"),
    ("Laptop", "Electronics", 1200.0, 1, "Köln", "2026-02-05"),
    ("Desk Chair", "Furniture", 180.0, 2, "Berlin", "2026-02-10"),
    ("Keyboard", "Electronics", 50.0, 6, "Duisburg", "2026-02-15"),
    ("Monitor", "Electronics", 300.0, 2, "Essen", "2026-03-01")
]

cursor.executemany('''
INSERT INTO sales (product, category, price, quantity, city, order_date)
VALUES (?, ?, ?, ?, ?, ?)
''', data)
conn.commit()

# 3. اجرای کوئری SQL برای تحلیل فروش شهرها
query = '''
SELECT city, SUM(price * quantity) as total_revenue
FROM sales
GROUP BY city
ORDER BY total_revenue DESC
'''

df = pd.read_sql_query(query, conn)
print("--- درآمد کل به تفکیک شهرها ---")
print(df)

# 4. رسم نمودار میله‌ای با پایتون
plt.figure(figsize=(8, 5))
plt.bar(df['city'], df['total_revenue'], color='skyblue')
plt.title('Total Revenue by City (2026)')
plt.xlabel('City')
plt.ylabel('Revenue (EUR)')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# ذخیره نمودار
plt.savefig("revenue_by_city.png")
print("\n✅ نمودار با موفقیت به عنوان 'revenue_by_city.png' ذخیره شد!")

conn.close()