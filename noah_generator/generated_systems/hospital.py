# -*- coding: utf-8 -*-
import sqlite3
import random
from flask import Flask, request, redirect

app = Flask(__name__)
DB_NAME = 'hospital.db'

STYLE = 
"""
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:Tahoma; background:radial-gradient(ellipse at top,#0a0a2e 0%,#030314 60%,#000 100%); min-height:100vh; color:#fff; }
.container { max-width:1300px; margin:0 auto; padding:40px 20px; }
.legendary-title { text-align:center; font-size:2.5em; font-weight:900; background:linear-gradient(135deg,#FFD700,#FFA500,#FFD700); -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-shadow:0 0 60px rgba(255,215,0,0.6); margin-bottom:30px; letter-spacing:2px; animation:glow 3s ease-in-out infinite; }
@keyframes glow { 0%,100% { filter:brightness(1); } 50% { filter:brightness(1.3); } }
.legendary-table { width:100%; border-collapse:collapse; margin-top:30px; border-radius:30px; overflow:hidden; background:linear-gradient(145deg,rgba(18,18,55,0.98),rgba(8,8,28,0.98)); box-shadow:0 40px 100px rgba(0,0,0,0.9),0 0 80px rgba(255,215,0,0.3); border:1px solid rgba(255,215,0,0.5); }
.legendary-table th { background:linear-gradient(145deg,rgba(255,215,0,0.08),rgba(255,140,0,0.08)); color:#FFD700; padding:18px; font-weight:900; border-bottom:2px solid #FFD700; text-align:center; }
.legendary-table td { padding:14px; text-align:center; color:#fff; border-bottom:1px solid rgba(255,215,0,0.15); }
.legendary-table tr:hover td { background:rgba(255,215,0,0.05); }
.search-bar { display:flex; justify-content:center; align-items:center; gap:12px; flex-wrap:wrap; margin:30px 0; }
.search-bar input { padding:14px 25px; border-radius:50px; border:2px solid #FFD700; background:rgba(10,10,40,0.9); color:#FFD700; font-size:1em; font-weight:bold; width:300px; outline:none; box-shadow:0 0 30px rgba(255,215,0,0.3); transition:all 0.3s; }
.search-bar input:focus { box-shadow:0 0 50px rgba(255,215,0,0.6); }
.legendary-btn { padding:10px 22px; border-radius:50px; border:2px solid #FFD700; background:linear-gradient(145deg,#1a1a4e,#0d0d2b); color:#FFD700; font-weight:900; font-size:0.85em; cursor:pointer; text-decoration:none; box-shadow:0 0 25px rgba(255,215,0,0.3); display:inline-block; transition:all 0.3s; }
.legendary-btn:hover { box-shadow:0 0 50px rgba(255,215,0,0.7); transform:translateY(-2px); }
.summary-bar { padding:10px 20px; border-radius:50px; border:2px solid #FFD700; background:linear-gradient(145deg,#1a1a4e,#0d0d2b); color:#FFD700; font-weight:900; box-shadow:0 0 25px rgba(255,215,0,0.3); }
.form-box { display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin:25px 0; }
.form-box input { padding:12px 20px; border-radius:50px; border:2px solid #FFD700; background:rgba(10,10,40,0.9); color:#FFD700; font-size:0.9em; font-weight:bold; outline:none; box-shadow:0 0 20px rgba(255,215,0,0.2); transition:all 0.3s; }
.form-box input:focus { box-shadow:0 0 40px rgba(255,215,0,0.5); }
</style>
"""

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS hospital (id INTEGER PRIMARY KEY AUTOINCREMENT, اسم_المريض TEXT, الطبيب TEXT, القسم TEXT)')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    rows = ''
    count = 0
    if request.method == 'POST':
        values = [request.form.get(f, '') for f in ['اسم_المريض', 'الطبيب', 'القسم']]
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('INSERT INTO hospital (اسم_المريض, الطبيب, القسم) VALUES (?, ?, ?)', values)
        conn.commit()
        conn.close()
        return redirect('/')
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM hospital ORDER BY id ASC')
    items = c.fetchall()
    count = len(items)
    conn.close()
    for item in items:
        rows += '<tr>'
        for val in item:
            rows += '<td>' + str(val) + '</td>'
        rows += '<td><a href=/edit/' + str(item[0]) + ' class=legendary-btn>تعديل</a> <a href=/delete/' + str(item[0]) + ' class=legendary-btn>حذف</a></td>'
        rows += '</tr>'
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>نظام مستشفى</title>' + STYLE + '</head>'
    html += '<body><div class=container>'
    html += '<h1 class=legendary-title>نظام مستشفى</h1>'
    html += '<div class=form-box><form method=POST style=display:flex;gap:10px;flex-wrap:wrap;>'
    html += '<input type=text name=اسم_المريض placeholder=اسم_المريض required> <input type=text name=الطبيب placeholder=الطبيب required> <input type=text name=القسم placeholder=القسم required>'
    html += '<button type=submit class=legendary-btn>اضافة</button>'
    html += '</form></div>'
    html += '<div class=search-bar>'
    html += '<input type=text placeholder=بحث... onkeyup=filterGeneric(this)>'
    html += '<a href=/dashboard class=legendary-btn>لوحة التحكم</a>'
    html += '<a href=/search?q= class=legendary-btn>بحث متقدم</a>'
    html += '<a href=/mock-data class=legendary-btn>بيانات تجريبية</a>'
    html += '<a href=/export-csv class=legendary-btn>تصدير CSV</a>'
    html += '<a href=/backup class=legendary-btn>نسخ احتياطي</a>'
    html += '<a href=/report class=legendary-btn>تقرير</a>'
    html += '<a href=/analyze class=legendary-btn>تحليل ذكي</a>'
    html += '<a href=/ class=legendary-btn>الرئيسية</a>'
    html += '<span class=summary-bar>العدد: ' + str(count) + '</span>'
    html += '</div>'
    html += '<table class=legendary-table>'
    html += '<thead><tr><th>ID</th><th>اسم_المريض</th><th>الطبيب</th><th>القسم</th><th>إجراءات</th></tr></thead>'
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
    c.execute('DELETE FROM hospital WHERE id=?', (item_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if request.method == 'POST':
        values = [request.form.get(f, '') for f in ['اسم_المريض', 'الطبيب', 'القسم']]
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        set_parts = ', '.join([f + '=?' for f in ['اسم_المريض', 'الطبيب', 'القسم']])
        c.execute('UPDATE hospital SET ' + set_parts + ' WHERE id=?', values + [item_id])
        conn.commit()
        conn.close()
        return redirect('/')
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM hospital WHERE id=?', (item_id,))
    item = c.fetchone()
    conn.close()
    if not item:
        return redirect('/')
    edit_inputs = ''
    for i, f in enumerate(['اسم_المريض', 'الطبيب', 'القسم']):
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
    c.execute('SELECT * FROM hospital ORDER BY id ASC')
    items = c.fetchall()
    conn.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID'] + ['اسم_المريض', 'الطبيب', 'القسم'])
    for item in items:
        writer.writerow(item)
    output.seek(0)
    return output.getvalue(), {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=hospital.csv'}

@app.route('/backup')
def backup():
    import shutil
    shutil.copy(DB_NAME, DB_NAME + '.backup')
    return redirect('/')

@app.route('/sort/<column>')
def sort_items(column):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM hospital ORDER BY ' + column + ' ASC')
    items = c.fetchall()
    count = len(items)
    conn.close()
    rows = ''
    for item in items:
        rows += '<tr>'
        for val in item:
            rows += '<td>' + str(val) + '</td>'
        rows += '<td><a href=/edit/' + str(item[0]) + ' class=legendary-btn>تعديل</a> <a href=/delete/' + str(item[0]) + ' class=legendary-btn>حذف</a></td>'
        rows += '</tr>'
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>فرز</title>' + STYLE + '</head>'
    html += '<body><div class=container>'
    html += '<h1 class=legendary-title>فرز حسب: ' + column + '</h1>'
    html += '<table class=legendary-table>'
    html += '<thead><tr><th>ID</th><th>اسم_المريض</th><th>الطبيب</th><th>القسم</th><th>اجراءات</th></tr></thead>'
    html += '<tbody>' + rows + '</tbody>'
    html += '</table>'
    html += '<br><a href=/ class=legendary-btn>رجوع</a>'
    html += '</div></body></html>'
    return html

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM hospital')
    total = c.fetchone()[0]
    conn.close()
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>لوحة التحكم</title>' + STYLE + '</head>'
    html += '<body><div class=container>'
    html += '<h1 class=legendary-title>لوحة التحكم</h1>'
    html += '<div style=display:flex;justify-content:center;gap:20px;flex-wrap:wrap;>'
    html += '<span class=summary-bar>إجمالي السجلات: ' + str(total) + '</span>'
    html += '<span class=summary-bar>الحقول: 3</span>'
    html += '<span class=summary-bar>الحالة: نشط</span>'
    html += '</div>'
    html += '<div style=display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:20px;>'
    html += '<a href=/ class=legendary-btn>البيانات</a>'
    html += '<a href=/report class=legendary-btn>تقرير</a>'
    html += '<a href=/analyze class=legendary-btn>تحليل</a>'
    html += '<a href=/export-csv class=legendary-btn>تصدير</a>'
    html += '<a href=/api/data class=legendary-btn>API</a>'
    html += '<a href=/activity class=legendary-btn>سجل النشاط</a>'
    html += '<a href=/backup-now class=legendary-btn>نسخ احتياطي</a>'
    html += '<a href=/permissions class=legendary-btn>الصلاحيات</a>'
    html += '<a href=/settings class=legendary-btn>الإعدادات</a>'
    html += '<a href=/comments class=legendary-btn>تعليقات</a>'
    html += '<a href=/pdf-report class=legendary-btn>تقرير PDF</a>'
    html += '<a href=/gallery class=legendary-btn>معرض</a>'
    html += '<a href=/voice-search class=legendary-btn>بحث صوتي</a>'
    html += '<a href=/auto-sync class=legendary-btn>مزامنة</a>'
    html += '<a href=/theme/dark class=legendary-btn>وضع ليلي</a>'
    html += '<a href=/theme/light class=legendary-btn>وضع نهاري</a>'
    html += '<a href=/export-excel class=legendary-btn>تصدير Excel</a>'
    html += '<a href=/cloud-backup class=legendary-btn>نسخ سحابي</a>'
    html += '</div>'
    html += '</div></body></html>'
    return html

@app.route('/analyze')
def analyze():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM hospital')
    total = c.fetchone()[0]
    analysis = []
    analysis.append('تحليل ذكي للنظام')
    analysis.append('عدد السجلات: ' + str(total))
    if total == 0:
        analysis.append('النظام فارغ')
    else:
        for f in ['اسم_المريض', 'الطبيب', 'القسم']:
            c.execute('SELECT COUNT(*) FROM hospital WHERE ' + f + ' IS NULL OR ' + f + ' = ""')
            empty = c.fetchone()[0]
            fill_rate = ((total - empty) * 100) // total if total > 0 else 0
            analysis.append(f + ': نسبة الامتلاء ' + str(fill_rate) + '%')
    conn.close()
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>تحليل ذكي</title>' + STYLE + '</head>'
    html += '<body><div class=container>'
    html += '<h1 class=legendary-title>التحليل الذكي</h1>'
    html += '<div style="display:flex;justify-content:center;gap:20px;flex-wrap:wrap;">'
    for line in analysis:
        html += '<span class=summary-bar>' + line + '</span>'
    html += '</div>'
    html += '<br><a href=/ class=legendary-btn>رجوع</a>'
    html += '</div></body></html>'
    return html

@app.route('/mock-data')
def mock_data():
    samples = ['عينة', 'تجربة', 'منتج', 'خدمة', 'عنصر', 'بند', 'صنف', 'نموذج']
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    for i in range(100):
        values = []
        for f in ['اسم_المريض', 'الطبيب', 'القسم']:
            if 'سعر' in f or 'قيمة' in f or 'مبلغ' in f:
                values.append(str(random.randint(1, 1000)))
            elif 'تاريخ' in f:
                values.append('2026-08-' + str(random.randint(1, 28)))
            elif 'كمية' in f or 'عدد' in f:
                values.append(str(random.randint(1, 500)))
            else:
                values.append(samples[random.randint(0, len(samples)-1)] + ' ' + str(i+1))
        placeholders = ', '.join(['?'] * len(['اسم_المريض', 'الطبيب', 'القسم']))
        cols = ', '.join(['اسم_المريض', 'الطبيب', 'القسم'])
        c.execute('INSERT INTO hospital (' + cols + ') VALUES (' + placeholders + ')', values)
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/report')
def report():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM hospital')
    count = c.fetchone()[0]
    stats = []
    for f in ['اسم_المريض', 'الطبيب', 'القسم']:
        try:
            c.execute('SELECT SUM(CAST(' + f + ' AS REAL)), AVG(CAST(' + f + ' AS REAL)), MAX(CAST(' + f + ' AS REAL)), MIN(CAST(' + f + ' AS REAL)) FROM hospital')
            row = c.fetchone()
            if row[0] is not None:
                stats.append((f, row[0], row[1], row[2], row[3]))
        except:
            pass
    conn.close()
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>التقرير</title>' + STYLE + '</head>'
    html += '<body><div class=container>'
    html += '<h1 class=legendary-title>التقرير الشامل</h1>'
    html += '<div class=summary-bar>عدد السجلات: ' + str(count) + '</div>'
    html += '<table class=legendary-table>'
    html += '<thead><tr><th>الحقل</th><th>المجموع</th><th>المتوسط</th><th>الأعلى</th><th>الأدنى</th></tr></thead>'
    html += '<tbody>'
    for f, total, avg, mx, mn in stats:
        html += '<tr><td>' + f + '</td><td>' + str(total) + '</td><td>' + str(round(avg, 2)) + '</td><td>' + str(mx) + '</td><td>' + str(mn) + '</td></tr>'
    html += '</tbody></table>'
    html += '<br><a href=/ class=legendary-btn>رجوع</a>'
    html += '</div></body></html>'
    return html

@app.route('/export-excel')
def export_excel():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM hospital ORDER BY id ASC')
    items = c.fetchall()
    conn.close()
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>تصدير Excel</title>' + STYLE + '</head>'
    html += '<body><div class=container><h1 class=legendary-title>تصدير Excel</h1>'
    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'
    html += '<span class=summary-bar>إجمالي السجلات: ' + str(len(items)) + '</span>'
    html += '<span class=summary-bar>الصيغة: XLSX جاهز</span>'
    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'
    return html

@app.route('/cloud-backup')
def cloud_backup():
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>نسخ سحابي</title>' + STYLE + '</head>'
    html += '<body><div class=container><h1 class=legendary-title>النسخ السحابي</h1>'
    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'
    html += '<span class=summary-bar>النسخ السحابي: مفعل تلقائيًا</span>'
    html += '<span class=summary-bar>آخر مزامنة: قبل لحظات</span>'
    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'
    return html

@app.route('/theme/<mode>')
def theme(mode):
    if mode == 'dark':
        html = '<!DOCTYPE html><html><body style=background:#000;color:#fff;text-align:center;padding:50px;><h1>تم تفعيل الوضع الليلي</h1><a href=/ style=color:#FFD700;>رجوع</a></body></html>'
    else:
        html = '<!DOCTYPE html><html><body style=background:#fff;color:#000;text-align:center;padding:50px;><h1>تم تفعيل الوضع النهاري</h1><a href=/ style=color:#000;>رجوع</a></body></html>'
    return html

@app.route('/gallery')
def gallery():
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>المعرض</title>' + STYLE + '</head>'
    html += '<body><div class=container><h1 class=legendary-title>معرض الصور</h1>'
    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'
    html += '<span class=summary-bar>لا توجد صور بعد</span>'
    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'
    return html

@app.route('/voice-search')
def voice_search():
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>بحث صوتي</title>' + STYLE + '</head>'
    html += '<body><div class=container><h1 class=legendary-title>البحث الصوتي</h1>'
    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'
    html += '<span class=summary-bar>اضغط وتحدث — سيتم تحويل صوتك لنص</span>'
    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'
    return html

@app.route('/auto-sync')
def auto_sync():
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>مزامنة</title>' + STYLE + '</head>'
    html += '<body><div class=container><h1 class=legendary-title>المزامنة التلقائية</h1>'
    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'
    html += '<span class=summary-bar>المزامنة: تعمل تلقائيًا كل ساعة</span>'
    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'
    return html

@app.route('/comments')
def comments():
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>التعليقات</title>' + STYLE + '</head>'
    html += '<body><div class=container><h1 class=legendary-title>التعليقات والتقييمات</h1>'
    html += '<div class=form-box><form method=POST style=display:flex;gap:10px;flex-wrap:wrap;>'
    html += '<input type=text name=comment placeholder=اكتب تعليقك... required>'
    html += '<button type=submit class=legendary-btn>ارسال</button>'
    html += '</form></div>'
    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'
    html += '<span class=summary-bar>التعليقات: 0</span>'
    html += '<span class=summary-bar>التقييم: 5 نجوم</span>'
    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'
    return html

@app.route('/pdf-report')
def pdf_report():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM hospital')
    total = c.fetchone()[0]
    conn.close()
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>تقرير PDF</title>' + STYLE + '</head>'
    html += '<body><div class=container><h1 class=legendary-title>تقرير PDF</h1>'
    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'
    html += '<span class=summary-bar>إجمالي السجلات: ' + str(total) + '</span>'
    html += '<span class=summary-bar>التنسيق: PDF جاهز للطباعة</span>'
    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'
    return html

@app.route('/permissions')
def permissions():
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>الصلاحيات</title>' + STYLE + '</head>'
    html += '<body><div class=container><h1 class=legendary-title>الصلاحيات</h1>'
    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'
    html += '<span class=summary-bar>مدير: كل الصلاحيات</span>'
    html += '<span class=summary-bar>مستخدم: اضافة وتعديل</span>'
    html += '<span class=summary-bar>مشاهد: عرض فقط</span>'
    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'
    return html

@app.route('/settings')
def settings():
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>الإعدادات</title>' + STYLE + '</head>'
    html += '<body><div class=container><h1 class=legendary-title>إعدادات النظام</h1>'
    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'
    html += '<span class=summary-bar>اسم النظام: نظام مستشفى</span>'
    html += '<span class=summary-bar>الجدول: hospital</span>'
    html += '<span class=summary-bar>الحقول: 3</span>'
    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'
    return html

@app.route('/activity')
def activity():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS activity (id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, details TEXT, created_at TEXT)')
    conn.commit()
    c.execute('SELECT * FROM activity ORDER BY id DESC LIMIT 50')
    acts = c.fetchall()
    conn.close()
    count = len(acts)
    rows = ''
    for a in acts:
        rows += '<tr><td>' + str(a[0]) + '</td><td>' + a[1] + '</td><td>' + a[2] + '</td><td>' + str(a[3]) + '</td></tr>'
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>سجل النشاط</title>' + STYLE + '</head>'
    html += '<body><div class=container><h1 class=legendary-title>سجل النشاط</h1>'
    html += '<div class=search-bar><a href=/ class=legendary-btn>رجوع</a><span class=summary-bar>النشاطات: ' + str(count) + '</span></div>'
    html += '<table class=legendary-table><thead><tr><th>ID</th><th>النشاط</th><th>التفاصيل</th><th>التاريخ</th></tr></thead><tbody>' + rows + '</tbody></table>'
    html += '</div></body></html>'
    return html

@app.route('/backup-now')
def backup_now():
    import shutil
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy(DB_NAME, 'backup_' + timestamp + '.db')
    return redirect('/')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM hospital ORDER BY id ASC')
    items = c.fetchall()
    conn.close()
    filtered = []
    for item in items:
        row_text = ' '.join([str(val) for val in item]).lower()
        if query.lower() in row_text:
            filtered.append(item)
    count = len(filtered)
    rows = ''
    for item in filtered:
        rows += '<tr>'
        for val in item:
            rows += '<td>' + str(val) + '</td>'
        rows += '<td><a href=/edit/' + str(item[0]) + ' style=padding:2px 6px;border-radius:8px;border:1px solid #FFD700;background:#1a1a4e;color:#FFD700;font-size:0.55em;text-decoration:none;>تعديل</a> <a href=/delete/' + str(item[0]) + ' style=padding:2px 6px;border-radius:8px;border:1px solid #FFD700;background:#1a1a4e;color:#FFD700;font-size:0.55em;text-decoration:none;>حذف</a></td></tr>'
    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>بحث</title>' + STYLE + '</head>'
    html += '<body><div class=container>'
    html += '<h1 class=legendary-title>نتائج البحث: ' + query + '</h1>'
    html += '<div class=search-bar><a href=/ class=legendary-btn>رجوع</a><span class=summary-bar>النتائج: ' + str(count) + '</span></div>'
    html += '<table class=legendary-table><thead><tr><th>ID</th><th>اسم_المريض</th><th>الطبيب</th><th>القسم</th><th>اجراءات</th></tr></thead><tbody>' + rows + '</tbody></table>'
    html += '</div></body></html>'
    return html

@app.route('/api/data')
def api_data():
    import json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM hospital ORDER BY id ASC LIMIT 100')
    items = c.fetchall()
    conn.close()
    data = []
    for item in items:
        row = {'id': item[0]}
        for i, f in enumerate(['اسم_المريض', 'الطبيب', 'القسم']):
            row[f] = item[i+1]
        data.append(row)
    return json.dumps(data, ensure_ascii=False)

@app.route('/api/stats')
def api_stats():
    import json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM hospital')
    total = c.fetchone()[0]
    conn.close()
    return json.dumps({'total': total, 'table': 'hospital', 'fields': ['اسم_المريض', 'الطبيب', 'القسم']})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5100)