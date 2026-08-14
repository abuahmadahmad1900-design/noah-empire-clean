#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦅 نوح - لوحة تحكم الإمبراطورية
لوحة بصرية لإدارة العقول والأباطرة.
"""

import json
from flask import Flask, render_template_string, request

app = Flask(__name__)

try:
    with open("minds_registry.json", "r", encoding="utf-8") as f:
        minds = json.load(f)
except:
    minds = []

@app.route('/')
def home():
    emperors = []
    for m in minds:
        if m["emperor"] not in emperors:
            emperors.append(m["emperor"])
    total_minds = len(minds)
    total_emperors = len(emperors)
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🦅 نوح - لوحة تحكم الإمبراطورية</title>
        <style>
            body {{ font-family:Tahoma; background:#0a0a2e; color:#fff; padding:20px; }}
            h1 {{ text-align:center; color:#FFD700; font-size:2.5rem; }}
            .stats {{ display:flex; gap:20px; justify-content:center; margin:30px 0; }}
            .stat {{ background:#1a1a3e; border-radius:15px; padding:30px; text-align:center; border:1px solid rgba(255,215,0,0.3); }}
            .stat .num {{ font-size:2.5rem; color:#FFD700; }}
            .emperors-list {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:10px; }}
            .emp {{ background:#1a1a4e; padding:15px; border-radius:12px; text-align:center; }}
            a {{ color:#00c8ff; display:inline-block; margin-top:20px; }}
        </style>
    </head>
    <body>
        <h1>🦅 لوحة تحكم الإمبراطورية</h1>
        <div class="stats">
            <div class="stat"><div class="num">{total_emperors}</div>أباطرة</div>
            <div class="stat"><div class="num">{total_minds}</div>عقول</div>
        </div>
        <div class="emperors-list">
    '''
    for emp in emperors:
        count = sum(1 for m in minds if m["emperor"] == emp)
        content += f'<div class="emp">{emp}<br><small style="color:#aaa;">{count} عقل</small></div>'
    content += '''
        </div>
        <a href="/minds">🧠 عرض كل العقول</a>
    </body>
    </html>
    '''
    return content

@app.route('/minds')
def minds_list():
    search = request.args.get('q', '')
    filtered = [m for m in minds if search in m["name"] or search in m["emperor"]]
    content = f'''
    <h1 style="color:#00c8ff;">🧠 عقول نوح ({len(filtered)})</h1>
    <form method="GET"><input name="q" placeholder="بحث عن عقل..." value="{search}"><button>بحث</button></form>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:10px;margin-top:20px;">'''
    for m in filtered[:100]:
        content += f'<div style="background:#1a1a3e;padding:15px;border-radius:12px;"><strong style="color:#FFD700;">{m["name"]}</strong><br><small>{m["emperor"]} - {m["type"]}</small></div>'
    content += '</div>'
    return content

if __name__ == '__main__':
    print("🦅 لوحة تحكم الإمبراطورية تعمل")
    app.run(host='0.0.0.0', port=5003, debug=False)
