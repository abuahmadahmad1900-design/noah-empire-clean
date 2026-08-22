# -*- coding: utf-8 -*-
import sqlite3
import random
from flask import Flask, request, redirect

app = Flask(__name__)
DB_NAME = 'restaurants.db'

STYLE = '''
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:Tahoma; background:radial-gradient(ellipse at top,#0a0a2e,#000); min-height:100vh; color:#fff; }
.container { max-width:1200px; margin:0 auto; padding:40px 20px; }
.legendary-title { text-align:center; font-size:2.5em; font-weight:900; background:linear-gradient(135deg,#FFD700,#FFA500,#FFD700); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:40px; }
.legendary-table { width:100%; border-collapse:collapse; margin-top:30px; border-radius:30px; overflow:hidden; background:linear-gradient(145deg,rgba(18,18,55,0.98),rgba(8,8,28,0.98)); box-shadow:0 40px 100px rgba(0,0,0,0.9); border:1px solid #FFD700; }
.legendary-table th { background:linear-gradient(145deg,rgba(255,215,0,0.08),rgba(255,140,0,0.08)); color:#FFD700; padding:20px; border-bottom:2px solid #FFD700; }
.legendary-table td { padding:18px; text-align:center; color:#fff; border-bottom:1px solid rgba(255,215,0,0.15); }
.search-bar { display:flex; justify-content:center; align-items:center; gap:15px; flex-wrap:wrap; margin:30px 0; }
.search-bar input { padding:16px 28px; border-radius:50px; border:2px solid #FFD700; background:rgba(10,10,40,0.9); color:#FFD700; font-size:1.1em; width:350px; outline:none; }
.legendary-btn { padding:14px 30px; border-radius:50px; border:2px solid #FFD700; background:linear-gradient(145deg,#1a1a4e,#0d0d2b); color:#FFD700; font-weight:900; cursor:pointer; text-decoration:none; }
.summary-bar { padding:14px 25px; border-radius:50px; border:2px solid #FFD700; background:linear-gradient(145deg,#1a1a4e,#0d0d2b); color:#FFD700; font-weight:900; }
.form-box { display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin:30px 0; }
.form-box input { padding:14px 22px; border-radius:20px; border:2px solid #FFD700; background:rgba(10,10,40,0.9); color:#FFD700; font-size:1em; outline:none; }
</style>
'''

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS restaurants (id INTEGER PRIMARY KEY AUTOINCREMENT, اسم_الطبق TEXT, السعر TEXT, القسم TEXT)')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    rows = ''
    count = 0
    if request.method == 'POST':
        values = [request.form.get(f, '') for f in ['اسم_الطبق', 'السعر', 'القسم']]
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('INSERT INTO restaurants (اسم_الطبق, السعر, القسم) VALUES (?, ?, ?)', values)
        conn.commit()
        conn.close()
        return redirect('/')
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM restaurants ORDER BY id ASC')
    items = c.fetchall()
    count = len(items)
    conn.close()
    for item in items:
        rows += '<tr>'
        for val in item:
            rows += '<td>' + str(val) + '</td>'
        rows += '<td><a href=/edit/' + str(item[0]) + ' class=legendary-btn>تعديل</a> <a href=/delete/' + str(item[0]) + ' class=legendary-btn>حذف</a></td>'
        rows += '</tr>'
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>نظام المطاعم</title>' + STYLE + '</head>'
    html += '<body><div class=container>'
    html += '<h1 class=legendary-title>نظام المطاعم</h1>'
    html += '<div class=form-box><form method=POST style=display:flex;gap:10px;flex-wrap:wrap;>'
    html += '<input type=text name=اسم_الطبق placeholder=اسم_الطبق required> <input type=text name=السعر placeholder=السعر required> <input type=text name=القسم placeholder=القسم required>'
    html += '<button type=submit class=legendary-btn>اضافة</button>'
    html += '</form></div>'
    html += '<div class=search-bar>'
    html += '<input type=text placeholder=بحث... onkeyup=filterGeneric(this)>'
    html += '<a href=/mock-data class=legendary-btn>بيانات تجريبية</a>'
    html += '<a href=/export-csv class=legendary-btn>تصدير CSV</a>'
    html += '<a href=/backup class=legendary-btn>نسخ احتياطي</a>'
    html += '<a href=/report class=legendary-btn>تقرير</a>'
    html += '<a href=/ class=legendary-btn>الرئيسية</a>'
    html += '<span class=summary-bar>العدد: ' + str(count) + '</span>'
    html += '</div>'
    html += '<table class=legendary-table>'
    html += '<thead><tr><th>ID</th><th>اسم_الطبق</th><th>السعر</th><th>القسم</th><th>إجراءات</th></tr></thead>'
    html += '<tbody>' + rows + '</tbody>'
    html += '</table>'
    html += '</div>'
    html += '<script>function filterGeneric(input){var f=input.value.toLowerCase();document.querySelectorAll("tbody tr").forEach(function(r){r.style.display=r.innerText.toLowerCase().includes(f)?"":"none";});}</script>'
    html += '</body></html>'
    return html

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM restaurants WHERE id=?', (item_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if request.method == 'POST':
        values = [request.form.get(f, '') for f in ['اسم_الطبق', 'السعر', 'القسم']]
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        set_parts = ', '.join([f + '=?' for f in ['اسم_الطبق', 'السعر', 'القسم']])
        c.execute('UPDATE restaurants SET ' + set_parts + ' WHERE id=?', values + [item_id])
        conn.commit()
        conn.close()
        return redirect('/')
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM restaurants WHERE id=?', (item_id,))
    item = c.fetchone()
    conn.close()
    if not item:
        return redirect('/')
    edit_inputs = ''
    for i, f in enumerate(['اسم_الطبق', 'السعر', 'القسم']):
        edit_inputs += '<input type=text name=' + f + ' value=' + str(item[i+1]) + ' required> '
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>تعديل</title>' + STYLE + '</head>'
    html += '<body><div class=container>'
    html += '<h1 class=legendary-title>تعديل السجل</h1>'
    html += '<div class=form-box><form method=POST style=display:flex;gap:10px;flex-wrap:wrap;>'
    html += edit_inputs
    html += '<button type=submit class=legendary-btn>حفظ التعديل</button>'
    html += '</form></div>'
    html += '<a href=/ class=legendary-btn>رجوع</a>'
    html += '</div></body></html>'
    return html

@app.route('/export-csv')
def export_csv():
    import csv
    import io
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM restaurants ORDER BY id ASC')
    items = c.fetchall()
    conn.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID'] + ['اسم_الطبق', 'السعر', 'القسم'])
    for item in items:
        writer.writerow(item)
    output.seek(0)
    return output.getvalue(), {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=restaurants.csv'}

@app.route('/backup')
def backup():
    import shutil
    shutil.copy(DB_NAME, DB_NAME + '.backup')
    return redirect('/')

@app.route('/mock-data')
def mock_data():
    samples = ['عينة', 'تجربة', 'منتج', 'خدمة', 'عنصر', 'بند', 'صنف', 'نموذج']
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    for i in range(100):
        values = []
        for f in ['اسم_الطبق', 'السعر', 'القسم']:
            if 'سعر' in f or 'قيمة' in f or 'مبلغ' in f:
                values.append(str(random.randint(1, 1000)))
            elif 'تاريخ' in f:
                values.append('2026-08-' + str(random.randint(1, 28)))
            elif 'كمية' in f or 'عدد' in f:
                values.append(str(random.randint(1, 500)))
            else:
                values.append(samples[random.randint(0, len(samples)-1)] + ' ' + str(i+1))
        placeholders = ', '.join(['?'] * len(['اسم_الطبق', 'السعر', 'القسم']))
        cols = ', '.join(['اسم_الطبق', 'السعر', 'القسم'])
        c.execute('INSERT INTO restaurants (' + cols + ') VALUES (' + placeholders + ')', values)
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/report')
def report():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM restaurants')
    count = c.fetchone()[0]
    conn.close()
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>التقرير</title>' + STYLE + '</head>'
    html += '<body><div class=container>'
    html += '<h1 class=legendary-title>التقرير الشامل</h1>'
    html += '<div class=summary-bar>عدد السجلات: ' + str(count) + '</div>'
    html += '<br><a href=/ class=legendary-btn>رجوع</a>'
    html += '</div></body></html>'
    return html

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5100)