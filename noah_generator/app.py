# -*- coding: utf-8 -*-
from flask import Flask, request, redirect
import sqlite3
import os
import generator as gen

app = Flask(__name__)

STYLE = """
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:Tahoma; background:radial-gradient(ellipse at top,#0a0a2e 0%,#030314 60%,#000 100%); min-height:100vh; color:#fff; overflow-x:hidden; }
.container { max-width:1300px; margin:0 auto; padding:40px 20px; }
.legendary-title { text-align:center; font-size:2.8em; font-weight:900; background:linear-gradient(135deg,#FFD700,#FFA500,#FFD700); -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-shadow:0 0 80px rgba(255,215,0,0.6); margin-bottom:30px; letter-spacing:2px; animation:titleGlow 3s ease-in-out infinite; }
@keyframes titleGlow { 0%,100% { filter:brightness(1); } 50% { filter:brightness(1.4); } }
.legendary-table { width:100%; border-collapse:collapse; margin-top:30px; border-radius:30px; overflow:hidden; background:linear-gradient(145deg,rgba(18,18,55,0.98),rgba(8,8,28,0.98)); box-shadow:0 40px 100px rgba(0,0,0,0.9),0 0 80px rgba(255,215,0,0.3); border:1px solid rgba(255,215,0,0.5); }
.legendary-table th { background:linear-gradient(145deg,rgba(255,215,0,0.08),rgba(255,140,0,0.08)); color:#FFD700; padding:20px; font-weight:900; border-bottom:2px solid #FFD700; text-align:center; }
.legendary-table td { padding:16px; text-align:center; color:#fff; border-bottom:1px solid rgba(255,215,0,0.15); }
.legendary-table tr:hover td { background:rgba(255,215,0,0.05); }
.search-bar { display:flex; justify-content:center; align-items:center; gap:12px; flex-wrap:wrap; margin:30px 0; }
.search-bar input { padding:16px 28px; border-radius:50px; border:2px solid #FFD700; background:rgba(10,10,40,0.9); color:#FFD700; font-size:1.1em; font-weight:bold; width:350px; outline:none; box-shadow:0 0 30px rgba(255,215,0,0.3); transition:all 0.3s; }
.search-bar input:focus { box-shadow:0 0 50px rgba(255,215,0,0.6); border-color:#FFF; }
.legendary-btn { padding:12px 25px; border-radius:50px; border:2px solid #FFD700; background:linear-gradient(145deg,#1a1a4e,#0d0d2b); color:#FFD700; font-weight:900; font-size:0.9em; cursor:pointer; text-decoration:none; box-shadow:0 0 25px rgba(255,215,0,0.3); display:inline-block; transition:all 0.3s; }
.legendary-btn:hover { box-shadow:0 0 50px rgba(255,215,0,0.7); transform:translateY(-3px); border-color:#FFF; }
.summary-bar { padding:12px 22px; border-radius:50px; border:2px solid #FFD700; background:linear-gradient(145deg,#1a1a4e,#0d0d2b); color:#FFD700; font-weight:900; box-shadow:0 0 25px rgba(255,215,0,0.3); }
.form-box { display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin:25px 0; }
.form-box input { padding:14px 22px; border-radius:50px; border:2px solid #FFD700; background:rgba(10,10,40,0.9); color:#FFD700; font-size:1em; font-weight:bold; outline:none; box-shadow:0 0 20px rgba(255,215,0,0.2); transition:all 0.3s; }
.form-box input:focus { box-shadow:0 0 40px rgba(255,215,0,0.5); }
</style>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ''
    if request.method == 'POST':
        smart_name = request.form.get('smart_name')
        name = request.form.get('name')
        table_name = request.form.get('table_name')
        fields_str = request.form.get('fields')
        
        if request.form.get('template_name'):
            tname = request.form.get('template_name')
            success = gen.create_from_template(tname)
            message = 'تم انشاء ' + tname + ' بنجاح' if success else 'فشل الانشاء'
        if request.form.get('batch_generate'):
            created = gen.batch_generate(3)
            if created > 0:
                message = 'تم توليد ' + str(created) + ' أنظمة جديدة بنجاح'
            else:
                message = 'كل الأنواع موجودة مسبقًا'
        if request.form.get('auto_generate'):
            success = gen.auto_generate()
            message = 'تم التوليد التلقائي بنجاح' if success else 'كل الأنظمة موجودة'
        if smart_name:
            success = gen.smart_generate(smart_name)
            message = 'تم التوليد الذكي بنجاح' if success else 'فشل التوليد الذكي'
        elif name and table_name and fields_str:
            fields_list = [f.strip() for f in fields_str.split(',') if f.strip()]
            success = gen.create_system(name, table_name, fields_list)
            message = 'تم انشاء النظام بنجاح' if success else 'فشل الانشاء'
        else:
            message = 'يرجى ملء الحقول'

    systems = gen.list_systems()
    sort_by = request.args.get('sort', 'id')
    if sort_by == 'name':
        systems = sorted(systems, key=lambda x: x[1])
    elif sort_by == 'table':
        systems = sorted(systems, key=lambda x: x[2])
    elif sort_by == 'newest':
        systems = sorted(systems, key=lambda x: x[5], reverse=True)
    count = len(systems)
    rows = ''
    for s in systems:
        rows += '<tr><td>' + str(s[0]) + '</td><td>' + s[1] + '</td><td>' + s[2] + '</td><td>' + s[3].replace(',', '، ') + '</td><td>' + str(s[5]) + '</td>'
        rows += '<td>'
        rows += '<a href="/view/' + str(s[0]) + '" style="padding:3px 8px;border-radius:8px;border:1px solid #FFD700;background:#1a1a4e;color:#FFD700;font-size:0.55em;text-decoration:none;">عرض</a> '
        rows += '<a href="/run/' + str(s[0]) + '" style="padding:3px 8px;border-radius:8px;border:1px solid #00ff88;background:#0a2a1a;color:#00ff88;font-size:0.55em;text-decoration:none;">تشغيل</a> '
        rows += '<a href="/delete/' + str(s[0]) + '" style="padding:3px 8px;border-radius:8px;border:1px solid #FFD700;background:#1a1a4e;color:#FFD700;font-size:0.55em;text-decoration:none;">حذف</a>'
        rows += '</td></tr>'

    return f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head>
    <meta charset="UTF-8"><title>مولد انظمة نوح</title>{STYLE}</head>
    <body><div class="container">
        <h1 class="legendary-title">مولد انظمة نوح</h1>
        <div style="display:flex;justify-content:center;gap:20px;flex-wrap:wrap;margin-bottom:20px;">
            <span class="summary-bar">عدد الانظمة: {count}</span>
            <span class="summary-bar">قاعدة البيانات: noah_generator.db</span>
            <span class="summary-bar">الحالة: نشط</span>
        </div>
        <div style="text-align:center;color:#FFD700;margin-bottom:20px;">{message}</div>
        <div class="form-box">
            <form method="POST" style="display:flex;gap:10px;flex-wrap:wrap;">
                <input type="text" name="smart_name" placeholder="اكتب اسم النظام فقط (مثال: نظام فنادق)" style="width:300px;">
                <button type="submit" class="legendary-btn">توليد ذكي</button>
                <button type="submit" name="auto_generate" class="legendary-btn">توليد تلقائي</button>
                <button type="submit" name="batch_generate" class="legendary-btn">توليد دفعة (5)</button>
                <button type="submit" formaction="/preview" name="preview_name" value="" class="legendary-btn">معاينة</button>
            </form>
        </div>
        <div class="form-box">
            <form method="POST" style="display:flex;gap:10px;flex-wrap:wrap;">
                <input type="text" name="name" placeholder="اسم النظام" required>
                <input type="text" name="table_name" placeholder="اسم الجدول" required>
                <input type="text" name="fields" placeholder="الحقول (اسم, خدمة, تاريخ)" required>
                <button type="submit" class="legendary-btn">توليد يدوي</button>
            </form>
        </div>
        <div class="search-bar">
            <input type="text" placeholder="بحث..." onkeyup="filterGeneric(this)">
            <a href="/" class="legendary-btn">الرئيسية</a>
            <a href="/activities" class="legendary-btn">سجل النشاطات</a>
            <a href="/?sort=name" class="legendary-btn">فرز بالاسم</a>
            <a href="/?sort=table" class="legendary-btn">فرز بالجدول</a>
            <a href="/?sort=newest" class="legendary-btn">الأحدث</a>
            <a href="/stats" class="legendary-btn">الاحصائيات</a>
            <a href="/export-all" class="legendary-btn">تصدير الكل</a>
            <a href="/backup-all" class="legendary-btn">نسخ شامل</a>
            <a href="/ask" class="legendary-btn">مساعد نوح</a>
            <a href="/suggestions" class="legendary-btn">مقترحات</a>
            <a href="/health" class="legendary-btn">فحص دوري</a>
            <a href="/templates" class="legendary-btn">معرض القوالب</a>
            <a href="/full-report" class="legendary-btn">تقرير شامل</a>
            <a href="/learn" class="legendary-btn">تعلم ذاتي</a>
            <a href="/predict" class="legendary-btn">تنبؤ ذكي</a>
            <a href="/recommend" class="legendary-btn">توصيات</a>
            <a href="/executive" class="legendary-btn">لوحة تنفيذية</a>
            <a href="/search-types" class="legendary-btn">بحث ذكي</a>
            <a href="/sync" class="legendary-btn">مزامنة</a>
            <a href="/maintenance" class="legendary-btn">أتمتة</a>
            <a href="/expand" class="legendary-btn">توسع ذاتي</a>
            <a href="/schedule" class="legendary-btn">جدولة</a>
            <a href="/performance" class="legendary-btn">أداء</a>
            <a href="/optimize" class="legendary-btn">تحسين</a>
            <a href="/resources" class="legendary-btn">موارد</a>
            <a href="/analytics" class="legendary-btn">تحليلات</a>
            <a href="/import-sample" class="legendary-btn">استيراد</a>
            <a href="/export-json" class="legendary-btn">تصدير JSON</a>
            <a href="/errors" class="legendary-btn">سجل أخطاء</a>
            <a href="/fix" class="legendary-btn">إصلاح تلقائي</a>
            <a href="/notifications" class="legendary-btn">إشعارات</a>
            <a href="/periodic" class="legendary-btn">تقرير دوري</a>
            <a href="/multi-backup" class="legendary-btn">نسخ متعدد</a>
            <a href="/classify" class="legendary-btn">تصنيف</a>
            <a href="/deep-search" class="legendary-btn">بحث عميق</a>
            <a href="/compare" class="legendary-btn">مقارنة</a>
            <span class="summary-bar">العدد: {count}</span>
        </div>
        <table class="legendary-table">
            <thead><tr><th>ID</th><th>النظام</th><th>الجدول</th><th>الحقول</th><th>تاريخ الانشاء</th><th>اجراءات</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    <script>
    function filterGeneric(input) {{
        var f = input.value.toLowerCase();
        document.querySelectorAll('tbody tr').forEach(function(r) {{
            r.style.display = r.innerText.toLowerCase().includes(f) ? '' : 'none';
        }});
    }}
    </script>
    </body></html>'''

@app.route('/run/<int:system_id>')
def run_system(system_id):
    conn = sqlite3.connect('noah_generator.db')
    c = conn.cursor()
    c.execute('SELECT * FROM generated_systems WHERE id=?', (system_id,))
    sys_row = c.fetchone()
    conn.close()
    if not sys_row:
        return 'النظام غير موجود'
    
    table_name = sys_row[2]
    fields = sys_row[3].split(',')
    
    # جلب بيانات النظام
    conn = sqlite3.connect('noah_generator.db')
    c = conn.cursor()
    c.execute('SELECT * FROM ' + table_name + ' ORDER BY id ASC LIMIT 50')
    items = c.fetchall()
    count = len(items)
    conn.close()
    
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>' + sys_row[1] + '</title>' + STYLE + '</head>'
    html += '<body><div class="container">'
    html += '<h1 class="legendary-title">' + sys_row[1] + '</h1>'
    html += '<div style="display:flex;justify-content:center;gap:15px;flex-wrap:wrap;">'
    html += '<span class="summary-bar">الجدول: ' + table_name + '</span>'
    html += '<span class="summary-bar">عدد السجلات: ' + str(count) + '</span>'
    html += '</div>'
    html += '<div class="search-bar"><a href="/" class="legendary-btn">الرئيسية</a></div>'
    html += '<table class="legendary-table">'
    html += '<thead><tr><th>ID</th>'
    for f in fields:
        html += '<th>' + f + '</th>'
    html += '</tr></thead><tbody>'
    for item in items:
        html += '<tr>'
        for val in item:
            html += '<td>' + str(val) + '</td>'
        html += '</tr>'
    html += '</tbody></table>'
    html += '</div></body></html>'
    return html


@app.route('/backup-all')
def backup_all():
    import shutil
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = 'backup_' + timestamp + '.db'
    shutil.copy('noah_generator.db', backup_file)
    return 'تم النسخ الاحتياطي الشامل: ' + backup_file


@app.route('/export-all')
def export_all():
    import csv
    import io
    systems = gen.list_systems()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'النظام', 'الجدول', 'الحقول', 'التاريخ'])
    for s in systems:
        writer.writerow([s[0], s[1], s[2], s[3], s[5]])
    output.seek(0)
    return output.getvalue(), {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=all_systems.csv'}


@app.route('/preview', methods=['POST'])
def preview():
    name = request.form.get('preview_name', '')
    if name:
        p = gen.preview_system(name)
        if p:
            fields_str = '، '.join(p['fields'])
            return '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>معاينة</title>' + STYLE + '</head><body><div class="container"><h1 class="legendary-title">معاينة النظام</h1><div style="display:flex;justify-content:center;gap:15px;flex-wrap:wrap;"><span class="summary-bar">النوع: ' + p['type'] + '</span><span class="summary-bar">الجدول: ' + p['table'] + '</span><span class="summary-bar">الحقول (' + str(p['fields_count']) + '): ' + fields_str + '</span></div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
        return 'لا يوجد نوع مطابق'
    return 'يرجى إدخال الاسم'


@app.route('/errors')
def errors():
    errs = gen.get_errors()
    rows = ''
    for e in errs:
        rows += '<tr><td>' + str(e[0]) + '</td><td>' + e[1] + '</td><td>' + e[2] + '</td><td>' + str(e[3]) + '</td></tr>'
    count = len(errs)
    return '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الأخطاء</title>' + STYLE + '</head><body><div class="container"><h1 class="legendary-title">سجل الأخطاء</h1><div class="search-bar"><a href="/" class="legendary-btn">الرئيسية</a><span class="summary-bar">الأخطاء: ' + str(count) + '</span></div><table class="legendary-table"><thead><tr><th>ID</th><th>النوع</th><th>التفاصيل</th><th>التاريخ</th></tr></thead><tbody>' + rows + '</tbody></table></div></body></html>'


@app.route('/classify')
def classify():
    cats = gen.classify_systems()
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>تصنيف</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">التصنيف الذكي</h1>'
    html += '<div style="display:flex;justify-content:center;gap:15px;flex-wrap:wrap;">'
    for cat, systems_list in cats.items():
        html += '<span class="summary-bar">' + cat + ' (' + str(len(systems_list)) + ')</span>'
    html += '</div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/deep-search', methods=['GET', 'POST'])
def deep_search():
    results_html = ''
    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            results = gen.deep_search(query)
            for r in results:
                results_html += '<span class="summary-bar">' + r + '</span>'
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>بحث عميق</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">البحث العميق</h1>'
    html += '<div class="form-box"><form method="POST" style="display:flex;gap:10px;flex-wrap:wrap;">'
    html += '<input type="text" name="query" placeholder="ابحث في كل شيء..." required style="width:300px;">'
    html += '<button type="submit" class="legendary-btn">بحث</button>'
    html += '</form></div>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">' + results_html + '</div>'
    html += '<br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/compare', methods=['GET', 'POST'])
def compare():
    result = ''
    if request.method == 'POST':
        table1 = request.form.get('table1', '')
        table2 = request.form.get('table2', '')
        if table1 and table2:
            result = gen.compare_systems(table1, table2)
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>مقارنة</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">مقارنة الأنظمة</h1>'
    html += '<div class="form-box"><form method="POST" style="display:flex;gap:10px;flex-wrap:wrap;">'
    html += '<input type="text" name="table1" placeholder="الجدول الأول" required>'
    html += '<input type="text" name="table2" placeholder="الجدول الثاني" required>'
    html += '<button type="submit" class="legendary-btn">مقارنة</button>'
    html += '</form></div>'
    html += '<div style="text-align:center;"><span class="summary-bar">' + result + '</span></div>'
    html += '<br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/notifications')
def notifications():
    notifs = gen.get_notifications()
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>إشعارات</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">الإشعارات</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for n in notifs:
        html += '<span class="summary-bar">' + n + '</span>'
    html += '</div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/periodic')
def periodic():
    result = gen.periodic_report()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>تقرير دوري</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">التقرير الدوري</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/multi-backup')
def multi_backup():
    result = gen.multi_backup()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>نسخ متعدد</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">النسخ الاحتياطي المتعدد</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        html += '<span class="summary-bar">' + line + '</span>'
    html += '</div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/fix')
def fix():
    result = gen.auto_fix()
    return '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>إصلاح</title>' + STYLE + '</head><body><div class="container"><h1 class="legendary-title">الإصلاح التلقائي</h1><span class="summary-bar">' + result + '</span><br><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'


@app.route('/analytics')
def analytics():
    result = gen.deep_analytics()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>تحليلات</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">التحليلات العميقة</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/import-sample')
def import_sample():
    systems = gen.list_systems()
    if systems:
        s = systems[0]
        fields = s[3].split(',')
        imported = gen.auto_import_sample(s[2], fields)
        return 'تم استيراد ' + str(imported) + ' سجل إلى ' + s[1]
    return 'لا توجد أنظمة'


@app.route('/export-json')
def export_json():
    systems = gen.list_systems()
    if systems:
        s = systems[0]
        result = gen.export_advanced(s[2], "json")
        return result
    return 'لا توجد أنظمة'


@app.route('/schedule')
def schedule():
    result = gen.schedule_tasks()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>جدولة</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">جدولة المهام</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/performance')
def performance():
    result = gen.performance_monitor()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>أداء</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">مراقبة الأداء</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/optimize')
def optimize():
    result = gen.auto_optimize()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>تحسين</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">التحسين التلقائي</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/resources')
def resources():
    result = gen.resource_manager()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>موارد</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">إدارة الموارد</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/sync')
def sync():
    result = gen.sync_all_systems()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>مزامنة</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">المزامنة التلقائية</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/maintenance')
def maintenance():
    result = gen.auto_maintenance()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>أتمتة</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">الأتمتة الكاملة</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/expand')
def expand():
    result = gen.self_expand()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>توسع ذاتي</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">التوسع الذاتي</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'
    return html


@app.route('/search-types', methods=['GET', 'POST'])
def search_types():
    results_html = ''
    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            results = gen.search_types(query)
            for key, table, fields in results:
                results_html += '<span class="summary-bar">' + key + ' -> ' + table + ' [' + ', '.join(fields) + ']</span>'
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>البحث الذكي</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">البحث الذكي في الأنواع</h1>'
    html += '<div class="form-box"><form method="POST" style="display:flex;gap:10px;flex-wrap:wrap;">'
    html += '<input type="text" name="query" placeholder="ابحث: مطعم، صيدلية، فندق..." required style="width:300px;">'
    html += '<button type="submit" class="legendary-btn">بحث</button>'
    html += '</form></div>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">' + results_html + '</div>'
    html += '<br><a href="/" class="legendary-btn">الرئيسية</a>'
    html += '</div></body></html>'
    return html


@app.route('/recommend')
def recommend():
    result = gen.recommend_systems()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>محرك التوصيات</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">محرك التوصيات</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div>'
    html += '<br><a href="/" class="legendary-btn">الرئيسية</a>'
    html += '</div></body></html>'
    return html


@app.route('/executive')
def executive():
    result = gen.executive_dashboard()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>لوحة التحكم التنفيذية</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">لوحة التحكم التنفيذية</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div>'
    html += '<br><a href="/" class="legendary-btn">الرئيسية</a>'
    html += '</div></body></html>'
    return html


@app.route('/learn')
def learn():
    result = gen.learn_pattern()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>التعلم الذاتي</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">التعلم الذاتي</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div>'
    html += '<br><a href="/" class="legendary-btn">الرئيسية</a>'
    html += '</div></body></html>'
    return html


@app.route('/predict')
def predict():
    result = gen.predict_next()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>التنبؤ الذكي</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">التنبؤ الذكي</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div>'
    html += '<br><a href="/" class="legendary-btn">الرئيسية</a>'
    html += '</div></body></html>'
    return html


@app.route('/full-report')
def full_report():
    result = gen.full_report()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>التقرير الشامل</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">التقرير الشامل</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for line in lines:
        if line.strip():
            html += '<span class="summary-bar">' + line + '</span>'
    html += '</div>'
    html += '<br><a href="/" class="legendary-btn">الرئيسية</a>'
    html += '</div></body></html>'
    return html


@app.route('/templates')
def templates():
    templates_list = gen.list_templates()
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>معرض القوالب</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">معرض القوالب</h1>'
    html += '<div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">'
    for t in templates_list:
        html += '<form method="POST" action="/" style="display:inline;"><input type="hidden" name="template_name" value="' + t + '"><button type="submit" class="legendary-btn">' + t + '</button></form>'
    html += '</div>'
    html += '<br><a href="/" class="legendary-btn">الرئيسية</a>'
    html += '</div></body></html>'
    return html


@app.route('/health')
def health():
    result = gen.health_check()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الفحص الدوري</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">الفحص الدوري التلقائي</h1>'
    html += '<div style="display:flex;justify-content:center;gap:15px;flex-wrap:wrap;">'
    for line in lines:
        html += '<span class="summary-bar">' + line + '</span>'
    html += '</div>'
    html += '<br><a href="/" class="legendary-btn">الرئيسية</a>'
    html += '</div></body></html>'
    return html


@app.route('/suggestions')
def suggestions():
    result = gen.suggest_improvements()
    lines = result.split('\n')
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>مقترحات</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">مقترحات التحسين</h1>'
    html += '<div style="display:flex;justify-content:center;gap:15px;flex-wrap:wrap;">'
    for line in lines:
        html += '<span class="summary-bar">' + line + '</span>'
    html += '</div>'
    html += '<br><a href="/" class="legendary-btn">الرئيسية</a>'
    html += '</div></body></html>'
    return html


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    answer = ''
    if request.method == 'POST':
        question = request.form.get('question', '')
        if question:
            answer = gen.ask_noah(question)
    return '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>مساعد نوح</title>' + STYLE + '</head><body><div class="container"><h1 class="legendary-title">مساعد نوح الذكي</h1><div class="form-box"><form method="POST" style="display:flex;gap:10px;flex-wrap:wrap;"><input type="text" name="question" placeholder="اسأل: كم نظام؟ ما الأحدث؟" required style="width:300px;"><button type="submit" class="legendary-btn">اسأل</button></form></div><div style="text-align:center;margin-top:30px;"><span class="summary-bar">' + answer + '</span></div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'


@app.route('/stats')
def stats():
    s = gen.get_stats()
    return '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الاحصائيات</title>' + STYLE + '</head><body><div class="container"><h1 class="legendary-title">الاحصائيات المتقدمة</h1><div style="display:flex;justify-content:center;gap:25px;flex-wrap:wrap;"><span class="summary-bar">عدد الانظمة: ' + str(s["total_systems"]) + '</span><span class="summary-bar">عدد الحقول: ' + str(s["total_fields"]) + '</span><span class="summary-bar">حجم القاعدة: ' + str(s["db_size"]) + ' بايت</span><span class="summary-bar">الملفات المولدة: ' + str(s["generated_files"]) + '</span></div><br><a href="/" class="legendary-btn">الرئيسية</a></div></body></html>'


@app.route('/activities')
def activities():
    acts = gen.get_activities()
    rows = ''
    for a in acts:
        rows += '<tr><td>' + str(a[0]) + '</td><td>' + a[1] + '</td><td>' + a[2] + '</td><td>' + str(a[3]) + '</td></tr>'
    count = len(acts)
    return '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>سجل النشاطات</title>' + STYLE + '</head><body><div class="container"><h1 class="legendary-title">سجل النشاطات</h1><div class="search-bar"><a href="/" class="legendary-btn">الرئيسية</a><span class="summary-bar">عدد النشاطات: ' + str(count) + '</span></div><table class="legendary-table"><thead><tr><th>ID</th><th>النشاط</th><th>التفاصيل</th><th>التاريخ</th></tr></thead><tbody>' + rows + '</tbody></table></div></body></html>'


@app.route('/view/<int:system_id>')
def view_system(system_id):
    conn = sqlite3.connect('noah_generator.db')
    c = conn.cursor()
    c.execute('SELECT * FROM generated_systems WHERE id=?', (system_id,))
    sys_row = c.fetchone()
    conn.close()
    if not sys_row:
        return 'النظام غير موجود'
    filepath = sys_row[4]
    fields_display = sys_row[3].replace(',', '، ')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            code_content = f.read()
        html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>' + sys_row[1] + '</title>' + STYLE + '</head>'
        html += '<body><div class="container">'
        html += '<h1 class="legendary-title">' + sys_row[1] + '</h1>'
        html += '<div style="display:flex;justify-content:center;gap:20px;flex-wrap:wrap;margin-bottom:20px;">'
        html += '<span class="summary-bar">الجدول: ' + sys_row[2] + '</span>'
        html += '<span class="summary-bar">الحقول: ' + fields_display + '</span>'
        html += '<span class="summary-bar">تاريخ الانشاء: ' + str(sys_row[5]) + '</span>'
        html += '</div>'
        html += '<div class="search-bar"><a href="/" class="legendary-btn">الرئيسية</a></div>'
        html += '<pre style="background:#111;padding:20px;border-radius:15px;color:#0f0;overflow:auto;">' + code_content + '</pre>'
        html += '</div></body></html>'
        return html
    return 'ملف الكود غير موجود'

@app.route('/delete/<int:system_id>')
def delete_system(system_id):
    conn = sqlite3.connect('noah_generator.db')
    c = conn.cursor()
    c.execute('SELECT table_name FROM generated_systems WHERE id=?', (system_id,))
    row = c.fetchone()
    if row:
        c.execute('DROP TABLE IF EXISTS ' + row[0])
        c.execute('DELETE FROM generated_systems WHERE id=?', (system_id,))
        conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    gen.init_db()
    app.run(host='0.0.0.0', port=5062)


# تهيئة تلقائية عند استيراد الملف على Render
gen.init_db()
