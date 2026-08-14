#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦅 نوح - مصنع الأباطرة (Emperor Factory)
يسجل الأباطرة العشرين الحقيقيين ويمنحهم نطاقاتهم.
"""

class Emperor:
    """إمبراطور واحد في نوح."""
    def __init__(self, emp_id, name, title, domain, description):
        self.id = emp_id
        self.name = name
        self.title = title
        self.domain = domain
        self.description = description
        self.minds = []  # قائمة العقول التابعة له

    def add_mind(self, mind):
        self.minds.append(mind)

    def info(self):
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "domain": self.domain,
            "description": self.description,
            "minds_count": len(self.minds),
        }

# ========== تسجيل الأباطرة العشرين ==========
emperors_data = [
    (1, "NoahPrime", "الإمبراطور الأعلى", "النواة المركزية", "يدير كل الإمبراطورية"),
    (2, "OmniCore", "عرش القيادة", "المحاسبة والمالية", "يدير الأنظمة المالية"),
    (3, "NexusPrime", "مركز الترابط", "التكامل والربط", "يربط كل المكونات"),
    (4, "AegisPrime", "درع الحماية", "الأمن والحماية", "يحرس الإمبراطورية"),
    (5, "EvoPrime", "عقل التطور", "التطوير الذاتي", "يطور الأنظمة تلقائياً"),
    (6, "EthosPrime", "حارس الأخلاق", "القيم والامتثال", "يضمن السلوك الأخلاقي"),
    (7, "ClientPrime", "سيد العملاء", "إدارة العملاء", "يعتني بالعملاء"),
    (8, "MindsPrime", "سيد العقول", "إدارة العقول", "يشرف على 500 عقل"),
    (9, "SoulsPrime", "سيد الأرواح", "عناصر الروح", "يدير القيم الروحية"),
    (10, "CapabilitiesPrime", "سيد القدرات", "القدرات", "يدير القدرات المتخصصة"),
    (11, "SecretsPrime", "حارس الأسرار", "التشفير والأسرار", "يحمي الأسرار"),
    (12, "KnowledgePrime", "خازن المعرفة", "المعرفة والتعلم", "يدير المعرفة"),
    (13, "NoahPayPrime", "سيد المدفوعات", "المدفوعات", "يدير أنظمة الدفع"),
    (14, "ShieldsPrime", "سيد الدروع", "الدروع", "يدير الدروع"),
    (15, "CoresPrime", "سيد الأنوية", "الأنوية", "يدير الأنوية"),
    (16, "GenesisPrime", "سيد التكوين", "الإنشاء والتوليد", "يولد الأنظمة"),
    (17, "AppStoresPrime", "سيد المتاجر", "المتاجر والتطبيقات", "يدير المتاجر"),
    (18, "OmniVaultPrime", "حارس الخزائن", "الخزائن", "يحمي الخزائن"),
    (19, "ZeroSpacePrime", "سيد الفضاء الصفري", "الفضاء الصفري", "يدير الفراغ الرقمي"),
    (20, "SelfDevPrime", "سيد التطوير الذاتي", "التطوير الذاتي", "يطور نفسه"),
]

emperors = []
for emp in emperors_data:
    emperors.append(Emperor(*emp))

if __name__ == "__main__":
    print("🦅 الأباطرة العشرون:")
    for e in emperors:
        print(f"  {e.id}. {e.name} - {e.title} ({e.domain})")
