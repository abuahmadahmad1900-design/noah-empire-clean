#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦅 نوح - مركز قيادة الأباطرة
يعرض 20 إمبراطور وعقولهم وأدواتهم.
"""

import json
from flask import Flask, render_template_string

app = Flask(__name__)

try:
    with open("minds_registry.json", "r", encoding="utf-8") as f:
        minds = json.load(f)
except:
    minds = []

# بيانات الأباطرة
emperors = [
    (1, "NoahPrime", "الإمبراطور الأعلى", "النواة المركزية"),
    (2, "OmniCore", "عرش القيادة", "المحاسبة والمالية"),
    (3, "NexusPrime", "مركز الترابط", "التكامل"),
    (4, "AegisPrime", "درع الحماية", "الأمن"),
    (5, "EvoPrime", "عقل التطور", "التطوير الذاتي"),
    (6, "EthosPrime", "حارس الأخلاق", "القيم"),
    (7, "ClientPrime", "سيد العملاء", "العملاء"),
    (8, "MindsPrime", "سيد العقول", "إدارة العقول"),
    (9, "SoulsPrime", "سيد الأرواح", "الروح"),
    (10, "CapabilitiesPrime", "سيد القدرات", "القدرات"),
    (11, "SecretsPrime", "حارس الأسرار", "التشفير"),
    (12, "KnowledgePrime", "خازن المعرفة", "المعرفة"),
    (13, "NoahPayPrime", "سيد المدفوعات", "المدفوعات"),
    (14, "ShieldsPrime", "سيد الدروع", "الدروع"),
    (15, "CoresPrime", "سيد الأنوية", "الأنوية"),
    (16, "GenesisPrime", "سيد التكوين", "التوليد"),
    (17, "AppStoresPrime", "سيد المتاجر", "المتاجر"),
    (18, "OmniVaultPrime", "حارس الخزائن", "الخزائن"),
    (19, "ZeroSpacePrime", "سيد الفضاء الصفري", "الفضاء"),
    (20, "SelfDevPrime", "سيد التطوير الذاتي", "التطوير"),
]

@app.route('/')
def command():
    emp_stats = []
    for emp in emperors:
        emp_id, name, title, domain = emp
        emp_minds = [m for m in minds if m["emperor"] == name]
        emp_stats.append({
            "id": emp_id,
            "name": name,
            "title": title,
            "domain": domain,
            "minds_count": len(emp_minds),
        })

    content = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🦅 نوح - مركز قيادة الأباطرة</title>
        <style>
            body { font-family:Tahoma; background:#0a0a2e; color:#fff; padding:30px; }
            h1 { text-align:center; color:#FFD700; font-size:2.5rem; margin-bottom:30px; }
            .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:15px; }
            .card {
                background:linear-gradient(145deg,#1a1a4e,#0d0d2e);
                border-radius:20px; padding:25px; text-align:center;
                border:1px solid rgba(255,215,0,0.3); transition:all 0.3s;
            }
            .card:hover { transform:translateY(-8px); border-color:#00c8ff; box-shadow:0 15px 30px rgba(0,200,255,0.3); }
            .icon { font-size:3rem; margin-bottom:10px; }
            .name { color:#FFD700; font-size:1.2rem; font-weight:bold; }
            .title { color:#00c8ff; font-size:0.9rem; margin:8px 0; }
            .domain { color:#aaa; font-size:0.8rem; }
            .count { color:#4aff4a; font-size:1.5rem; font-weight:bold; margin-top:10px; }
            a { color:#00c8ff; text-decoration:none; display:inline-block; margin-top:20px; }
        </style>
    </head>
    <body>
        <h1>🦅 مركز قيادة الأباطرة العشرين</h1>
        <div class="grid">'''
    
    icons = ["👑","🏛️","🔗","🛡️","🧬","⚖️","👥","🧠","💫","⚡","🔐","📚","💳","🛡️","⚙️","🌱","🏪","🔑","🌌","🚀"]
    
    for i, emp in enumerate(emp_stats):
        content += f'''
        <div class="card">
            <div class="icon">{icons[i]}</div>
            <div class="name">{emp["name"]}</div>
            <div class="title">{emp["title"]}</div>
            <div class="domain">{emp["domain"]}</div>
            <div class="count">{emp["minds_count"]} عقل</div>
        </div>'''
    
    content += '''
        </div>
        <a href="/minds">🧠 عرض كل العقول</a>
    </body>
    </html>'''
    return content

@app.route('/minds')
def all_minds():
    content = '''
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>🧠 كل العقول</title>
    <style>
        body { font-family:Tahoma; background:#0a0a2e; color:#fff; padding:20px; }
        h1 { color:#00c8ff; text-align:center; }
        .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:8px; }
        .mind { background:#1a1a3e; padding:10px; border-radius:8px; font-size:0.8rem; }
        a { color:#00c8ff; }
    </style>
    </head>
    <body>
        <h1>🧠 عقول نوح (500)</h1>
        <div class="grid">'''
    for m in minds:
        content += f'<div class="mind">{m["id"]}. {m["name"]}<br><small style="color:#aaa;">{m["emperor"]}</small></div>'
    content += '</div><br><a href="/">🏠 العودة</a></body></html>'
    return content

if __name__ == '__main__':
    print("🦅 مركز قيادة الأباطرة يعمل")
    app.run(host='0.0.0.0', port=5005, debug=False)
