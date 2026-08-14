#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦅 نوح - نواة الإمبراطورية (Empire Core)
يربط الأباطرة العشرين مع مصنع العقول.
"""

from emperors import emperors
from mind_factory import factory

class Empire:
    """الإمبراطورية الكاملة."""
    def __init__(self, emperors, factory):
        self.emperors = emperors
        self.factory = factory

    def assign_mind_to_emperor(self, emperor_name, mind_id):
        """يربط عقلًا بإمبراطور."""
        for emperor in self.emperors:
            if emperor.name == emperor_name:
                mind = self.factory.get_mind(mind_id)
                if mind:
                    emperor.add_mind(mind)
                    return f"✅ تم ربط {mind.name} بـ {emperor.name}"
        return "❌ لم يتم العثور على الإمبراطور"

    def report(self):
        """تقرير شامل."""
        report = "🦅 تقرير إمبراطورية نوح\n"
        report += "=" * 40 + "\n"
        report += f"📊 عدد الأباطرة: {len(self.emperors)}\n"
        report += f"🧠 عدد العقول المسجلة: {len(self.factory.minds)}\n"
        report += "=" * 40 + "\n\n"
        report += "👑 الأباطرة العشرون:\n"
        for e in self.emperors:
            report += f"  {e.id}. {e.name} - {e.title}\n"
        report += "\n🧠 العقول الحالية:\n"
        for mind in self.factory.list_minds():
            report += f"  {mind['id']}. {mind['name']} ({mind['type']}) - {mind['description']}\n"
        return report

if __name__ == "__main__":
    empire = Empire(emperors, factory)

    # ربط العقول بأباطرتهم
    empire.assign_mind_to_emperor("OmniCore", 1)       # حاسب الزكاة
    empire.assign_mind_to_emperor("TradeOmniPrime", 2) # محول العملات
    empire.assign_mind_to_emperor("OmniCore", 3)       # محلل الربحية
    empire.assign_mind_to_emperor("NoahPrime", 4)      # المتنبئ البسيط

    print(empire.report())
