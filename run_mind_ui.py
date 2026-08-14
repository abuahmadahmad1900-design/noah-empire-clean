#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦅 نوح - واجهة تشغيل العقول
تشغيل أي عقل من المتصفح مباشرة.
"""

import json
from flask import Flask, request, render_template_string
from engine import run_by_id, run_by_name, _get_registry

app = Flask(__name__)

PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦅 نوح - تشغيل العقول</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family: Tahoma, sans-serif;
            background: linear-gradient(135deg, #0a0a2e, #1a0a3e, #0a1a2e);
            background-size: 400% 400%;
            animation: bg-shift 10s ease infinite;
            color: #fff;
            min-height: 100vh;
            padding: 30px;
        }
        @keyframes bg-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(20,20,50,0.9);
            border-radius: 25px;
            padding: 40px;
            border: 1px solid rgba(255,215,0,0.4);
            box-shadow: 0 20px 50px rgba(0,0,0,0.6);
        }
        h1 {
            text-align: center;
            color: #FFD700;
            margin-bottom: 30px;
            font-size: 2rem;
        }
        label {
            display: block;
            margin: 15px 0 5px;
            color: #ccc;
        }
        input, textarea, select, button {
            width: 100%;
            padding: 12px;
            margin: 5px 0 15px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            color: #fff;
            font-size: 1rem;
        }
        textarea {
            min-height: 120px;
            font-family: monospace;
        }
        button {
            background: linear-gradient(45deg, #FFD700, #FF8C00);
            color: #000;
            font-weight: bold;
            cursor: pointer;
            border: none;
            transition: all 0.3s;
        }
        button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(255,215,0,0.4);
        }
        .result {
            background: rgba(0,200,255,0.1);
            border: 1px solid #00c8ff;
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            font-size: 1.2rem;
            text-align: center;
        }
        a {
            color: #00c8ff;
            text-decoration: none;
            display: inline-block;
            margin-top: 20px;
        }
        .minds-list {
            max-height: 300px;
            overflow-y: auto;
            background: rgba(0,0,0,0.2);
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .mind-item {
            padding: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦅 تشغيل عقول نوح</h1>
        <form method="POST">
            <label>اسم العقل أو رقمه:</label>
            <input name="mind_id" placeholder="مثال: 26 أو حاسب الزكاة" required>
            <label>بيانات JSON (اختياري):</label>
            <textarea name="data" placeholder='{"amount": 100000}'></textarea>
            <button type="submit">🚀 تشغيل العقل</button>
        </form>
        {% if result %}
        <div class="result">{{ result }}</div>
        {% endif %}
        <a href="/">🏠 الرئيسية</a> |
        <a href="/minds">🧠 كل العقول</a>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        mind_input = request.form.get('mind_id', '').strip()
        data_str = request.form.get('data', '').strip()
        try:
            data = json.loads(data_str) if data_str else {}
        except json.JSONDecodeError:
            data = {}
        if mind_input.isdigit():
            result = run_by_id(int(mind_input), data)
        else:
            result = run_by_name(mind_input, data)
    return render_template_string(PAGE, result=result)

@app.route('/minds')
def minds():
    minds = _get_registry()
    content = '''
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>🧠 كل العقول</title>
    <style>
        body { font-family:Tahoma; background:#0a0a2e; color:#fff; padding:20px; }
        h1 { color:#FFD700; text-align:center; }
        .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:8px; margin-top:20px; }
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
    print("🦅 واجهة تشغيل العقول تعمل")
    app.run(host='0.0.0.0', port=5004, debug=False)
