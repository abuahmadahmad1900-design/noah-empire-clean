#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦅 نوح - محرك تشغيل العقول (النسخة الشاملة 250+)
"""

import json
import minds_handlers as handlers

def _get_registry():
    with open("minds_registry.json", "r", encoding="utf-8") as f:
        return json.load(f)

# خريطة أسماء ذكية: تحول اسم العقل إلى دالة معالج
HANDLER_MAP = [
    ("زكاة", handlers.h_zakat),
    ("تحويل", handlers.h_currency),
    ("عملة", handlers.h_currency),
    ("ربح", handlers.h_profit),
    ("توقع", handlers.h_forecast),
    ("نمو", handlers.h_forecast),
    ("تدفق", handlers.h_cashflow),
    ("نقد", handlers.h_cashflow),
    ("عملاء", handlers.h_customers_count),
    ("عميل", handlers.h_customers_count),
    ("منتجات", handlers.h_products_count),
    ("مخزون", handlers.h_products_count),
    ("إيراد", handlers.h_revenue_total),
    ("ديون", handlers.h_debt_ratio),
    ("استثمار", handlers.h_roi),
    ("تعادل", handlers.h_break_even),
    ("ضريب", handlers.h_vat),
    ("راتب", handlers.h_salary),
    ("فائدة", handlers.h_interest),
    ("قيمة", handlers.h_present_value),
    ("قسط", handlers.h_amortization),
    ("72", handlers.h_rule_of_72),
    ("سيولة", handlers.h_current_ratio),
    ("مخاطر", handlers.h_var),
    ("أمان", handlers.h_var),
    ("توزيع", handlers.h_dividend_yield),
    ("سهم", handlers.h_eps),
    ("منشأة", handlers.h_enterprise_value),
    ("معنويات", handlers.h_sentiment),
    ("اكتساب", handlers.h_customer_acquisition_cost),
    ("احتفاظ", handlers.h_customer_retention_rate),
    ("تراجع", handlers.h_churn_rate),
    ("ترويج", handlers.h_net_promoter_score),
    ("رضا", handlers.h_customer_satisfaction),
    ("طلب", handlers.h_average_order_value),
    ("سلة", handlers.h_cart_abandonment),
    ("تحويل الزوار", handlers.h_conversion_rate),
    ("نقر", handlers.h_click_through_rate),
    ("إنفاق إعلاني", handlers.h_roas),
    ("تكلفة التحويل", handlers.h_cpa),
    ("بريد", handlers.h_email_open_rate),
    ("تفاعل", handlers.h_social_engagement),
    ("بحث", handlers.h_seo_traffic),
    ("ارتداد", handlers.h_bounce_rate),
    ("مشاهدات", handlers.h_page_views),
    ("وقت", handlers.h_time_on_site),
    ("إنتاجية", handlers.h_employee_productivity),
    ("غياب", handlers.h_absenteeism),
    ("دوران", handlers.h_turnover_rate),
    ("تدريب", handlers.h_training_hours),
    ("موظف", handlers.h_revenue_per_employee),
    ("موارد", handlers.h_hr_cost),
    ("إضافي", handlers.h_overtime_percentage),
    ("تعويض", handlers.h_compensation_ratio),
    ("إنتاج", handlers.h_production_yield),
    ("عيب", handlers.h_defect_rate),
    ("طاقة", handlers.h_capacity_utilization),
    ("دورة", handlers.h_cycle_time),
    ("تسليم", handlers.h_lead_time),
    ("دقة", handlers.h_inventory_accuracy),
    ("نفاد", handlers.h_stockout_rate),
    ("إعادة طلب", handlers.h_reorder_point),
    ("كمية الطلب", handlers.h_economic_order_quantity),
    ("أمان المخزون", handlers.h_safety_stock),
    ("إرجاع", handlers.h_return_rate),
    ("شحن", handlers.h_shipping_accuracy),
    ("مورد", handlers.h_supplier_on_time),
    ("مشتريات", handlers.h_procurement_cycle),
    ("أصول", handlers.h_return_on_assets),
    ("حقوق", handlers.h_return_on_equity),
    ("نقدية", handlers.h_cash_ratio),
    ("مديونية", handlers.h_debt_ratio),
    ("تغطية", handlers.h_interest_coverage),
    ("مبيعات", handlers.h_sales_growth),
    ("انحراف", handlers.h_price_variance),
    ("جودة", handlers.h_quality_variance),
    ("عمالة", handlers.h_labor_variance),
    ("مواد", handlers.h_material_variance),
    ("ميزانية", handlers.h_budget_variance),
    ("مشروع", handlers.h_project_progress),
    ("تكلفة", handlers.h_cost_performance_index),
    ("جدول", handlers.h_schedule_performance_index),
    ("مخاطرة", handlers.h_risk_score),
    ("تعرض", handlers.h_risk_exposure),
    ("فشل", handlers.h_failure_mode),
    ("أعطال", handlers.h_mean_time_between_failures),
    ("إصلاح", handlers.h_mean_time_to_repair),
    ("توافر", handlers.h_availability),
    ("موثوقية", handlers.h_reliability),
    ("صيانة", handlers.h_maintenance_cost),
    ("كفاءة", handlers.h_efficiency_ratio),
    ("استغلال", handlers.h_utilization_rate),
    ("خردة", handlers.h_scrap_rate),
    ("طاقة كهربائية", handlers.h_energy_consumption),
    ("كربون", handlers.h_carbon_footprint),
    ("مياه", handlers.h_water_usage),
    ("نفايات", handlers.h_waste_reduction),
    ("استدامة", handlers.h_sustainability_score),
    ("حوكمة", handlers.h_governance_score),
    ("ESG", handlers.h_esg_score),
    ("رقمي", handlers.h_digital_transformation),
    ("ابتكار", handlers.h_innovation_index),
    ("بيانات", handlers.h_data_quality),
    ("نظام", handlers.h_system_uptime),
    ("استجابة", handlers.h_response_time),
    ("معالجة", handlers.h_throughput),
    ("انتقال", handlers.h_latency),
    ("نطاق", handlers.h_bandwidth_utilization),
    ("تخزين", handlers.h_storage_utilization),
    ("معالج", handlers.h_cpu_usage),
    ("ذاكرة", handlers.h_memory_usage),
    ("شبكة", handlers.h_network_uptime),
    ("API", handlers.h_api_success_rate),
    ("خطأ", handlers.h_error_rate),
    ("نسخ", handlers.h_backup_success_rate),
    ("استعادة", handlers.h_recovery_time),
    ("حادث", handlers.h_incident_count),
    ("خدمة", handlers.h_sla_compliance),
    ("توقف", handlers.h_downtime_cost),
]

def find_handler(mind_name):
    """يبحث عن معالج حسب كلمات مفتاحية في اسم العقل."""
    for keyword, handler in HANDLER_MAP:
        if keyword in mind_name:
            return handler
    return None

def execute_mind(mind, data):
    handler = find_handler(mind["name"])
    if handler:
        return handler(data)
    return f"✅ العقل «{mind['name']}» تم تفعيله (لا يوجد منطق مخصص)"

def run_by_id(mind_id, data=None):
    minds = _get_registry()
    if mind_id < 1 or mind_id > len(minds):
        return "❌ رقم العقل غير صحيح"
    return execute_mind(minds[mind_id - 1], data or {})

def run_by_name(name, data=None):
    minds = _get_registry()
    for mind in minds:
        if mind["name"] == name:
            return execute_mind(mind, data or {})
    return "❌ لم يتم العثور على العقل"

if __name__ == "__main__":
    print("🦅 المحرك الشامل جاهز (250+ معالج)")
    print(run_by_name("حاسب الزكاة", {"amount": 100000}))
    print(run_by_name("محلل الربحية", {"revenue": 100000, "expenses": 40000}))
    print(run_by_name("صافي نقاط الترويج", {"promoters": 70, "detractors": 10, "total": 100}))
    print(run_by_name("معدل النمو السنوي المركب", {"beginning": 100, "ending": 200, "years": 3}))
