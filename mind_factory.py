#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦅 نوح - مصنع العقول (Mind Factory)
يسجل العقول ويعطي كل عقل وظيفة حقيقية قابلة للتشغيل.
"""

from datetime import datetime

class Mind:
    """عقل واحد في إمبراطورية نوح."""
    def __init__(self, mind_id, emperor, name, mind_type, description, handler=None):
        self.id = mind_id
        self.emperor = emperor
        self.name = name
        self.type = mind_type      # rule | predictive | language | vision
        self.description = description
        self.handler = handler
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def run(self, input_data):
        """تشغيل العقل إذا كانت له دالة معالجة."""
        if self.handler:
            return self.handler(input_data)
        return f"⚠️ العقل {self.name} ليس له معالج مفعّل بعد."

    def info(self):
        return {
            "id": self.id,
            "emperor": self.emperor,
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "created_at": self.created_at,
        }

class MindFactory:
    """يدير كل عقول نوح."""
    def __init__(self):
        self.minds = {}

    def create_mind(self, emperor, name, mind_type, description, handler=None):
        mind_id = len(self.minds) + 1
        mind = Mind(mind_id, emperor, name, mind_type, description, handler)
        self.minds[mind_id] = mind
        return mind

    def get_mind(self, mind_id):
        return self.minds.get(mind_id)

    def run_mind(self, mind_id, input_data):
        mind = self.get_mind(mind_id)
        if mind:
            return mind.run(input_data)
        return f"❌ لا يوجد عقل برقم {mind_id}"

    def list_minds(self):
        return [mind.info() for mind in self.minds.values()]

# ========== معالجات حقيقية لبعض العقول ==========

def zakat_calculator(data):
    """عقل قواعدي: حساب الزكاة."""
    amount = data.get("amount", 0)
    nisab = 85 * 60
    if amount >= nisab:
        return f"💰 الزكاة المستحقة: {amount * 0.025:.2f}"
    return "✅ لا زكاة عليك لأن المبلغ أقل من النصاب."

def currency_converter(data):
    """عقل قواعدي: تحويل عملات."""
    amount = data.get("amount", 0)
    from_rate = data.get("from_rate", 1.0)
    to_rate = data.get("to_rate", 1.0)
    result = amount * (to_rate / from_rate)
    return f"💱 النتيجة: {result:.4f}"

def profit_analyzer(data):
    """عقل قواعدي: تحليل الربح."""
    revenue = data.get("revenue", 0)
    expenses = data.get("expenses", 0)
    profit = revenue - expenses
    margin = (profit / revenue * 100) if revenue > 0 else 0
    return f"📈 الربح: {profit} | هامش الربح: {margin:.1f}%"

def simple_forecast(data):
    """عقل تنبؤي بسيط: توقع النمو."""
    current = data.get("current", 0)
    growth = data.get("growth", 10)  # نسبة النمو %
    forecast = current * (1 + growth / 100)
    return f"🔮 التوقع: {forecast:.2f}"

# ========== تجهيز المصنع وتسجيل أول 4 عقول ==========
factory = MindFactory()
factory.create_mind("OmniCore", "حاسب الزكاة", "rule", "يحسب زكاة المال", zakat_calculator)
factory.create_mind("TradeOmniPrime", "محول العملات", "rule", "يحول بين العملات", currency_converter)
factory.create_mind("OmniCore", "محلل الربحية", "rule", "يحلل الربح والخسارة", profit_analyzer)
factory.create_mind("NoahPrime", "المتنبئ البسيط", "predictive", "يتوقع النمو المستقبلي", simple_forecast)

if __name__ == "__main__":
    print("🦅 مصنع العقول يعمل")
    print(f"📊 عدد العقول المسجلة: {len(factory.minds)}")
    for mind in factory.list_minds():
        print(f"  {mind['id']}. {mind['name']} ({mind['type']}) - {mind['description']}")
