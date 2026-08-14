#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦅 نوح - بوابة API للإمبراطورية
تشغيل العقول الخمسمائة عبر HTTP.
"""

import json
from flask import Flask, request, jsonify
from emperors import emperors
from mind_factory import MindFactory, zakat_calculator, currency_converter, profit_analyzer, simple_forecast

app = Flask(__name__)

# تحميل سجل العقول
try:
    with open("minds_registry.json", "r", encoding="utf-8") as f:
        minds_registry = json.load(f)
except FileNotFoundError:
    minds_registry = []
    print("⚠️ ملف minds_registry.json غير موجود. شغّل generate_500_minds.py أولاً.")

# إنشاء مصنع جديد وتسجيل العقول
factory = MindFactory()
handlers = {
    "zakat_calculator": zakat_calculator,
    "currency_converter": currency_converter,
    "profit_analyzer": profit_analyzer,
    "simple_forecast": simple_forecast,
}

def get_handler(mind_name):
    """إرجاع معالج مناسب حسب اسم العقل."""
    if "زكاة" in mind_name:
        return zakat_calculator
    elif "تحويل" in mind_name or "عملة" in mind_name:
        return currency_converter
    elif "ربح" in mind_name:
        return profit_analyzer
    elif "توقع" in mind_name or "متنبئ" in mind_name:
        return simple_forecast
    else:
        # معالج افتراضي: يرجع وصفًا بسيطًا
        def default_handler(data):
            return f"🧠 العقل {mind_name} يعمل (لا يوجد منطق مخصص بعد)."
        return default_handler

# تسجيل العقول في المصنع
for m in minds_registry:
    handler = get_handler(m["name"])
    factory.create_mind(
        m["emperor"],
        m["name"],
        m["type"],
        m["description"],
        handler
    )

@app.route('/minds', methods=['GET'])
def list_minds():
    """قائمة كل العقول."""
    return jsonify(factory.list_minds())

@app.route('/minds/<int:mind_id>/run', methods=['POST'])
def run_mind(mind_id):
    """تشغيل عقل محدد."""
    data = request.get_json(silent=True) or {}
    result = factory.run_mind(mind_id, data)
    return jsonify({"mind_id": mind_id, "result": result})

@app.route('/emperors', methods=['GET'])
def list_emperors():
    """قائمة الأباطرة."""
    emp_list = [e.info() for e in emperors]
    return jsonify(emp_list)

@app.route('/')
def home():
    return "🦅 إمبراطورية نوح تعمل. استخدم /minds أو /emperors"

if __name__ == '__main__':
    print(f"🦅 بوابة API تعمل، عدد العقول: {len(factory.minds)}")
    app.run(host='0.0.0.0', port=5002, debug=False)
