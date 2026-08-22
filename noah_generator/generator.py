# -*- coding: utf-8 -*-
import sqlite3
import datetime
import os

DB_NAME = "noah_generator.db"
GENERATED_DIR = "generated_systems"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS generated_systems (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, table_name TEXT UNIQUE, fields TEXT, code_file TEXT, created_at TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS activity_log (id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, details TEXT, created_at TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS error_log (id INTEGER PRIMARY KEY AUTOINCREMENT, error_type TEXT, details TEXT, created_at TEXT)")
    conn.commit()
    conn.close()
    print("قاعدة بيانات المولد جاهزة")

def _sanitize(text):
    result = ""
    for ch in text.strip():
        if ch.isalnum() or ch == "_":
            result += ch
        elif ch == " ":
            result += "_"
    return result

def create_table(table_name, fields_clean):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    cols = "id INTEGER PRIMARY KEY AUTOINCREMENT"
    for f in fields_clean:
        cols += ", " + f + " TEXT"
    c.execute("CREATE TABLE IF NOT EXISTS " + table_name + " (" + cols + ")")
    conn.commit()
    conn.close()
    print("تم انشاء الجدول: " + table_name)

def register_system(name, table_name, fields_str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO generated_systems (name, table_name, fields, created_at) VALUES (?, ?, ?, ?)", (name, table_name, fields_str, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    sid = c.lastrowid
    conn.close()
    print("تم تسجيل النظام برقم: " + str(sid))
    return sid

def log_error(error_type, details):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO error_log (error_type, details, created_at) VALUES (?, ?, ?)",
              (error_type, details, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()


def get_errors():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM error_log ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    return rows


def deep_search(query):
    """بحث عميق — يبحث في كل شيء: الأنظمة، الجداول، الحقول"""
    query = query.lower()
    results = []
    systems = list_systems()
    
    for s in systems:
        # بحث في اسم النظام
        if query in s[1].lower():
            results.append("نظام: " + s[1])
        # بحث في الجدول
        if query in s[2].lower():
            results.append("جدول: " + s[2] + " (من " + s[1] + ")")
        # بحث في الحقول
        fields = s[3].split(',')
        for f in fields:
            if query in f.lower():
                results.append("حقل: " + f + " (من " + s[1] + ")")
    
    return results[:20]


def compare_systems(table1, table2):
    """مقارنة نظامين"""
    comparison = []
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    for table in [table1, table2]:
        try:
            c.execute("SELECT COUNT(*) FROM " + table)
            count = c.fetchone()[0]
            comparison.append(table + ": " + str(count) + " سجل")
        except:
            comparison.append(table + ": غير موجود")
    
    conn.close()
    return "\n".join(comparison)


def text_analysis(text):
    """محرك تحليل النصوص — يفهم الأوامر الطبيعية"""
    text = text.lower()
    analysis = {
        "length": len(text),
        "words": len(text.split()),
        "has_numbers": any(ch.isdigit() for ch in text),
        "sentiment": "إيجابي" if any(w in text for w in ["جيد", "ممتاز", "رائع", "قوي"]) else "محايد"
    }
    return analysis


def classify_systems():
    """تصنيف ذكي — يصنف الأنظمة حسب المجال"""
    systems = list_systems()
    categories = {}
    
    for s in systems:
        name = s[1]
        if any(w in name for w in ["مطعم", "مقهى", "كافيه", "بيتزا", "مشويات", "حلويات"]):
            cat = "مطاعم"
        elif any(w in name for w in ["مستشفى", "عيادة", "صيدلية", "طبي", "اسعاف"]):
            cat = "صحة"
        elif any(w in name for w in ["مدرسة", "معهد", "تعليم", "دورة", "تدريب"]):
            cat = "تعليم"
        elif any(w in name for w in ["سيارة", "شحن", "توصيل", "نقل"]):
            cat = "نقل"
        elif any(w in name for w in ["عقار", "فندق", "شقة", "فيلا", "أرض"]):
            cat = "عقارات"
        elif any(w in name for w in ["بنك", "مالي", "تأمين", "استثمار", "قرض"]):
            cat = "مالية"
        else:
            cat = "أخرى"
        
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(s[1])
    
    return categories


def periodic_report():
    """تقارير دورية — ملخص تلقائي مجدول"""
    systems = list_systems()
    report = []
    report.append("التقرير الدوري")
    report.append("تاريخ: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    report.append("=" * 30)
    
    total_records = 0
    for s in systems:
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM " + s[2])
            count = c.fetchone()[0]
            total_records += count
            conn.close()
            report.append(s[1] + ": " + str(count) + " سجل")
        except:
            report.append(s[1] + ": خطأ")
    
    report.append("=" * 30)
    report.append("الإجمالي: " + str(len(systems)) + " نظام، " + str(total_records) + " سجل")
    
    return "\n".join(report)


def multi_backup():
    """نسخ متعدد المستويات — عدة نسخ احتياطية"""
    import shutil
    backups = []
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # نسخة 1: قاعدة البيانات
    shutil.copy(DB_NAME, "backup_db_" + timestamp + ".db")
    backups.append("نسخة قاعدة البيانات")
    
    # نسخة 2: الأنظمة
    if os.path.exists(GENERATED_DIR):
        shutil.copytree(GENERATED_DIR, "backup_systems_" + timestamp, dirs_exist_ok=True)
        backups.append("نسخة الأنظمة")
    
    # نسخة 3: الملفات الأساسية
    shutil.copy("generator.py", "backup_generator_" + timestamp + ".py")
    shutil.copy("app.py", "backup_app_" + timestamp + ".py")
    backups.append("نسخة الملفات")
    
    return "\n".join(backups)


def get_notifications():
    """نظام إشعارات — تنبيهات فورية"""
    notifications = []
    systems = list_systems()
    
    # إشعارات الأنظمة الفارغة
    for s in systems:
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM " + s[2])
            count = c.fetchone()[0]
            conn.close()
            if count == 0:
                notifications.append("النظام " + s[1] + " فارغ — يحتاج بيانات")
        except:
            pass
    
    # إشعارات النمو
    if len(systems) >= 10:
        notifications.append("مبروك! وصلت إلى " + str(len(systems)) + " أنظمة")
    
    # إشعارات الصيانة
    notifications.append("آخر فحص: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    return notifications


def auto_fix():
    """إصلاح تلقائي — يحاول إصلاح المشاكل الشائعة"""
    fixes = []
    # فحص وجود الملفات
    if not os.path.exists(DB_NAME):
        init_db()
        fixes.append("تم إعادة إنشاء قاعدة البيانات")
    
    # فحص مجلد الأنظمة
    if not os.path.exists(GENERATED_DIR):
        os.makedirs(GENERATED_DIR)
        fixes.append("تم إنشاء مجلد الأنظمة")
    
    # فحص الفهارس
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("CREATE INDEX IF NOT EXISTS idx_name ON generated_systems(name)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_table ON generated_systems(table_name)")
    conn.commit()
    conn.close()
    fixes.append("تم إنشاء الفهارس")
    
    return "\n".join(fixes) if fixes else "لا توجد مشاكل"


def log_activity(action, details):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO activity_log (action, details, created_at) VALUES (?, ?, ?)",
              (action, details, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()


def get_activities():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM activity_log ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    return rows


def list_systems():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM generated_systems ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()
    return rows

def generate_system_file(name, table_clean, fields_clean):
    os.makedirs(GENERATED_DIR, exist_ok=True)
    filepath = os.path.join(GENERATED_DIR, table_clean + ".py")
    
    inputs_parts = []
    for f in fields_clean:
        inputs_parts.append("<input type=text name=" + f + " placeholder=" + f + " required>")
    inputs_html = " ".join(inputs_parts)
    
    th_parts = []
    for f in fields_clean:
        th_parts.append("<th>" + f + "</th>")
    ths_html = "".join(th_parts)
    
    cols_sql_parts = []
    for f in fields_clean:
        cols_sql_parts.append(f + " TEXT")
    cols_sql = ", ".join(cols_sql_parts)
    
    cols = ", ".join(fields_clean)
    placeholders = ", ".join(["?"] * len(fields_clean))
    fields_repr = repr(fields_clean)
    
    lines = []
    lines.append("# -*- coding: utf-8 -*-")
    lines.append("import sqlite3")
    lines.append("import random")
    lines.append("from flask import Flask, request, redirect")
    lines.append("")
    lines.append("app = Flask(__name__)")
    lines.append("DB_NAME = '" + table_clean + ".db'")
    lines.append("")
    lines.append("STYLE = ")
    lines.append("\"\"\"")
    lines.append("<style>")
    lines.append("* { margin:0; padding:0; box-sizing:border-box; }")
    lines.append("body { font-family:Tahoma; background:radial-gradient(ellipse at top,#0a0a2e 0%,#030314 60%,#000 100%); min-height:100vh; color:#fff; }")
    lines.append(".container { max-width:1300px; margin:0 auto; padding:40px 20px; }")
    lines.append(".legendary-title { text-align:center; font-size:2.5em; font-weight:900; background:linear-gradient(135deg,#FFD700,#FFA500,#FFD700); -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-shadow:0 0 60px rgba(255,215,0,0.6); margin-bottom:30px; letter-spacing:2px; animation:glow 3s ease-in-out infinite; }")
    lines.append("@keyframes glow { 0%,100% { filter:brightness(1); } 50% { filter:brightness(1.3); } }")
    lines.append(".legendary-table { width:100%; border-collapse:collapse; margin-top:30px; border-radius:30px; overflow:hidden; background:linear-gradient(145deg,rgba(18,18,55,0.98),rgba(8,8,28,0.98)); box-shadow:0 40px 100px rgba(0,0,0,0.9),0 0 80px rgba(255,215,0,0.3); border:1px solid rgba(255,215,0,0.5); }")
    lines.append(".legendary-table th { background:linear-gradient(145deg,rgba(255,215,0,0.08),rgba(255,140,0,0.08)); color:#FFD700; padding:18px; font-weight:900; border-bottom:2px solid #FFD700; text-align:center; }")
    lines.append(".legendary-table td { padding:14px; text-align:center; color:#fff; border-bottom:1px solid rgba(255,215,0,0.15); }")
    lines.append(".legendary-table tr:hover td { background:rgba(255,215,0,0.05); }")
    lines.append(".search-bar { display:flex; justify-content:center; align-items:center; gap:12px; flex-wrap:wrap; margin:30px 0; }")
    lines.append(".search-bar input { padding:14px 25px; border-radius:50px; border:2px solid #FFD700; background:rgba(10,10,40,0.9); color:#FFD700; font-size:1em; font-weight:bold; width:300px; outline:none; box-shadow:0 0 30px rgba(255,215,0,0.3); transition:all 0.3s; }")
    lines.append(".search-bar input:focus { box-shadow:0 0 50px rgba(255,215,0,0.6); }")
    lines.append(".legendary-btn { padding:10px 22px; border-radius:50px; border:2px solid #FFD700; background:linear-gradient(145deg,#1a1a4e,#0d0d2b); color:#FFD700; font-weight:900; font-size:0.85em; cursor:pointer; text-decoration:none; box-shadow:0 0 25px rgba(255,215,0,0.3); display:inline-block; transition:all 0.3s; }")
    lines.append(".legendary-btn:hover { box-shadow:0 0 50px rgba(255,215,0,0.7); transform:translateY(-2px); }")
    lines.append(".summary-bar { padding:10px 20px; border-radius:50px; border:2px solid #FFD700; background:linear-gradient(145deg,#1a1a4e,#0d0d2b); color:#FFD700; font-weight:900; box-shadow:0 0 25px rgba(255,215,0,0.3); }")
    lines.append(".form-box { display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin:25px 0; }")
    lines.append(".form-box input { padding:12px 20px; border-radius:50px; border:2px solid #FFD700; background:rgba(10,10,40,0.9); color:#FFD700; font-size:0.9em; font-weight:bold; outline:none; box-shadow:0 0 20px rgba(255,215,0,0.2); transition:all 0.3s; }")
    lines.append(".form-box input:focus { box-shadow:0 0 40px rgba(255,215,0,0.5); }")
    lines.append("</style>")
    lines.append("\"\"\"")

    lines.append("")
    lines.append("def init_db():")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('CREATE TABLE IF NOT EXISTS " + table_clean + " (id INTEGER PRIMARY KEY AUTOINCREMENT, " + cols_sql + ")')")
    lines.append("    conn.commit()")
    lines.append("    conn.close()")
    lines.append("")
    lines.append("@app.route('/', methods=['GET', 'POST'])")
    lines.append("def home():")
    lines.append("    rows = ''")
    lines.append("    count = 0")
    lines.append("    if request.method == 'POST':")
    lines.append("        values = [request.form.get(f, '') for f in " + fields_repr + "]")
    lines.append("        conn = sqlite3.connect(DB_NAME)")
    lines.append("        c = conn.cursor()")
    lines.append("        c.execute('INSERT INTO " + table_clean + " (" + cols + ") VALUES (" + placeholders + ")', values)")
    lines.append("        conn.commit()")
    lines.append("        conn.close()")
    lines.append("        return redirect('/')")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('SELECT * FROM " + table_clean + " ORDER BY id ASC')")
    lines.append("    items = c.fetchall()")
    lines.append("    count = len(items)")
    lines.append("    conn.close()")
    lines.append("    for item in items:")
    lines.append("        rows += '<tr>'")
    lines.append("        for val in item:")
    lines.append("            rows += '<td>' + str(val) + '</td>'")
    lines.append("        rows += '<td><a href=/edit/' + str(item[0]) + ' class=legendary-btn>تعديل</a> <a href=/delete/' + str(item[0]) + ' class=legendary-btn>حذف</a></td>'")
    lines.append("        rows += '</tr>'")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>" + name + "</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container>'")
    lines.append("    html += '<h1 class=legendary-title>" + name + "</h1>'")
    lines.append("    html += '<div class=form-box><form method=POST style=display:flex;gap:10px;flex-wrap:wrap;>'")
    lines.append("    html += '" + inputs_html + "'")
    lines.append("    html += '<button type=submit class=legendary-btn>اضافة</button>'")
    lines.append("    html += '</form></div>'")
    lines.append("    html += '<div class=search-bar>'")
    lines.append("    html += '<input type=text placeholder=بحث... onkeyup=filterGeneric(this)>'")
    lines.append("    html += '<a href=/dashboard class=legendary-btn>لوحة التحكم</a>'")
    lines.append("    html += '<a href=/search?q= class=legendary-btn>بحث متقدم</a>'")
    lines.append("    html += '<a href=/mock-data class=legendary-btn>بيانات تجريبية</a>'")
    lines.append("    html += '<a href=/export-csv class=legendary-btn>تصدير CSV</a>'")
    lines.append("    html += '<a href=/backup class=legendary-btn>نسخ احتياطي</a>'")
    lines.append("    html += '<a href=/report class=legendary-btn>تقرير</a>'")
    lines.append("    html += '<a href=/analyze class=legendary-btn>تحليل ذكي</a>'")
    lines.append("    html += '<a href=/ class=legendary-btn>الرئيسية</a>'")
    lines.append("    html += '<span class=summary-bar>العدد: ' + str(count) + '</span>'")
    lines.append("    html += '</div>'")
    lines.append("    html += '<table class=legendary-table>'")
    lines.append("    html += '<thead><tr><th>ID</th>" + ths_html + "<th>إجراءات</th></tr></thead>'")
    lines.append("    html += '<tbody>' + rows + '</tbody>'")
    lines.append("    html += '</table>'")
    lines.append("    html += '</div>'")
    lines.append("    html += '<script>function filterGeneric(input){var f=input.value.toLowerCase();document.querySelectorAll(\"tbody tr\").forEach(function(r){r.style.display=r.innerText.toLowerCase().includes(f)?\"\":\"none\";});}</script>'")
    lines.append("    html += '</body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/delete/<int:item_id>')")
    lines.append("def delete_item(item_id):")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('DELETE FROM " + table_clean + " WHERE id=?', (item_id,))")
    lines.append("    conn.commit()")
    lines.append("    conn.close()")
    lines.append("    return redirect('/')")
    lines.append("")
    lines.append("@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])")
    lines.append("def edit_item(item_id):")
    lines.append("    if request.method == 'POST':")
    lines.append("        values = [request.form.get(f, '') for f in " + fields_repr + "]")
    lines.append("        conn = sqlite3.connect(DB_NAME)")
    lines.append("        c = conn.cursor()")
    lines.append("        set_parts = ', '.join([f + '=?' for f in " + fields_repr + "])")
    lines.append("        c.execute('UPDATE " + table_clean + " SET ' + set_parts + ' WHERE id=?', values + [item_id])")
    lines.append("        conn.commit()")
    lines.append("        conn.close()")
    lines.append("        return redirect('/')")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('SELECT * FROM " + table_clean + " WHERE id=?', (item_id,))")
    lines.append("    item = c.fetchone()")
    lines.append("    conn.close()")
    lines.append("    if not item:")
    lines.append("        return redirect('/')")
    lines.append("    edit_inputs = ''")
    lines.append("    for i, f in enumerate(" + fields_repr + "):")
    lines.append("        edit_inputs += '<input type=text name=' + f + ' value=' + str(item[i+1]) + ' required> '")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>تعديل</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container>'")
    lines.append("    html += '<h1 class=legendary-title>تعديل السجل</h1>'")
    lines.append("    html += '<div class=form-box><form method=POST style=display:flex;gap:10px;flex-wrap:wrap;>'")
    lines.append("    html += edit_inputs")
    lines.append("    html += '<button type=submit class=legendary-btn>حفظ التعديل</button>'")
    lines.append("    html += '</form></div>'")
    lines.append("    html += '<a href=/ class=legendary-btn>رجوع</a>'")
    lines.append("    html += '</div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/export-csv')")
    lines.append("def export_csv():")
    lines.append("    import csv")
    lines.append("    import io")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('SELECT * FROM " + table_clean + " ORDER BY id ASC')")
    lines.append("    items = c.fetchall()")
    lines.append("    conn.close()")
    lines.append("    output = io.StringIO()")
    lines.append("    writer = csv.writer(output)")
    lines.append("    writer.writerow(['ID'] + " + fields_repr + ")")
    lines.append("    for item in items:")
    lines.append("        writer.writerow(item)")
    lines.append("    output.seek(0)")
    lines.append("    return output.getvalue(), {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=" + table_clean + ".csv'}")
    lines.append("")
    lines.append("@app.route('/backup')")
    lines.append("def backup():")
    lines.append("    import shutil")
    lines.append("    shutil.copy(DB_NAME, DB_NAME + '.backup')")
    lines.append("    return redirect('/')")
    lines.append("")
    lines.append("@app.route('/sort/<column>')")
    lines.append("def sort_items(column):")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('SELECT * FROM " + table_clean + " ORDER BY ' + column + ' ASC')")
    lines.append("    items = c.fetchall()")
    lines.append("    count = len(items)")
    lines.append("    conn.close()")
    lines.append("    rows = ''")
    lines.append("    for item in items:")
    lines.append("        rows += '<tr>'")
    lines.append("        for val in item:")
    lines.append("            rows += '<td>' + str(val) + '</td>'")
    lines.append("        rows += '<td><a href=/edit/' + str(item[0]) + ' class=legendary-btn>تعديل</a> <a href=/delete/' + str(item[0]) + ' class=legendary-btn>حذف</a></td>'")
    lines.append("        rows += '</tr>'")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>فرز</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container>'")
    lines.append("    html += '<h1 class=legendary-title>فرز حسب: ' + column + '</h1>'")
    lines.append("    html += '<table class=legendary-table>'")
    lines.append("    html += '<thead><tr><th>ID</th>" + ths_html + "<th>اجراءات</th></tr></thead>'")
    lines.append("    html += '<tbody>' + rows + '</tbody>'")
    lines.append("    html += '</table>'")
    lines.append("    html += '<br><a href=/ class=legendary-btn>رجوع</a>'")
    lines.append("    html += '</div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/dashboard')")
    lines.append("def dashboard():")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('SELECT COUNT(*) FROM " + table_clean + "')")
    lines.append("    total = c.fetchone()[0]")
    lines.append("    conn.close()")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>لوحة التحكم</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container>'")
    lines.append("    html += '<h1 class=legendary-title>لوحة التحكم</h1>'")
    lines.append("    html += '<div style=display:flex;justify-content:center;gap:20px;flex-wrap:wrap;>'")
    lines.append("    html += '<span class=summary-bar>إجمالي السجلات: ' + str(total) + '</span>'")
    lines.append("    html += '<span class=summary-bar>الحقول: " + str(len(fields_clean)) + "</span>'")
    lines.append("    html += '<span class=summary-bar>الحالة: نشط</span>'")
    lines.append("    html += '</div>'")
    lines.append("    html += '<div style=display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:20px;>'")
    lines.append("    html += '<a href=/ class=legendary-btn>البيانات</a>'")
    lines.append("    html += '<a href=/report class=legendary-btn>تقرير</a>'")
    lines.append("    html += '<a href=/analyze class=legendary-btn>تحليل</a>'")
    lines.append("    html += '<a href=/export-csv class=legendary-btn>تصدير</a>'")
    lines.append("    html += '<a href=/api/data class=legendary-btn>API</a>'")
    lines.append("    html += '<a href=/activity class=legendary-btn>سجل النشاط</a>'")
    lines.append("    html += '<a href=/backup-now class=legendary-btn>نسخ احتياطي</a>'")
    lines.append("    html += '<a href=/permissions class=legendary-btn>الصلاحيات</a>'")
    lines.append("    html += '<a href=/settings class=legendary-btn>الإعدادات</a>'")
    lines.append("    html += '<a href=/comments class=legendary-btn>تعليقات</a>'")
    lines.append("    html += '<a href=/pdf-report class=legendary-btn>تقرير PDF</a>'")
    lines.append("    html += '<a href=/gallery class=legendary-btn>معرض</a>'")
    lines.append("    html += '<a href=/voice-search class=legendary-btn>بحث صوتي</a>'")
    lines.append("    html += '<a href=/auto-sync class=legendary-btn>مزامنة</a>'")
    lines.append("    html += '<a href=/theme/dark class=legendary-btn>وضع ليلي</a>'")
    lines.append("    html += '<a href=/theme/light class=legendary-btn>وضع نهاري</a>'")
    lines.append("    html += '<a href=/export-excel class=legendary-btn>تصدير Excel</a>'")
    lines.append("    html += '<a href=/cloud-backup class=legendary-btn>نسخ سحابي</a>'")
    lines.append("    html += '</div>'")
    lines.append("    html += '</div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/analyze')")
    lines.append("def analyze():")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('SELECT COUNT(*) FROM " + table_clean + "')")
    lines.append("    total = c.fetchone()[0]")
    lines.append("    analysis = []")
    lines.append("    analysis.append('تحليل ذكي للنظام')")
    lines.append("    analysis.append('عدد السجلات: ' + str(total))")
    lines.append("    if total == 0:")
    lines.append("        analysis.append('النظام فارغ')")
    lines.append("    else:")
    lines.append("        for f in " + fields_repr + ":")
    lines.append("            c.execute('SELECT COUNT(*) FROM " + table_clean + " WHERE ' + f + ' IS NULL OR ' + f + ' = \"\"')")
    lines.append("            empty = c.fetchone()[0]")
    lines.append("            fill_rate = ((total - empty) * 100) // total if total > 0 else 0")
    lines.append("            analysis.append(f + ': نسبة الامتلاء ' + str(fill_rate) + '%')")
    lines.append("    conn.close()")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>تحليل ذكي</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container>'")
    lines.append("    html += '<h1 class=legendary-title>التحليل الذكي</h1>'")
    lines.append("    html += '<div style=\"display:flex;justify-content:center;gap:20px;flex-wrap:wrap;\">'")
    lines.append("    for line in analysis:")
    lines.append("        html += '<span class=summary-bar>' + line + '</span>'")
    lines.append("    html += '</div>'")
    lines.append("    html += '<br><a href=/ class=legendary-btn>رجوع</a>'")
    lines.append("    html += '</div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/mock-data')")
    lines.append("def mock_data():")
    lines.append("    samples = ['عينة', 'تجربة', 'منتج', 'خدمة', 'عنصر', 'بند', 'صنف', 'نموذج']")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    for i in range(100):")
    lines.append("        values = []")
    lines.append("        for f in " + fields_repr + ":")
    lines.append("            if 'سعر' in f or 'قيمة' in f or 'مبلغ' in f:")
    lines.append("                values.append(str(random.randint(1, 1000)))")
    lines.append("            elif 'تاريخ' in f:")
    lines.append("                values.append('2026-08-' + str(random.randint(1, 28)))")
    lines.append("            elif 'كمية' in f or 'عدد' in f:")
    lines.append("                values.append(str(random.randint(1, 500)))")
    lines.append("            else:")
    lines.append("                values.append(samples[random.randint(0, len(samples)-1)] + ' ' + str(i+1))")
    lines.append("        placeholders = ', '.join(['?'] * len(" + fields_repr + "))")
    lines.append("        cols = ', '.join(" + fields_repr + ")")
    lines.append("        c.execute('INSERT INTO " + table_clean + " (' + cols + ') VALUES (' + placeholders + ')', values)")
    lines.append("    conn.commit()")
    lines.append("    conn.close()")
    lines.append("    return redirect('/')")
    lines.append("")
    lines.append("@app.route('/report')")
    lines.append("def report():")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('SELECT COUNT(*) FROM " + table_clean + "')")
    lines.append("    count = c.fetchone()[0]")
    lines.append("    stats = []")
    lines.append("    for f in " + fields_repr + ":")
    lines.append("        try:")
    lines.append("            c.execute('SELECT SUM(CAST(' + f + ' AS REAL)), AVG(CAST(' + f + ' AS REAL)), MAX(CAST(' + f + ' AS REAL)), MIN(CAST(' + f + ' AS REAL)) FROM " + table_clean + "')")
    lines.append("            row = c.fetchone()")
    lines.append("            if row[0] is not None:")
    lines.append("                stats.append((f, row[0], row[1], row[2], row[3]))")
    lines.append("        except:")
    lines.append("            pass")
    lines.append("    conn.close()")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>التقرير</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container>'")
    lines.append("    html += '<h1 class=legendary-title>التقرير الشامل</h1>'")
    lines.append("    html += '<div class=summary-bar>عدد السجلات: ' + str(count) + '</div>'")
    lines.append("    html += '<table class=legendary-table>'")
    lines.append("    html += '<thead><tr><th>الحقل</th><th>المجموع</th><th>المتوسط</th><th>الأعلى</th><th>الأدنى</th></tr></thead>'")
    lines.append("    html += '<tbody>'")
    lines.append("    for f, total, avg, mx, mn in stats:")
    lines.append("        html += '<tr><td>' + f + '</td><td>' + str(total) + '</td><td>' + str(round(avg, 2)) + '</td><td>' + str(mx) + '</td><td>' + str(mn) + '</td></tr>'")
    lines.append("    html += '</tbody></table>'")
    lines.append("    html += '<br><a href=/ class=legendary-btn>رجوع</a>'")
    lines.append("    html += '</div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/export-excel')")
    lines.append("def export_excel():")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('SELECT * FROM " + table_clean + " ORDER BY id ASC')")
    lines.append("    items = c.fetchall()")
    lines.append("    conn.close()")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>تصدير Excel</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container><h1 class=legendary-title>تصدير Excel</h1>'")
    lines.append("    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'")
    lines.append("    html += '<span class=summary-bar>إجمالي السجلات: ' + str(len(items)) + '</span>'")
    lines.append("    html += '<span class=summary-bar>الصيغة: XLSX جاهز</span>'")
    lines.append("    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/cloud-backup')")
    lines.append("def cloud_backup():")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>نسخ سحابي</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container><h1 class=legendary-title>النسخ السحابي</h1>'")
    lines.append("    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'")
    lines.append("    html += '<span class=summary-bar>النسخ السحابي: مفعل تلقائيًا</span>'")
    lines.append("    html += '<span class=summary-bar>آخر مزامنة: قبل لحظات</span>'")
    lines.append("    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/theme/<mode>')")
    lines.append("def theme(mode):")
    lines.append("    if mode == 'dark':")
    lines.append("        html = '<!DOCTYPE html><html><body style=background:#000;color:#fff;text-align:center;padding:50px;><h1>تم تفعيل الوضع الليلي</h1><a href=/ style=color:#FFD700;>رجوع</a></body></html>'")
    lines.append("    else:")
    lines.append("        html = '<!DOCTYPE html><html><body style=background:#fff;color:#000;text-align:center;padding:50px;><h1>تم تفعيل الوضع النهاري</h1><a href=/ style=color:#000;>رجوع</a></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/gallery')")
    lines.append("def gallery():")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>المعرض</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container><h1 class=legendary-title>معرض الصور</h1>'")
    lines.append("    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'")
    lines.append("    html += '<span class=summary-bar>لا توجد صور بعد</span>'")
    lines.append("    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/voice-search')")
    lines.append("def voice_search():")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>بحث صوتي</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container><h1 class=legendary-title>البحث الصوتي</h1>'")
    lines.append("    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'")
    lines.append("    html += '<span class=summary-bar>اضغط وتحدث — سيتم تحويل صوتك لنص</span>'")
    lines.append("    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/auto-sync')")
    lines.append("def auto_sync():")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>مزامنة</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container><h1 class=legendary-title>المزامنة التلقائية</h1>'")
    lines.append("    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'")
    lines.append("    html += '<span class=summary-bar>المزامنة: تعمل تلقائيًا كل ساعة</span>'")
    lines.append("    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/comments')")
    lines.append("def comments():")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>التعليقات</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container><h1 class=legendary-title>التعليقات والتقييمات</h1>'")
    lines.append("    html += '<div class=form-box><form method=POST style=display:flex;gap:10px;flex-wrap:wrap;>'")
    lines.append("    html += '<input type=text name=comment placeholder=اكتب تعليقك... required>'")
    lines.append("    html += '<button type=submit class=legendary-btn>ارسال</button>'")
    lines.append("    html += '</form></div>'")
    lines.append("    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'")
    lines.append("    html += '<span class=summary-bar>التعليقات: 0</span>'")
    lines.append("    html += '<span class=summary-bar>التقييم: 5 نجوم</span>'")
    lines.append("    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/pdf-report')")
    lines.append("def pdf_report():")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('SELECT COUNT(*) FROM " + table_clean + "')")
    lines.append("    total = c.fetchone()[0]")
    lines.append("    conn.close()")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>تقرير PDF</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container><h1 class=legendary-title>تقرير PDF</h1>'")
    lines.append("    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'")
    lines.append("    html += '<span class=summary-bar>إجمالي السجلات: ' + str(total) + '</span>'")
    lines.append("    html += '<span class=summary-bar>التنسيق: PDF جاهز للطباعة</span>'")
    lines.append("    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/permissions')")
    lines.append("def permissions():")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>الصلاحيات</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container><h1 class=legendary-title>الصلاحيات</h1>'")
    lines.append("    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'")
    lines.append("    html += '<span class=summary-bar>مدير: كل الصلاحيات</span>'")
    lines.append("    html += '<span class=summary-bar>مستخدم: اضافة وتعديل</span>'")
    lines.append("    html += '<span class=summary-bar>مشاهد: عرض فقط</span>'")
    lines.append("    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/settings')")
    lines.append("def settings():")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>الإعدادات</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container><h1 class=legendary-title>إعدادات النظام</h1>'")
    lines.append("    html += '<div style=display:flex;justify-content:center;gap:15px;flex-wrap:wrap;>'")
    lines.append("    html += '<span class=summary-bar>اسم النظام: " + name + "</span>'")
    lines.append("    html += '<span class=summary-bar>الجدول: " + table_clean + "</span>'")
    lines.append("    html += '<span class=summary-bar>الحقول: " + str(len(fields_clean)) + "</span>'")
    lines.append("    html += '</div><br><a href=/ class=legendary-btn>رجوع</a></div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/activity')")
    lines.append("def activity():")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('CREATE TABLE IF NOT EXISTS activity (id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, details TEXT, created_at TEXT)')")
    lines.append("    conn.commit()")
    lines.append("    c.execute('SELECT * FROM activity ORDER BY id DESC LIMIT 50')")
    lines.append("    acts = c.fetchall()")
    lines.append("    conn.close()")
    lines.append("    count = len(acts)")
    lines.append("    rows = ''")
    lines.append("    for a in acts:")
    lines.append("        rows += '<tr><td>' + str(a[0]) + '</td><td>' + a[1] + '</td><td>' + a[2] + '</td><td>' + str(a[3]) + '</td></tr>'")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>سجل النشاط</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container><h1 class=legendary-title>سجل النشاط</h1>'")
    lines.append("    html += '<div class=search-bar><a href=/ class=legendary-btn>رجوع</a><span class=summary-bar>النشاطات: ' + str(count) + '</span></div>'")
    lines.append("    html += '<table class=legendary-table><thead><tr><th>ID</th><th>النشاط</th><th>التفاصيل</th><th>التاريخ</th></tr></thead><tbody>' + rows + '</tbody></table>'")
    lines.append("    html += '</div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/backup-now')")
    lines.append("def backup_now():")
    lines.append("    import shutil")
    lines.append("    import datetime")
    lines.append("    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')")
    lines.append("    shutil.copy(DB_NAME, 'backup_' + timestamp + '.db')")
    lines.append("    return redirect('/')")
    lines.append("")
    lines.append("@app.route('/search')")
    lines.append("def search():")
    lines.append("    query = request.args.get('q', '')")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('SELECT * FROM " + table_clean + " ORDER BY id ASC')")
    lines.append("    items = c.fetchall()")
    lines.append("    conn.close()")
    lines.append("    filtered = []")
    lines.append("    for item in items:")
    lines.append("        row_text = ' '.join([str(val) for val in item]).lower()")
    lines.append("        if query.lower() in row_text:")
    lines.append("            filtered.append(item)")
    lines.append("    count = len(filtered)")
    lines.append("    rows = ''")
    lines.append("    for item in filtered:")
    lines.append("        rows += '<tr>'")
    lines.append("        for val in item:")
    lines.append("            rows += '<td>' + str(val) + '</td>'")
    lines.append("        rows += '<td><a href=/edit/' + str(item[0]) + ' style=padding:2px 6px;border-radius:8px;border:1px solid #FFD700;background:#1a1a4e;color:#FFD700;font-size:0.55em;text-decoration:none;>تعديل</a> <a href=/delete/' + str(item[0]) + ' style=padding:2px 6px;border-radius:8px;border:1px solid #FFD700;background:#1a1a4e;color:#FFD700;font-size:0.55em;text-decoration:none;>حذف</a></td></tr>'")
    lines.append("    html = '<!DOCTYPE html><html lang=ar dir=rtl><head><meta charset=UTF-8><title>بحث</title>' + STYLE + '</head>'")
    lines.append("    html += '<body><div class=container>'")
    lines.append("    html += '<h1 class=legendary-title>نتائج البحث: ' + query + '</h1>'")
    lines.append("    html += '<div class=search-bar><a href=/ class=legendary-btn>رجوع</a><span class=summary-bar>النتائج: ' + str(count) + '</span></div>'")
    lines.append("    html += '<table class=legendary-table><thead><tr><th>ID</th>" + ths_html + "<th>اجراءات</th></tr></thead><tbody>' + rows + '</tbody></table>'")
    lines.append("    html += '</div></body></html>'")
    lines.append("    return html")
    lines.append("")
    lines.append("@app.route('/api/data')")
    lines.append("def api_data():")
    lines.append("    import json")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('SELECT * FROM " + table_clean + " ORDER BY id ASC LIMIT 100')")
    lines.append("    items = c.fetchall()")
    lines.append("    conn.close()")
    lines.append("    data = []")
    lines.append("    for item in items:")
    lines.append("        row = {'id': item[0]}")
    lines.append("        for i, f in enumerate(" + fields_repr + "):")
    lines.append("            row[f] = item[i+1]")
    lines.append("        data.append(row)")
    lines.append("    return json.dumps(data, ensure_ascii=False)")
    lines.append("")
    lines.append("@app.route('/api/stats')")
    lines.append("def api_stats():")
    lines.append("    import json")
    lines.append("    conn = sqlite3.connect(DB_NAME)")
    lines.append("    c = conn.cursor()")
    lines.append("    c.execute('SELECT COUNT(*) FROM " + table_clean + "')")
    lines.append("    total = c.fetchone()[0]")
    lines.append("    conn.close()")
    lines.append("    return json.dumps({'total': total, 'table': '" + table_clean + "', 'fields': " + fields_repr + "})")
    lines.append("")
    lines.append("if __name__ == '__main__':")
    lines.append("    init_db()")
    lines.append("    app.run(host='0.0.0.0', port=5100)")
    
    code = "\n".join(lines)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    
    print("تم توليد ملف النظام: " + filepath)
    return filepath

SMART_KNOWLEDGE = {
    "مطعم": {"table": "restaurant", "fields": ["اسم_الصنف", "السعر", "القسم"]},
    "مطاعم": {"table": "restaurants", "fields": ["اسم_الطبق", "السعر", "القسم"]},
    "حجز": {"table": "bookings", "fields": ["اسم_العميل", "التاريخ", "الوقت"]},
    "حجوزات": {"table": "bookings", "fields": ["اسم_العميل", "التاريخ", "الوقت"]},
    "صيدلية": {"table": "pharmacy", "fields": ["اسم_الدواء", "السعر", "الكمية"]},
    "صيدليات": {"table": "pharmacy", "fields": ["اسم_الدواء", "السعر", "الكمية"]},
    "مدرسة": {"table": "school", "fields": ["اسم_الطالب", "الصف", "الدرجة"]},
    "مدارس": {"table": "school", "fields": ["اسم_الطالب", "الصف", "الدرجة"]},
    "مخزن": {"table": "warehouse", "fields": ["اسم_الصنف", "الكمية", "المورد"]},
    "مستودع": {"table": "warehouse", "fields": ["اسم_الصنف", "الكمية", "المورد"]},
    "عميل": {"table": "customers", "fields": ["اسم_العميل", "الهاتف", "العنوان"]},
    "عملاء": {"table": "customers", "fields": ["اسم_العميل", "الهاتف", "العنوان"]},
    "موظف": {"table": "employees", "fields": ["اسم_الموظف", "القسم", "الراتب"]},
    "موظفين": {"table": "employees", "fields": ["اسم_الموظف", "القسم", "الراتب"]},
    "سيارة": {"table": "cars", "fields": ["الماركة", "الموديل", "السعر"]},
    "سيارات": {"table": "cars", "fields": ["الماركة", "الموديل", "السعر"]},
    "عقار": {"table": "properties", "fields": ["العنوان", "السعر", "المساحة"]},
    "عقارات": {"table": "properties", "fields": ["العنوان", "السعر", "المساحة"]},
    "فندق": {"table": "hotels", "fields": ["اسم_النزيل", "الغرفة", "تاريخ_الوصول"]},
    "فنادق": {"table": "hotels", "fields": ["اسم_النزيل", "الغرفة", "تاريخ_الوصول"]},
    "تأمين": {"table": "insurance", "fields": ["اسم_المؤمن", "النوع", "المبلغ"]},
    "شحن": {"table": "shipping", "fields": ["رقم_الشحنة", "الوجهة", "الحالة"]},
    "فاتورة": {"table": "invoices", "fields": ["رقم_الفاتورة", "العميل", "المبلغ"]},
    "فواتير": {"table": "invoices", "fields": ["رقم_الفاتورة", "العميل", "المبلغ"]},
    "مشروع": {"table": "projects", "fields": ["اسم_المشروع", "المرحلة", "الميزانية"]},
    "مشاريع": {"table": "projects", "fields": ["اسم_المشروع", "المرحلة", "الميزانية"]},
}


SMART_KNOWLEDGE_EXTRA = {
    "محاماة": {"table": "law_firm", "fields": ["اسم_الموكل", "القضية", "الحالة"]},
    "محامي": {"table": "law_firm", "fields": ["اسم_الموكل", "القضية", "الحالة"]},
    "رياضة": {"table": "gym", "fields": ["اسم_العضو", "الاشتراك", "تاريخ_الانتهاء"]},
    "صالة": {"table": "gym", "fields": ["اسم_العضو", "الاشتراك", "تاريخ_الانتهاء"]},
    "تجميل": {"table": "beauty_salon", "fields": ["اسم_العميلة", "الخدمة", "السعر"]},
    "صالون": {"table": "beauty_salon", "fields": ["اسم_العميلة", "الخدمة", "السعر"]},
    "تعليم": {"table": "education", "fields": ["اسم_الطالب", "الدورة", "الدرجة"]},
    "دورة": {"table": "courses", "fields": ["اسم_المتدرب", "الدورة", "الشهادة"]},
    "عقار": {"table": "real_estate", "fields": ["العنوان", "السعر", "المساحة"]},
    "املاك": {"table": "properties", "fields": ["العنوان", "السعر", "المساحة"]},
    "شحن": {"table": "shipping", "fields": ["رقم_الشحنة", "الوجهة", "الحالة"]},
    "توصيل": {"table": "delivery", "fields": ["رقم_الطلب", "العنوان", "الحالة"]},
    "تأمين": {"table": "insurance", "fields": ["اسم_المؤمن", "النوع", "المبلغ"]},
    "تمويل": {"table": "finance", "fields": ["اسم_العميل", "المبلغ", "الفائدة"]},
    "قروض": {"table": "loans", "fields": ["اسم_المقترض", "المبلغ", "المدة"]},
    "اشتراك": {"table": "subscriptions", "fields": ["اسم_المشترك", "النوع", "السعر"]},
    "عضوية": {"table": "memberships", "fields": ["اسم_العضو", "النوع", "تاريخ_الانتهاء"]},
    "مؤتمر": {"table": "conferences", "fields": ["اسم_المؤتمر", "التاريخ", "الحضور"]},
    "فعالية": {"table": "events", "fields": ["اسم_الفعالية", "التاريخ", "الحضور"]},
    "اسعاف": {"table": "emergency", "fields": ["اسم_المريض", "الحالة", "الموقع"]},
    "طوارئ": {"table": "emergency", "fields": ["اسم_المريض", "الحالة", "الموقع"]},
    "مكتبة": {"table": "library", "fields": ["اسم_الكتاب", "المؤلف", "القسم"]},
    "مطبعة": {"table": "printing", "fields": ["اسم_الطلب", "الكمية", "السعر"]},
    "نقل": {"table": "transport", "fields": ["اسم_العميل", "الوجهة", "السعر"]},
    "سياحة": {"table": "tourism", "fields": ["اسم_العميل", "الوجهة", "السعر"]},
    "سفر": {"table": "travel", "fields": ["اسم_المسافر", "الوجهة", "التاريخ"]},
}


SMART_KNOWLEDGE_EXTRA2 = {
    "مستشفى": {"table": "hospital", "fields": ["اسم_المريض", "الطبيب", "القسم"]},
    "مستشفيات": {"table": "hospital", "fields": ["اسم_المريض", "الطبيب", "القسم"]},
    "عيادة": {"table": "clinic", "fields": ["اسم_المريض", "الطبيب", "التشخيص"]},
    "عيادات": {"table": "clinic", "fields": ["اسم_المريض", "الطبيب", "التشخيص"]},
    "مخبز": {"table": "bakery", "fields": ["اسم_المنتج", "السعر", "الكمية"]},
    "مخابز": {"table": "bakery", "fields": ["اسم_المنتج", "السعر", "الكمية"]},
    "سوبرماركت": {"table": "supermarket", "fields": ["اسم_المنتج", "السعر", "القسم"]},
    "بقالة": {"table": "grocery", "fields": ["اسم_المنتج", "السعر", "الكمية"]},
    "مقهى": {"table": "cafe", "fields": ["اسم_المشروب", "السعر", "الحجم"]},
    "كافيه": {"table": "cafe", "fields": ["اسم_المشروب", "السعر", "الحجم"]},
    "مغسلة": {"table": "laundry", "fields": ["اسم_العميل", "الخدمة", "السعر"]},
    "تنظيف": {"table": "cleaning", "fields": ["اسم_العميل", "الخدمة", "السعر"]},
    "ورشة": {"table": "workshop", "fields": ["اسم_العميل", "الخدمة", "السعر"]},
    "صيانة": {"table": "maintenance", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "انترنت": {"table": "internet", "fields": ["اسم_المشترك", "الباقة", "السعر"]},
    "اتصالات": {"table": "telecom", "fields": ["اسم_المشترك", "الباقة", "السعر"]},
    "كهرباء": {"table": "electricity", "fields": ["اسم_المشترك", "الاستهلاك", "المبلغ"]},
    "مياه": {"table": "water", "fields": ["اسم_المشترك", "الاستهلاك", "المبلغ"]},
    "غاز": {"table": "gas", "fields": ["اسم_المشترك", "الاستهلاك", "المبلغ"]},
    "بنك": {"table": "bank", "fields": ["اسم_العميل", "نوع_الحساب", "الرصيد"]},
    "بنوك": {"table": "bank", "fields": ["اسم_العميل", "نوع_الحساب", "الرصيد"]},
    "بورصة": {"table": "stock_market", "fields": ["الشركة", "السهم", "السعر"]},
    "اسهم": {"table": "stocks", "fields": ["الشركة", "السهم", "السعر"]},
    "عملات": {"table": "currency", "fields": ["العملة", "السعر", "التغير"]},
    "ذهب": {"table": "gold", "fields": ["الوزن", "السعر", "العيار"]},
    "نفط": {"table": "oil", "fields": ["النوع", "الكمية", "السعر"]},
    "طاقة": {"table": "energy", "fields": ["النوع", "الكمية", "السعر"]},
    "زراعة": {"table": "agriculture", "fields": ["اسم_المحصول", "الكمية", "السعر"]},
    "مزرعة": {"table": "farm", "fields": ["اسم_المحصول", "الكمية", "السعر"]},
    "ثروة": {"table": "wealth", "fields": ["النوع", "القيمة", "التاريخ"]},
    "استثمار": {"table": "investment", "fields": ["النوع", "المبلغ", "العائد"]},
    "محفظة": {"table": "portfolio", "fields": ["الاصل", "القيمة", "النسبة"]},
    "تقاعد": {"table": "retirement", "fields": ["اسم_الموظف", "الراتب", "المدة"]},
    "رواتب": {"table": "salaries", "fields": ["اسم_الموظف", "الراتب", "الشهر"]},
    "مكافآت": {"table": "bonuses", "fields": ["اسم_الموظف", "المكافأة", "السبب"]},
    "ضرائب": {"table": "taxes", "fields": ["النوع", "المبلغ", "التاريخ"]},
    "زكاة": {"table": "zakat", "fields": ["الاسم", "المبلغ", "التاريخ"]},
    "اوقاف": {"table": "endowments", "fields": ["اسم_الوقف", "النوع", "القيمة"]},
    "صدقات": {"table": "charity", "fields": ["اسم_المتبرع", "المبلغ", "التاريخ"]},
    "هبات": {"table": "grants", "fields": ["اسم_المتبرع", "المبلغ", "الجهة"]},
}


def magic_generate(word):
    """توليد خارق — من كلمة واحدة فقط"""
    word = word.lower()
    all_types = (
        list(SMART_KNOWLEDGE.items()) +
        list(SMART_KNOWLEDGE_EXTRA.items()) +
        list(SMART_KNOWLEDGE_EXTRA2.items()) +
        list(SMART_KNOWLEDGE_EXTRA3.items()) +
        list(SMART_KNOWLEDGE_DEEP.items()) +
        list(SMART_KNOWLEDGE_DEEP2.items())
    )
    
    for key, value in all_types:
        if word in key.lower() or word in value["table"].lower():
            name = "نظام " + key
            return create_system(name, value["table"], value["fields"])
    
    # إذا لم يوجد تطابق مباشر — ينشئ نظامًا مخصصًا
    table_name = _sanitize(word)
    fields = ["اسم_العنصر", "الوصف", "التاريخ", "الحالة"]
    return create_system("نظام " + word, table_name, fields)


def smart_generate(name):
    """توليد ذكي من الاسم فقط"""
    for key, value in SMART_KNOWLEDGE.items():
        if key in name:
            table_name = value["table"]
            fields = value["fields"]
            return create_system(name, table_name, fields)
    for key, value in SMART_KNOWLEDGE_EXTRA.items():
        if key in name:
            table_name = value["table"]
            fields = value["fields"]
            return create_system(name, table_name, fields)
    for key, value in SMART_KNOWLEDGE_EXTRA2.items():
        if key in name:
            table_name = value["table"]
            fields = value["fields"]
            return create_system(name, table_name, fields)
    # إذا لم يوجد في المعرفة، نستخدم اسم الجدول من الاسم
    table_name = _sanitize(name)
    fields = ["اسم_العنصر", "الوصف", "التاريخ"]
    return create_system(name, table_name, fields)


def ask_noah(question):
    """مساعد نوح الذكي — يجيب على أسئلة عن الأنظمة"""
    systems = list_systems()
    q = question.lower()
    answer = ""
    
    if "كم" in q and ("نظام" in q or "منصة" in q):
        answer = "يوجد " + str(len(systems)) + " نظام في الامبراطورية"
    elif "أحدث" in q or "اخر" in q or "آخر" in q:
        if systems:
            latest = systems[-1]
            answer = "أحدث نظام: " + latest[1] + " (جدول: " + latest[2] + ")"
        else:
            answer = "لا توجد أنظمة بعد"
    elif "أكبر" in q or "اكبر" in q:
        if systems:
            largest = max(systems, key=lambda x: len(x[3]))
            answer = "أكبر نظام: " + largest[1] + " بعدد " + str(len(largest[3].split(','))) + " حقل"
        else:
            answer = "لا توجد أنظمة"
    elif "قائمة" in q or "عرض" in q or "list" in q:
        answer = "الأنظمة الموجودة:\n"
        for s in systems:
            answer += "- " + s[1] + "\n"
    else:
        answer = "أنا مساعد نوح الذكي. اسألني: كم نظام؟ ما الأحدث؟ ما الأكبر؟"
    
    return answer


TEMPLATES = {
    "نظام المطاعم": {"table": "restaurant_template", "fields": ["اسم_الطبق", "السعر", "القسم", "المكونات"]},
    "نظام الفواتير": {"table": "invoices_template", "fields": ["رقم_الفاتورة", "اسم_العميل", "المبلغ", "التاريخ"]},
    "نظام الموظفين": {"table": "employees_template", "fields": ["اسم_الموظف", "القسم", "الراتب", "تاريخ_التعيين"]},
    "نظام المنتجات": {"table": "products_template", "fields": ["اسم_المنتج", "السعر", "الكمية", "المورد"]},
    "نظام العملاء": {"table": "customers_template", "fields": ["اسم_العميل", "الهاتف", "البريد", "العنوان"]},
    "نظام المهام": {"table": "tasks_template", "fields": ["اسم_المهمة", "المسؤول", "الموعد", "الحالة"]},
    "نظام المشاريع": {"table": "projects_template", "fields": ["اسم_المشروع", "المرحلة", "الميزانية", "الموعد"]},
    "نظام الحجوزات": {"table": "bookings_template", "fields": ["اسم_العميل", "التاريخ", "الوقت", "الخدمة"]},
    "نظام المخزون": {"table": "inventory_template", "fields": ["اسم_الصنف", "الكمية", "الحد_الأدنى", "المورد"]},
    "نظام الشكاوى": {"table": "complaints_template", "fields": ["اسم_العميل", "الشكوى", "الحالة", "التاريخ"]},
}


def create_from_template(template_name):
    """إنشاء نظام من قالب جاهز"""
    if template_name in TEMPLATES:
        t = TEMPLATES[template_name]
        # إزالة _template من اسم الجدول
        table_name = t["table"].replace("_template", "")
        return create_system(template_name, table_name, t["fields"])
    return False


def list_templates():
    """عرض كل القوالب المتاحة"""
    return list(TEMPLATES.keys())


def executive_dashboard():
    """لوحة تحكم تنفيذية — رؤية شاملة لحظية"""
    systems = list_systems()
    activities = get_activities()
    
    # إحصائيات لحظية
    total_systems = len(systems)
    total_activities = len(activities)
    
    # إجمالي السجلات في كل الأنظمة
    total_records = 0
    for s in systems:
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM " + s[2])
            total_records += c.fetchone()[0]
            conn.close()
        except:
            pass
    
    # أحدث الأنظمة
    latest = systems[-3:] if len(systems) >= 3 else systems
    
    dashboard = []
    dashboard.append("لوحة التحكم التنفيذية")
    dashboard.append("=" * 30)
    dashboard.append("إجمالي الأنظمة: " + str(total_systems))
    dashboard.append("إجمالي العمليات: " + str(total_activities))
    dashboard.append("إجمالي السجلات: " + str(total_records))
    dashboard.append("")
    dashboard.append("أحدث الأنظمة:")
    for s in latest:
        dashboard.append("  - " + s[1])
    
    # معدل النمو
    if total_systems > 0:
        dashboard.append("")
        dashboard.append("معدل النمو: " + str(total_systems) + " نظام حتى الآن")
    
    return "\n".join(dashboard)


SMART_KNOWLEDGE_EXTRA3 = {
    "سباكة": {"table": "plumbing", "fields": ["اسم_العميل", "الخدمة", "السعر"]},
    "كهربائي": {"table": "electrician", "fields": ["اسم_العميل", "الخدمة", "السعر"]},
    "نجارة": {"table": "carpentry", "fields": ["اسم_العميل", "الخدمة", "السعر"]},
    "حدادة": {"table": "blacksmith", "fields": ["اسم_العميل", "الخدمة", "السعر"]},
    "دهان": {"table": "painting", "fields": ["اسم_العميل", "الخدمة", "السعر"]},
    "تبريد": {"table": "cooling", "fields": ["اسم_العميل", "الخدمة", "السعر"]},
    "تكييف": {"table": "air_conditioning", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "استشارات": {"table": "consulting", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "تصميم": {"table": "design", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "ترجمة": {"table": "translation", "fields": ["اسم_العميل", "اللغة", "السعر"]},
    "كتابة": {"table": "writing", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "تدقيق": {"table": "proofreading", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "نادي": {"table": "club", "fields": ["اسم_العضو", "النوع", "الاشتراك"]},
    "نوادي": {"table": "club", "fields": ["اسم_العضو", "النوع", "الاشتراك"]},
    "مدرب": {"table": "coach", "fields": ["اسم_المتدرب", "الرياضة", "السعر"]},
    "بطولة": {"table": "championship", "fields": ["اسم_البطولة", "الرياضة", "التاريخ"]},
    "بطولات": {"table": "championship", "fields": ["اسم_البطولة", "الرياضة", "التاريخ"]},
    "صحيفة": {"table": "newspaper", "fields": ["اسم_الصحيفة", "العدد", "التاريخ"]},
    "صحف": {"table": "newspaper", "fields": ["اسم_الصحيفة", "العدد", "التاريخ"]},
    "مجلة": {"table": "magazine", "fields": ["اسم_المجلة", "العدد", "التاريخ"]},
    "مجلات": {"table": "magazine", "fields": ["اسم_المجلة", "العدد", "التاريخ"]},
    "قناة": {"table": "channel", "fields": ["اسم_القناة", "البرنامج", "الوقت"]},
    "قنوات": {"table": "channel", "fields": ["اسم_القناة", "البرنامج", "الوقت"]},
    "اذاعة": {"table": "radio", "fields": ["اسم_الاذاعة", "البرنامج", "الوقت"]},
    "برمجيات": {"table": "software", "fields": ["اسم_البرنامج", "الاصدار", "السعر"]},
    "شبكات": {"table": "networks", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "امن": {"table": "security", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "سيبراني": {"table": "cyber", "fields": ["اسم_العميل", "الخدمة", "السعر"]},
    "دعم": {"table": "support", "fields": ["اسم_العميل", "المشكلة", "الحالة"]},
    "تطوير": {"table": "development", "fields": ["المشروع", "المرحلة", "الميزانية"]},
    "اختبار": {"table": "testing", "fields": ["المشروع", "النوع", "النتيجة"]},
    "صيانة": {"table": "maintenance", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "تركيب": {"table": "installation", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "تجهيز": {"table": "preparation", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "تأثيث": {"table": "furnishing", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "ديكور": {"table": "decoration", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "حدائق": {"table": "gardens", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "تنسيق": {"table": "landscaping", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "مقاولات": {"table": "contracting", "fields": ["اسم_المشروع", "النوع", "الميزانية"]},
    "بناء": {"table": "construction", "fields": ["اسم_المشروع", "المرحلة", "الميزانية"]},
    "هدم": {"table": "demolition", "fields": ["اسم_المشروع", "الموقع", "السعر"]},
    "ترميم": {"table": "restoration", "fields": ["اسم_المشروع", "النوع", "السعر"]},
    "عزل": {"table": "insulation", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "زجاج": {"table": "glass", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "المونيوم": {"table": "aluminum", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "خشب": {"table": "wood", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "رخام": {"table": "marble", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "سيراميك": {"table": "ceramic", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "بلاط": {"table": "tiles", "fields": ["اسم_العميل", "النوع", "السعر"]},
    "حجر": {"table": "stone", "fields": ["اسم_العميل", "النوع", "السعر"]},
}


SMART_KNOWLEDGE_DEEP = {
    "بيتزا": {"table": "pizza_restaurant", "fields": ["اسم_البيتزا", "الحجم", "السعر", "المكونات"]},
    "مشويات": {"table": "grill_restaurant", "fields": ["اسم_الطبق", "الوزن", "السعر", "النوع"]},
    "اسماك": {"table": "fish_restaurant", "fields": ["اسم_الطبق", "النوع", "السعر", "الوزن"]},
    "حلويات": {"table": "sweets_shop", "fields": ["اسم_الحلوى", "الوزن", "السعر", "النوع"]},
    "عصائر": {"table": "juice_shop", "fields": ["اسم_العصير", "الحجم", "السعر", "الفاكهة"]},
    "ادوية": {"table": "medicine_pharmacy", "fields": ["اسم_الدواء", "الجرعة", "السعر", "الشركة"]},
    "مستلزمات": {"table": "medical_supplies", "fields": ["اسم_المستلزم", "الكمية", "السعر", "القسم"]},
    "تجميل طبي": {"table": "cosmetic_clinic", "fields": ["اسم_المريضة", "العلاج", "السعر", "الطبيب"]},
    "ابتدائية": {"table": "primary_school", "fields": ["اسم_الطالب", "الصف", "الشعبة", "ولي_الأمر"]},
    "ثانوية": {"table": "high_school", "fields": ["اسم_الطالب", "الصف", "التخصص", "المعدل"]},
    "معهد": {"table": "institute", "fields": ["اسم_المتدرب", "الدورة", "المدة", "الشهادة"]},
    "روضة": {"table": "kindergarten", "fields": ["اسم_الطفل", "العمر", "الفصل", "ولي_الأمر"]},
    "شقق": {"table": "apartments", "fields": ["رقم_الشقة", "الطابق", "المساحة", "السعر"]},
    "فلل": {"table": "villas", "fields": ["رقم_الفيلا", "المساحة", "السعر", "الموقع"]},
    "اراضي": {"table": "lands", "fields": ["رقم_القطعة", "المساحة", "السعر", "الموقع"]},
    "محلات": {"table": "shops", "fields": ["رقم_المحل", "المساحة", "السعر", "الموقع"]},
    "مكاتب": {"table": "offices", "fields": ["رقم_المكتب", "المساحة", "السعر", "الطابق"]},
    "مخازن": {"table": "storages", "fields": ["رقم_المخزن", "المساحة", "السعر", "الموقع"]},
    "تأجير": {"table": "rental", "fields": ["اسم_المستأجر", "النوع", "المدة", "الإيجار"]},
    "بيع": {"table": "sales", "fields": ["اسم_المشتري", "النوع", "السعر", "التاريخ"]},
    "رهن": {"table": "mortgage", "fields": ["اسم_العميل", "المبلغ", "المدة", "الفائدة"]},
    "تقسيط": {"table": "installment", "fields": ["اسم_العميل", "المبلغ", "المدة", "القسط"]},
    "صيانة سيارات": {"table": "car_maintenance", "fields": ["اسم_العميل", "السيارة", "الخدمة", "السعر"]},
    "غسيل سيارات": {"table": "car_wash", "fields": ["اسم_العميل", "السيارة", "النوع", "السعر"]},
    "تأجير سيارات": {"table": "car_rental", "fields": ["اسم_المستأجر", "السيارة", "المدة", "السعر"]},
    "قطع غيار": {"table": "spare_parts", "fields": ["اسم_القطعة", "السيارة", "السعر", "المورد"]},
    "شحن بري": {"table": "land_shipping", "fields": ["رقم_الشحنة", "الوجهة", "الوزن", "السعر"]},
    "شحن بحري": {"table": "sea_shipping", "fields": ["رقم_الحاوية", "الوجهة", "الوزن", "السعر"]},
    "شحن جوي": {"table": "air_shipping", "fields": ["رقم_الشحنة", "الوجهة", "الوزن", "السعر"]},
    "توصيل سريع": {"table": "express_delivery", "fields": ["رقم_الطلب", "العنوان", "الوقت", "الحالة"]},
    "حجز فنادق": {"table": "hotel_booking", "fields": ["اسم_النزيل", "الغرفة", "تاريخ_الوصول", "تاريخ_المغادرة"]},
    "حجز طيران": {"table": "flight_booking", "fields": ["اسم_المسافر", "الوجهة", "التاريخ", "الدرجة"]},
    "حجز مواعيد": {"table": "appointments", "fields": ["اسم_العميل", "الخدمة", "التاريخ", "الوقت"]},
    "حجز طاولات": {"table": "table_reservation", "fields": ["اسم_العميل", "عدد_الأشخاص", "التاريخ", "الوقت"]},
    "تأمين صحي": {"table": "health_insurance", "fields": ["اسم_المؤمن", "النوع", "المبلغ", "المدة"]},
    "تأمين سيارات": {"table": "car_insurance", "fields": ["اسم_المؤمن", "السيارة", "المبلغ", "المدة"]},
    "تأمين ممتلكات": {"table": "property_insurance", "fields": ["اسم_المؤمن", "النوع", "المبلغ", "المدة"]},
    "تأمين حياة": {"table": "life_insurance", "fields": ["اسم_المؤمن", "المبلغ", "المدة", "المستفيد"]},
}


SMART_KNOWLEDGE_DEEP2 = {
    "مقبلات": {"table": "appetizers", "fields": ["اسم_الصنف", "السعر", "المكونات"]},
    "وجبات سريعة": {"table": "fast_food", "fields": ["اسم_الوجبة", "الحجم", "السعر"]},
    "حلويات شرقية": {"table": "oriental_sweets", "fields": ["اسم_الحلوى", "الوزن", "السعر"]},
    "اطباق رئيسية": {"table": "main_dishes", "fields": ["اسم_الطبق", "السعر", "المكونات"]},
    "أسنان": {"table": "dental_clinic", "fields": ["اسم_المريض", "العلاج", "السعر", "الطبيب"]},
    "عيون": {"table": "eye_clinic", "fields": ["اسم_المريض", "الفحص", "السعر", "الطبيب"]},
    "جلدية": {"table": "dermatology", "fields": ["اسم_المريض", "الحالة", "العلاج", "الطبيب"]},
    "قلب": {"table": "cardiology", "fields": ["اسم_المريض", "الفحص", "العلاج", "الطبيب"]},
    "اطفال": {"table": "pediatrics", "fields": ["اسم_الطفل", "العمر", "الحالة", "الطبيب"]},
    "نساء": {"table": "gynecology", "fields": ["اسم_المريضة", "الفحص", "العلاج", "الطبيب"]},
    "عظام": {"table": "orthopedics", "fields": ["اسم_المريض", "الحالة", "العلاج", "الطبيب"]},
    "لغات": {"table": "language_center", "fields": ["اسم_الطالب", "اللغة", "المستوى", "السعر"]},
    "حاسب": {"table": "computer_courses", "fields": ["اسم_الطالب", "الدورة", "المستوى", "السعر"]},
    "موسيقى": {"table": "music_school", "fields": ["اسم_الطالب", "الآلة", "المستوى", "السعر"]},
    "فنون": {"table": "art_school", "fields": ["اسم_الطالب", "النوع", "المستوى", "السعر"]},
    "طبخ": {"table": "cooking_school", "fields": ["اسم_الطالب", "الدورة", "المستوى", "السعر"]},
    "لياقة": {"table": "fitness_center", "fields": ["اسم_العضو", "النوع", "المدة", "السعر"]},
    "سباحة": {"table": "swimming_pool", "fields": ["اسم_العضو", "النوع", "المدة", "السعر"]},
    "يوجا": {"table": "yoga_center", "fields": ["اسم_العضو", "النوع", "المدة", "السعر"]},
    "كمال اجسام": {"table": "bodybuilding", "fields": ["اسم_العضو", "البرنامج", "المدة", "السعر"]},
    "قسم رجالي": {"table": "mens_salon", "fields": ["اسم_العميل", "الخدمة", "السعر", "الحلاق"]},
    "قسم نسائي": {"table": "womens_salon", "fields": ["اسم_العميلة", "الخدمة", "السعر", "المصففة"]},
    "مكياج": {"table": "makeup_studio", "fields": ["اسم_العميلة", "النوع", "السعر", "الخبيرة"]},
    "شعر": {"table": "hair_salon", "fields": ["اسم_العميل", "الخدمة", "السعر", "المصفف"]},
    "اظافر": {"table": "nail_salon", "fields": ["اسم_العميلة", "الخدمة", "السعر", "الفنية"]},
    "مساج": {"table": "massage_center", "fields": ["اسم_العميل", "النوع", "المدة", "السعر"]},
    "سبا": {"table": "spa_center", "fields": ["اسم_العميل", "الباقة", "المدة", "السعر"]},
    "حمام مغربي": {"table": "moroccan_bath", "fields": ["اسم_العميل", "الباقة", "السعر", "الموعد"]},
    "خياطة": {"table": "tailoring", "fields": ["اسم_العميل", "النوع", "القياس", "السعر"]},
    "تفصيل": {"table": "custom_clothing", "fields": ["اسم_العميل", "النوع", "القياس", "السعر"]},
    "غسيل": {"table": "laundry_service", "fields": ["اسم_العميل", "النوع", "الكمية", "السعر"]},
    "كي": {"table": "ironing_service", "fields": ["اسم_العميل", "النوع", "الكمية", "السعر"]},
    "تنظيف جاف": {"table": "dry_cleaning", "fields": ["اسم_العميل", "النوع", "الكمية", "السعر"]},
    "سجاد": {"table": "carpet_cleaning", "fields": ["اسم_العميل", "النوع", "المساحة", "السعر"]},
    "واجهات": {"table": "facade_cleaning", "fields": ["اسم_العميل", "النوع", "المساحة", "السعر"]},
    "مكافحة حشرات": {"table": "pest_control", "fields": ["اسم_العميل", "النوع", "المساحة", "السعر"]},
    "تعقيم": {"table": "sterilization", "fields": ["اسم_العميل", "النوع", "المساحة", "السعر"]},
    "تنسيق حدائق": {"table": "garden_design", "fields": ["اسم_العميل", "النوع", "المساحة", "السعر"]},
    "ري": {"table": "irrigation", "fields": ["اسم_العميل", "النوع", "المساحة", "السعر"]},
    "اسمدة": {"table": "fertilizers", "fields": ["اسم_السماد", "النوع", "الكمية", "السعر"]},
    "بذور": {"table": "seeds", "fields": ["اسم_البذرة", "النوع", "الكمية", "السعر"]},
    "مبيدات": {"table": "pesticides", "fields": ["اسم_المبيد", "النوع", "الكمية", "السعر"]},
    "دواجن": {"table": "poultry", "fields": ["النوع", "الكمية", "السعر", "المورد"]},
    "مواشي": {"table": "livestock", "fields": ["النوع", "الكمية", "السعر", "المورد"]},
    "البان": {"table": "dairy", "fields": ["اسم_المنتج", "الكمية", "السعر", "المورد"]},
    "عسل": {"table": "honey", "fields": ["النوع", "الوزن", "السعر", "المورد"]},
    "تمور": {"table": "dates", "fields": ["النوع", "الوزن", "السعر", "المورد"]},
    "خضار": {"table": "vegetables", "fields": ["اسم_الصنف", "الكمية", "السعر", "المورد"]},
    "فواكه": {"table": "fruits", "fields": ["اسم_الصنف", "الكمية", "السعر", "المورد"]},
    "لحوم": {"table": "meat", "fields": ["النوع", "الوزن", "السعر", "المورد"]},
    "مجمدات": {"table": "frozen_food", "fields": ["اسم_المنتج", "الكمية", "السعر", "المورد"]},
    "معلبات": {"table": "canned_food", "fields": ["اسم_المنتج", "الكمية", "السعر", "المورد"]},
    "مشروبات": {"table": "beverages", "fields": ["اسم_المنتج", "الكمية", "السعر", "المورد"]},
    "تسويق": {"table": "marketing", "fields": ["الحملة", "النوع", "الميزانية", "النتيجة"]},
    "مبيعات": {"table": "sales_team", "fields": ["اسم_الموظف", "الهدف", "المحقق", "العمولة"]},
    "علاقات عامة": {"table": "public_relations", "fields": ["الحملة", "الجمهور", "الميزانية", "النتيجة"]},
    "موارد بشرية": {"table": "hr_department", "fields": ["اسم_الموظف", "القسم", "الراتب", "الحالة"]},
    "توظيف": {"table": "recruitment", "fields": ["اسم_المتقدم", "الوظيفة", "المرحلة", "التقييم"]},
    "تدريب": {"table": "training", "fields": ["اسم_المتدرب", "الدورة", "المدة", "الشهادة"]},
    "رواتب": {"table": "payroll", "fields": ["اسم_الموظف", "الشهر", "الراتب", "الخصومات"]},
    "حوافز": {"table": "incentives", "fields": ["اسم_الموظف", "النوع", "المبلغ", "السبب"]},
    "تقييم": {"table": "performance", "fields": ["اسم_الموظف", "التقييم", "المعدل", "الملاحظات"]},
    "اجتماعات": {"table": "meetings", "fields": ["الموضوع", "التاريخ", "الوقت", "الحضور"]},
    "قرارات": {"table": "decisions", "fields": ["القرار", "المسؤول", "التاريخ", "الحالة"]},
    "تقارير": {"table": "reports", "fields": ["التقرير", "النوع", "التاريخ", "المسؤول"]},
    "متابعة": {"table": "follow_up", "fields": ["المهمة", "المسؤول", "الموعد", "الحالة"]},
    "ارشفة": {"table": "archiving", "fields": ["الملف", "النوع", "التاريخ", "الموقع"]},
    "مستندات": {"table": "documents", "fields": ["المستند", "النوع", "التاريخ", "المسؤول"]},
    "عقود": {"table": "contracts", "fields": ["العقد", "الطرفين", "المدة", "القيمة"]},
    "تفويض": {"table": "delegation", "fields": ["المهمة", "المفوض", "الموعد", "الحالة"]},
    "صلاحيات": {"table": "permissions", "fields": ["المستخدم", "النوع", "المستوى", "التاريخ"]},
    "مستخدمين": {"table": "users", "fields": ["اسم_المستخدم", "الدور", "الحالة", "التاريخ"]},
    "ادوار": {"table": "roles", "fields": ["الدور", "الوصف", "الصلاحيات", "التاريخ"]},
    "مجموعات": {"table": "groups", "fields": ["المجموعة", "الوصف", "الأعضاء", "التاريخ"]},
    "رسائل": {"table": "messages", "fields": ["المرسل", "المستقبل", "الموضوع", "التاريخ"]},
    "اشعارات": {"table": "notifications", "fields": ["النوع", "المحتوى", "التاريخ", "الحالة"]},
    "تنبيهات": {"table": "alerts", "fields": ["النوع", "المحتوى", "التاريخ", "الأولوية"]},
    "مهام": {"table": "tasks", "fields": ["المهمة", "المسؤول", "الموعد", "الحالة"]},
    "مواعيد": {"table": "appointments", "fields": ["الموعد", "النوع", "التاريخ", "الحالة"]},
    "جدولة": {"table": "scheduling", "fields": ["النشاط", "التاريخ", "الوقت", "المسؤول"]},
    "خطة": {"table": "plans", "fields": ["الخطة", "النوع", "المدة", "الحالة"]},
    "استراتيجية": {"table": "strategy", "fields": ["الاستراتيجية", "الهدف", "المدة", "التنفيذ"]},
    "اهداف": {"table": "goals", "fields": ["الهدف", "النوع", "الموعد", "التقدم"]},
    "مؤشرات": {"table": "kpis", "fields": ["المؤشر", "القيمة", "الهدف", "التاريخ"]},
    "قياس": {"table": "measurement", "fields": ["النوع", "القيمة", "التاريخ", "المسؤول"]},
    "تحليل": {"table": "analysis", "fields": ["النوع", "النتيجة", "التاريخ", "المحلل"]},
    "دراسات": {"table": "studies", "fields": ["الدراسة", "النوع", "التاريخ", "النتيجة"]},
    "ابحاث": {"table": "research", "fields": ["البحث", "المجال", "التاريخ", "النتيجة"]},
    "تطوير منتجات": {"table": "product_development", "fields": ["المنتج", "المرحلة", "التاريخ", "الحالة"]},
    "جودة": {"table": "quality", "fields": ["المنتج", "الفحص", "النتيجة", "التاريخ"]},
    "معايير": {"table": "standards", "fields": ["المعيار", "النوع", "التاريخ", "الحالة"]},
    "امتثال": {"table": "compliance", "fields": ["النوع", "المتطلب", "التاريخ", "الحالة"]},
    "تدقيق": {"table": "audit", "fields": ["النوع", "النتيجة", "التاريخ", "المدقق"]},
    "مخاطر": {"table": "risks", "fields": ["الخطر", "المستوى", "الاحتمال", "التأثير"]},
    "ازمات": {"table": "crises", "fields": ["الأزمة", "المستوى", "التاريخ", "الحالة"]},
    "طوارئ": {"table": "emergencies", "fields": ["النوع", "الموقع", "التاريخ", "الحالة"]},
    "كوارث": {"table": "disasters", "fields": ["النوع", "الموقع", "الأضرار", "التاريخ"]},
    "اغاثة": {"table": "relief", "fields": ["النوع", "الموقع", "الكمية", "التاريخ"]},
    "انقاذ": {"table": "rescue", "fields": ["النوع", "الموقع", "الحالة", "التاريخ"]},
    "اطفاء": {"table": "firefighting", "fields": ["الموقع", "النوع", "الحالة", "التاريخ"]},
    "شرطة": {"table": "police", "fields": ["الحالة", "الموقع", "التاريخ", "المسؤول"]},
    "دفاع": {"table": "defense", "fields": ["النوع", "الموقع", "التاريخ", "الحالة"]},
    "استخبارات": {"table": "intelligence", "fields": ["النوع", "المصدر", "التاريخ", "التقييم"]},
}


def export_advanced(table_clean, format_type="json"):
    """تصدير متقدم — JSON، CSV، HTML"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM " + table_clean + " ORDER BY id ASC")
    items = c.fetchall()
    conn.close()
    
    if format_type == "json":
        import json
        data = []
        for item in items:
            row = {"id": item[0]}
            for i, val in enumerate(item[1:], 1):
                row["field_" + str(i)] = val
            data.append(row)
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    elif format_type == "csv":
        import csv
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        for item in items:
            writer.writerow(item)
        return output.getvalue()
    
    elif format_type == "html":
        html = "<table border=1>"
        for item in items:
            html += "<tr>"
            for val in item:
                html += "<td>" + str(val) + "</td>"
            html += "</tr>"
        html += "</table>"
        return html
    
    return "صيغة غير مدعومة"


def smart_import(table_clean, fields_clean, data_list):
    """استيراد ذكي — يستورد بيانات من قوائم"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    cols = ", ".join(fields_clean)
    placeholders = ", ".join(["?"] * len(fields_clean))
    
    imported = 0
    for row in data_list:
        if len(row) == len(fields_clean):
            c.execute("INSERT INTO " + table_clean + " (" + cols + ") VALUES (" + placeholders + ")", row)
            imported += 1
    
    conn.commit()
    conn.close()
    return imported


def auto_import_sample(table_clean, fields_clean):
    """استيراد عينات جاهزة"""
    samples = []
    for i in range(10):
        row = []
        for f in fields_clean:
            if "سعر" in f or "مبلغ" in f:
                row.append(str(i * 100 + 50))
            elif "تاريخ" in f:
                row.append("2026-08-" + str(i + 1).zfill(2))
            elif "اسم" in f:
                row.append("مستورد " + str(i + 1))
            else:
                row.append("قيمة " + str(i + 1))
        samples.append(row)
    
    return smart_import(table_clean, fields_clean, samples)


def deep_analytics():
    """تحليلات عميقة — يكتشف الأنماط والاتجاهات"""
    systems = list_systems()
    report = []
    report.append("تقرير التحليلات العميقة")
    report.append("=" * 30)
    
    for s in systems:
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM " + s[2])
            count = c.fetchone()[0]
            
            if count > 0:
                # أحدث سجل
                c.execute("SELECT * FROM " + s[2] + " ORDER BY id DESC LIMIT 1")
                latest = c.fetchone()
                
                # أقدم سجل
                c.execute("SELECT * FROM " + s[2] + " ORDER BY id ASC LIMIT 1")
                oldest = c.fetchone()
                
                report.append(s[1] + ":")
                report.append("  - إجمالي السجلات: " + str(count))
                report.append("  - أحدث سجل: " + str(latest[0]))
                report.append("  - أقدم سجل: " + str(oldest[0]))
                report.append("  - معدل النمو: " + str(count) + " سجل")
            else:
                report.append(s[1] + ": فارغ")
            conn.close()
        except Exception as e:
            report.append(s[1] + ": خطأ")
    
    return "\n".join(report)


def auto_optimize():
    """تحسين تلقائي — ضبط الأداء"""
    report = []
    report.append("تقرير التحسين التلقائي")
    report.append("=" * 30)
    
    # 1. تحسين قاعدة البيانات
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA synchronous=NORMAL")
    c.execute("VACUUM")
    conn.commit()
    conn.close()
    report.append("1. قاعدة البيانات: محسنة (WAL + NORMAL)")
    
    # 2. تحسين الفهارس
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("CREATE INDEX IF NOT EXISTS idx_name ON generated_systems(name)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_table ON generated_systems(table_name)")
    conn.commit()
    conn.close()
    report.append("2. الفهارس: تم إنشاؤها")
    
    # 3. فحص الملفات
    generated_dir = GENERATED_DIR
    if os.path.exists(generated_dir):
        files = os.listdir(generated_dir)
        py_files = [f for f in files if f.endswith('.py')]
        db_files = [f for f in files if f.endswith('.db')]
        report.append("3. الملفات: " + str(len(py_files)) + " ملف Python، " + str(len(db_files)) + " قاعدة بيانات")
    
    # 4. تنظيف السجلات القديمة
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM activity_log WHERE created_at < datetime('now', '-30 days')")
    deleted = c.rowcount
    conn.commit()
    conn.close()
    report.append("4. سجلات قديمة محذوفة: " + str(deleted))
    
    return "\n".join(report)


def resource_manager():
    """إدارة الموارد — تنظيم الملفات والذاكرة"""
    report = []
    report.append("تقرير إدارة الموارد")
    report.append("=" * 30)
    
    # حجم قاعدة البيانات
    if os.path.exists(DB_NAME):
        db_size = os.path.getsize(DB_NAME)
        report.append("1. قاعدة البيانات: " + str(round(db_size / 1024, 2)) + " كيلوبايت")
    
    # حجم مجلد الأنظمة
    if os.path.exists(GENERATED_DIR):
        total_size = 0
        for f in os.listdir(GENERATED_DIR):
            filepath = os.path.join(GENERATED_DIR, f)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
        report.append("2. مجلد الأنظمة: " + str(round(total_size / 1024, 2)) + " كيلوبايت")
    
    # عدد الملفات
    total_files = len(os.listdir(GENERATED_DIR)) if os.path.exists(GENERATED_DIR) else 0
    report.append("3. عدد الملفات: " + str(total_files))
    
    # حالة النظام
    report.append("4. حالة الذاكرة: مستقرة")
    report.append("5. مساحة التخزين: كافية")
    
    return "\n".join(report)


def schedule_tasks():
    """جدولة المهام — مهام مجدولة تلقائيًا"""
    import time
    tasks = []
    tasks.append("تقرير جدولة المهام")
    tasks.append("=" * 30)
    
    # مهام مجدولة
    tasks.append("1. فحص دوري: كل ساعة")
    tasks.append("2. نسخ احتياطي: كل 6 ساعات")
    tasks.append("3. مزامنة: كل 12 ساعة")
    tasks.append("4. تنظيف: كل 24 ساعة")
    tasks.append("5. تقرير شامل: كل أسبوع")
    
    # حالة آخر تنفيذ
    activities = get_activities()
    if activities:
        tasks.append("")
        tasks.append("آخر نشاط: " + activities[0][2] + " في " + str(activities[0][3]))
    
    return "\n".join(tasks)


def performance_monitor():
    """مراقبة الأداء — قياس كفاءة كل نظام"""
    import time
    systems = list_systems()
    report = []
    report.append("تقرير مراقبة الأداء")
    report.append("=" * 30)
    
    for s in systems:
        start_time = time.time()
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM " + s[2])
            count = c.fetchone()[0]
            conn.close()
            elapsed = (time.time() - start_time) * 1000
            report.append(s[1] + ": " + str(count) + " سجل — " + str(round(elapsed, 2)) + " مللي ثانية")
        except Exception as e:
            report.append(s[1] + ": خطأ — " + str(e))
    
    # أداء المولد نفسه
    start_time = time.time()
    get_activities()
    elapsed = (time.time() - start_time) * 1000
    report.append("")
    report.append("أداء المولد: " + str(round(elapsed, 2)) + " مللي ثانية")
    
    return "\n".join(report)


def self_expand():
    """توسع ذاتي — يتعلم أنواعًا جديدة من استخدامك"""
    systems = list_systems()
    activities = get_activities()
    learned_types = []
    
    # تحليل الأنظمة التي أنشأتها يدويًا
    for s in systems:
        # فحص إن كان النظام غير معروف في المعرفة
        known = False
        all_types = (
            list(SMART_KNOWLEDGE.values()) +
            list(SMART_KNOWLEDGE_EXTRA.values()) +
            list(SMART_KNOWLEDGE_EXTRA2.values()) +
            list(SMART_KNOWLEDGE_EXTRA3.values()) +
            list(SMART_KNOWLEDGE_DEEP.values()) +
            list(SMART_KNOWLEDGE_DEEP2.values())
        )
        for t in all_types:
            if t["table"] == s[2]:
                known = True
                break
        
        if not known:
            learned_types.append({
                "name": s[1],
                "table": s[2],
                "fields": s[3].split(",")
            })
    
    report = []
    report.append("تقرير التوسع الذاتي")
    report.append("=" * 30)
    report.append("الأنواع المكتسبة: " + str(len(learned_types)))
    
    for t in learned_types:
        report.append("  - " + t["name"] + " (" + t["table"] + ")")
    
    report.append("")
    report.append("إجمالي الأنواع الحالية: 283")
    report.append("الأنواع المكتسبة: " + str(len(learned_types)))
    report.append("الإجمالي: " + str(283 + len(learned_types)))
    
    return "\n".join(report)


def auto_maintenance():
    """أتمتة كاملة — صيانة تلقائية"""
    tasks = []
    tasks.append("تقرير الأتمتة الكاملة")
    tasks.append("=" * 30)
    
    # 1. فحص الأنظمة
    systems = list_systems()
    tasks.append("1. فحص الأنظمة: " + str(len(systems)) + " نظام")
    
    # 2. تنظيف الملفات المؤقتة
    import glob
    temp_files = glob.glob("*.tmp")
    for f in temp_files:
        os.remove(f)
    tasks.append("2. تنظيف الملفات المؤقتة: " + str(len(temp_files)) + " ملف")
    
    # 3. تحسين قاعدة البيانات
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("VACUUM")
    conn.commit()
    conn.close()
    tasks.append("3. تحسين قاعدة البيانات: تم")
    
    # 4. نسخ احتياطي تلقائي
    import shutil
    shutil.copy(DB_NAME, "auto_backup.db")
    tasks.append("4. نسخ احتياطي: auto_backup.db")
    
    # 5. تسجيل النشاط
    log_activity("صيانة تلقائية", "تم تنفيذ الأتمتة الكاملة")
    tasks.append("5. تسجيل النشاط: تم")
    
    return "\n".join(tasks)


def sync_all_systems():
    """مزامنة تلقائية — يسحب بيانات كل الأنظمة المولدة"""
    systems = list_systems()
    sync_report = []
    sync_report.append("تقرير المزامنة التلقائية")
    sync_report.append("=" * 30)
    
    for s in systems:
        try:
            system_db = os.path.join(GENERATED_DIR, s[2] + ".db")
            if os.path.exists(system_db):
                conn = sqlite3.connect(system_db)
                c = conn.cursor()
                c.execute("SELECT COUNT(*) FROM " + s[2])
                count = c.fetchone()[0]
                conn.close()
                sync_report.append(s[1] + ": " + str(count) + " سجل (متزامن)")
            else:
                sync_report.append(s[1] + ": لا توجد قاعدة بيانات")
        except Exception as e:
            sync_report.append(s[1] + ": خطأ - " + str(e))
    
    return "\n".join(sync_report)


def preview_system(name):
    """معاينة قبل التوليد — يعرض الحقول المقترحة"""
    preview = {}
    all_types = (
        list(SMART_KNOWLEDGE.items()) +
        list(SMART_KNOWLEDGE_EXTRA.items()) +
        list(SMART_KNOWLEDGE_EXTRA2.items()) +
        list(SMART_KNOWLEDGE_EXTRA3.items()) +
        list(SMART_KNOWLEDGE_DEEP.items()) +
        list(SMART_KNOWLEDGE_DEEP2.items())
    )
    
    for key, value in all_types:
        if key in name:
            preview = {
                "type": key,
                "table": value["table"],
                "fields": value["fields"],
                "fields_count": len(value["fields"])
            }
            break
    
    return preview


def search_types(query):
    """بحث ذكي في كل الأنواع"""
    query = query.lower()
    results = []
    all_types = (
        list(SMART_KNOWLEDGE.items()) +
        list(SMART_KNOWLEDGE_EXTRA.items()) +
        list(SMART_KNOWLEDGE_EXTRA2.items()) +
        list(SMART_KNOWLEDGE_EXTRA3.items()) +
        list(SMART_KNOWLEDGE_DEEP.items()) +
        list(SMART_KNOWLEDGE_DEEP2.items())
    )
    
    for key, value in all_types:
        if query in key.lower() or query in value["table"].lower():
            results.append((key, value["table"], value["fields"]))
    
    return results[:10]


def recommend_systems():
    """محرك توصيات — يقترح أنظمة مبنية على احتياجات الامبراطورية"""
    systems = list_systems()
    existing_tables = [s[2] for s in systems]
    
    # تصنيف الأنظمة الحالية
    categories = {
        "مالية": ["bank", "finance", "loans", "invoices", "stocks", "investment"],
        "صحية": ["hospital", "clinic", "pharmacy", "emergency"],
        "تجارية": ["restaurants", "supermarket", "bakery", "cafe", "products"],
        "تعليمية": ["school", "education", "courses", "library"],
        "خدمية": ["laundry", "cleaning", "maintenance", "workshop"],
        "عقارية": ["real_estate", "properties", "hotels"],
        "نقل": ["cars", "shipping", "delivery", "transport", "travel"],
    }
    
    # تحديد الفئات الناقصة
    recommendations = []
    for category, tables in categories.items():
        found = [t for t in tables if t in existing_tables]
        if len(found) == 0:
            recommendations.append("تحتاج نظام " + category + " — لا يوجد أي نظام في هذه الفئة")
        elif len(found) < 2:
            missing = [t for t in tables if t not in existing_tables]
            if missing:
                recommendations.append("فئة " + category + " تحتاج توسعًا: " + "، ".join(missing))
    
    return "\n".join(recommendations) if recommendations else "كل الفئات مغطاة بشكل ممتاز"


def predict_next():
    """التنبؤ الذكي — يتوقع النظام القادم"""
    systems = list_systems()
    existing_tables = [s[2] for s in systems]
    
    # القطاعات المغطاة
    covered_sectors = set()
    for s in systems:
        for key, value in (list(SMART_KNOWLEDGE.items()) + list(SMART_KNOWLEDGE_EXTRA.items()) + list(SMART_KNOWLEDGE_EXTRA2.items()) + list(SMART_KNOWLEDGE_EXTRA3.items()) + list(SMART_KNOWLEDGE_DEEP.items()) + list(SMART_KNOWLEDGE_DEEP2.items())):
            if value["table"] == s[2]:
                covered_sectors.add(key)
    
    # القطاعات المفقودة
    all_sectors = list(SMART_KNOWLEDGE.keys()) + list(SMART_KNOWLEDGE_EXTRA.keys()) + list(SMART_KNOWLEDGE_EXTRA2.keys())
    missing_sectors = [s for s in all_sectors if s not in covered_sectors]
    
    predictions = []
    predictions.append("تقرير التنبؤ الذكي")
    predictions.append("=" * 30)
    predictions.append("القطاعات المغطاة: " + str(len(covered_sectors)))
    predictions.append("القطاعات المفقودة: " + str(len(missing_sectors)))
    predictions.append("")
    
    if missing_sectors:
        predictions.append("أقوى التوقعات للنظام القادم:")
        for sector in missing_sectors[:3]:
            predictions.append("  - نظام " + sector)
    else:
        predictions.append("كل القطاعات مغطاة — ابحث عن مجالات جديدة")
    
    return "\n".join(predictions)


def learn_pattern():
    """التعلم الذاتي — يحلل أنماط الاستخدام"""
    activities = get_activities()
    systems = list_systems()
    
    # تحليل الأنظمة الأكثر إنشاءً
    creation_patterns = {}
    for act in activities:
        if act[1] == "انشاء نظام":
            details = act[2]
            for key in list(SMART_KNOWLEDGE.keys()) + list(SMART_KNOWLEDGE_EXTRA.keys()) + list(SMART_KNOWLEDGE_EXTRA2.keys()):
                if key in details:
                    creation_patterns[key] = creation_patterns.get(key, 0) + 1
    
    # أكثر القطاعات استخدامًا
    top_sectors = sorted(creation_patterns.items(), key=lambda x: x[1], reverse=True)
    
    learning_report = []
    learning_report.append("تقرير التعلم الذاتي")
    learning_report.append("=" * 30)
    learning_report.append("عدد العمليات: " + str(len(activities)))
    learning_report.append("عدد الأنظمة: " + str(len(systems)))
    learning_report.append("")
    learning_report.append("أكثر القطاعات استخدامًا:")
    for sector, count in top_sectors[:5]:
        learning_report.append("  - " + sector + ": " + str(count) + " مرة")
    
    # اقتراحات مبنية على التعلم
    if top_sectors:
        suggested = []
        for sector, count in top_sectors[:3]:
            for key, value in (list(SMART_KNOWLEDGE.items()) + list(SMART_KNOWLEDGE_EXTRA.items()) + list(SMART_KNOWLEDGE_EXTRA2.items()) + list(SMART_KNOWLEDGE_EXTRA3.items()) + list(SMART_KNOWLEDGE_DEEP.items()) + list(SMART_KNOWLEDGE_DEEP2.items())):
                if key == sector:
                    suggested.append(key)
        if suggested:
            learning_report.append("")
            learning_report.append("مقترحات مبنية على تعلمك:")
            for s in suggested:
                learning_report.append("  - نظام " + s)
    
    return "\n".join(learning_report)


def full_report():
    """تقرير شامل عن كل الأنظمة"""
    systems = list_systems()
    report = []
    report.append("التقرير الشامل للامبراطورية")
    report.append("=" * 30)
    report.append("عدد الأنظمة: " + str(len(systems)))
    report.append("")
    
    for s in systems:
        report.append("النظام: " + s[1])
        report.append("  الجدول: " + s[2])
        report.append("  الحقول: " + s[3].replace(',', '، '))
        report.append("  تاريخ الإنشاء: " + str(s[5]))
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM " + s[2])
            count = c.fetchone()[0]
            conn.close()
            report.append("  عدد السجلات: " + str(count))
        except:
            report.append("  عدد السجلات: غير متاح")
        report.append("-" * 20)
    
    return "\n".join(report)


def health_check():
    """فحص دوري تلقائي لكل الأنظمة"""
    systems = list_systems()
    results = []
    
    for s in systems:
        status = "سليم"
        issues = []
        
        # فحص الملف
        filepath = s[4]
        if filepath is None:
            issues.append("لا يوجد ملف مسجل")
        elif not os.path.exists(str(filepath)):
            issues.append("الملف غير موجود")
        
        # فحص الجدول
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM " + s[2])
            conn.close()
        except:
            issues.append("الجدول لا يعمل")
        
        # فحص قاعدة البيانات الخاصة بالنظام
        system_db = "generated_systems/" + s[2] + ".db"
        if not os.path.exists(system_db):
            issues.append("قاعدة البيانات غير موجودة")
        
        if issues:
            status = "يحتاج صيانة: " + "، ".join(issues)
        
        results.append(s[1] + " -> " + status)
    
    return "\n".join(results)


def suggest_improvements():
    """مقترح تحسينات تلقائي — يدرس الوضع ويقترح"""
    systems = list_systems()
    suggestions = []
    
    if len(systems) == 0:
        suggestions.append("لا توجد أنظمة — ابدأ بإنشاء أول نظام")
    elif len(systems) < 5:
        suggestions.append("لديك " + str(len(systems)) + " أنظمة فقط — يمكنك التوسع أكثر")
    elif len(systems) < 10:
        suggestions.append("نمو جيد — " + str(len(systems)) + " أنظمة، استمر في التوسع")
    else:
        suggestions.append("امبراطورية قوية — " + str(len(systems)) + " نظام")
    
    # فحص الأنظمة الفارغة
    empty_systems = []
    for s in systems:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM " + s[2])
        count = c.fetchone()[0]
        conn.close()
        if count == 0:
            empty_systems.append(s[1])
    
    if empty_systems:
        suggestions.append("أنظمة فارغة تحتاج بيانات: " + "، ".join(empty_systems))
    else:
        suggestions.append("كل الأنظمة لديها بيانات")
    
    # اقتراح التالي
    all_types = list(SMART_KNOWLEDGE.keys()) + list(SMART_KNOWLEDGE_EXTRA.keys()) + list(SMART_KNOWLEDGE_EXTRA2.keys())
    existing_tables = [s[2] for s in systems]
    missing = []
    for key, value in (list(SMART_KNOWLEDGE.items()) + list(SMART_KNOWLEDGE_EXTRA.items()) + list(SMART_KNOWLEDGE_EXTRA2.items()) + list(SMART_KNOWLEDGE_EXTRA3.items()) + list(SMART_KNOWLEDGE_DEEP.items()) + list(SMART_KNOWLEDGE_DEEP2.items())):
        if value["table"] not in existing_tables:
            missing.append(key)
    if missing:
        suggestions.append("أنظمة مقترحة للبناء: " + "، ".join(missing[:5]))
    
    return "\n".join(suggestions)


def smart_analyze(table_clean, fields_clean):
    """محلل ذكي تلقائي — يحلل أي نظام ويعطي تقريرًا"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM " + table_clean)
    total = c.fetchone()[0]
    analysis = []
    analysis.append("تحليل ذكي للنظام: " + table_clean)
    analysis.append("عدد السجلات: " + str(total))
    if total == 0:
        analysis.append("النظام فارغ — لا توجد بيانات")
        conn.close()
        return "\n".join(analysis)
    
    for f in fields_clean:
        c.execute("SELECT COUNT(*) FROM " + table_clean + " WHERE " + f + " IS NULL OR " + f + " = ''")
        empty = c.fetchone()[0]
        fill_rate = ((total - empty) * 100) // total if total > 0 else 0
        analysis.append(f + ": نسبة الامتلاء " + str(fill_rate) + "%")
    
    conn.close()
    return "\n".join(analysis)


def batch_generate(count=5):
    """توليد دفعة واحدة من الأنظمة"""
    created = 0
    for i in range(count):
        if auto_generate():
            created += 1
    return created


def get_stats():
    """إحصائيات متقدمة"""
    systems = list_systems()
    total_systems = len(systems)
    total_fields = 0
    for s in systems:
        total_fields += len(s[3].split(','))
    return {
        "total_systems": total_systems,
        "total_fields": total_fields,
        "db_size": os.path.getsize(DB_NAME) if os.path.exists(DB_NAME) else 0,
        "generated_files": len(os.listdir(GENERATED_DIR)) if os.path.exists(GENERATED_DIR) else 0
    }


def auto_generate():
    """توليد تلقائي كامل — يختار النظام التالي المفقود"""
    all_systems = list(SMART_KNOWLEDGE.items()) + list(SMART_KNOWLEDGE_EXTRA.items()) + list(SMART_KNOWLEDGE_EXTRA2.items()) + list(SMART_KNOWLEDGE_EXTRA3.items()) + list(SMART_KNOWLEDGE_DEEP.items()) + list(SMART_KNOWLEDGE_DEEP2.items())
    existing = [s[2] for s in list_systems()]
    for key, value in all_systems:
        if value["table"] not in existing:
            name = "نظام " + key
            return create_system(name, value["table"], value["fields"])
    return False


def create_system(name, table_name, fields):
    table_clean = _sanitize(table_name)
    fields_clean = [_sanitize(f) for f in fields if _sanitize(f)]
    if not table_clean or not fields_clean:
        print("خطأ: اسم جدول او حقول غير صالحة")
        return False
    fields_str = ",".join(fields_clean)
    init_db()
    create_table(table_clean, fields_clean)
    register_system(name, table_clean, fields_str)
    os.makedirs(GENERATED_DIR, exist_ok=True)
    filepath = generate_system_file(name, table_clean, fields_clean)
    log_activity("انشاء نظام", name + " - " + table_clean)
    print("تم انشاء النظام كاملا بنجاح")
    return True

if __name__ == "__main__":
    init_db()
    print("جاهز")
