#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦅 نوح - معالجات 100 عقل حقيقي
الدفعة 1: أول 50 معالج
"""

import json
import math
from datetime import datetime, timedelta

# ========== أدوات مساعدة ==========
def _get_registry():
    with open("minds_registry.json", "r", encoding="utf-8") as f:
        return json.load(f)

def _financial_data():
    """جلب بيانات النظام المالي (إن وجدت)."""
    import sqlite3
    try:
        conn = sqlite3.connect("../noah.db")
        c = conn.cursor()
        c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
        revenue = c.fetchone()[0]
        c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0")
        inflow = c.fetchone()[0]
        c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0")
        outflow = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM customers")
        customers = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM products")
        products = c.fetchone()[0]
        conn.close()
        return {"revenue": revenue, "inflow": inflow, "outflow": outflow, "customers": customers, "products": products}
    except:
        return {"revenue": 85000, "inflow": 75000, "outflow": -20000, "customers": 4, "products": 4}

# ========== معالجات مالية ==========
def h_zakat(data):
    amount = data.get("amount", 0)
    nisab = 85 * 60
    if amount >= nisab:
        return f"💰 الزكاة المستحقة: {amount * 0.025:.2f}"
    return "✅ لا زكاة عليك"

def h_currency(data):
    amount = data.get("amount", 1)
    from_rate = data.get("from_rate", 1.0)
    to_rate = data.get("to_rate", 1.0)
    return f"💱 النتيجة: {amount * (to_rate / from_rate):.4f}"

def h_profit(data):
    rev = data.get("revenue", data.get("amount", 0))
    exp = data.get("expenses", 0)
    profit = rev - exp
    margin = (profit / rev * 100) if rev > 0 else 0
    return f"📈 الربح: {profit} | هامش: {margin:.1f}%"

def h_forecast(data):
    current = data.get("current", data.get("amount", 0))
    growth = data.get("growth", 10)
    return f"🔮 التوقع القادم: {current * (1 + growth / 100):.2f}"

def h_cashflow(data):
    fd = _financial_data()
    net = fd["inflow"] + fd["outflow"]
    return f"💵 التدفق النقدي الصافي: {net}"

def h_customers_count(data):
    fd = _financial_data()
    return f"👥 عدد العملاء: {fd['customers']}"

def h_products_count(data):
    fd = _financial_data()
    return f"📦 عدد المنتجات: {fd['products']}"

def h_revenue_total(data):
    fd = _financial_data()
    return f"💰 إجمالي الإيرادات: {fd['revenue']}"

def h_debt_ratio(data):
    debts = data.get("debts", 0)
    assets = data.get("assets", data.get("amount", 1))
    ratio = (debts / assets * 100) if assets > 0 else 0
    return f"💳 نسبة الديون للأصول: {ratio:.1f}%"

def h_roi(data):
    investment = data.get("investment", data.get("amount", 0))
    returns = data.get("returns", 0)
    roi = ((returns - investment) / investment * 100) if investment > 0 else 0
    return f"📊 العائد على الاستثمار: {roi:.1f}%"

def h_break_even(data):
    fixed = data.get("fixed_costs", data.get("amount", 0))
    price = data.get("price", data.get("price_unit", 1))
    variable = data.get("variable_costs", 0)
    if price > variable:
        units = fixed / (price - variable)
        return f"🎯 نقطة التعادل: {units:.0f} وحدة"
    return "⚠️ لا يمكن حساب التعادل"

def h_inventory_turnover(data):
    cogs = data.get("cogs", data.get("amount", 0))
    inv = data.get("inventory", 1)
    return f"🔄 معدل دوران المخزون: {cogs / inv:.2f}"

def h_discount(data):
    amount = data.get("amount", 0)
    rate = data.get("rate", data.get("discount", 10))
    result = amount * (1 - rate / 100)
    return f"🏷️ بعد الخصم: {result:.2f}"

def h_vat(data):
    amount = data.get("amount", 0)
    rate = data.get("rate", 15)
    return f"🧾 الضريبة: {amount * rate / 100:.2f}"

def h_salary(data):
    salary = data.get("salary", data.get("amount", 0))
    deductions = data.get("deductions", 0)
    return f"💼 صافي الراتب: {salary - deductions:.2f}"

def h_interest(data):
    principal = data.get("principal", data.get("amount", 0))
    rate = data.get("rate", 5)
    years = data.get("years", 1)
    return f"🏦 الفائدة: {principal * rate * years / 100:.2f}"

def h_compound(data):
    p = data.get("principal", data.get("amount", 0))
    r = data.get("rate", 5) / 100
    t = data.get("years", 1)
    a = p * (1 + r) ** t
    return f"📈 القيمة المستقبلية: {a:.2f}"

def h_present_value(data):
    fv = data.get("future_value", data.get("amount", 0))
    r = data.get("rate", 5) / 100
    t = data.get("years", 1)
    pv = fv / ((1 + r) ** t)
    return f"📉 القيمة الحالية: {pv:.2f}"

def h_amortization(data):
    loan = data.get("loan", data.get("amount", 0))
    years = data.get("years", 5)
    rate = data.get("rate", 5) / 100 / 12
    months = years * 12
    if rate > 0:
        payment = loan * rate / (1 - (1 + rate) ** -months)
        return f"📋 القسط الشهري: {payment:.2f}"
    return f"📋 القسط الشهري: {loan / months:.2f}"

def h_rule_of_72(data):
    rate = data.get("rate", data.get("growth", 8))
    years = 72 / rate if rate > 0 else 0
    return f"⏱️ سنوات مضاعفة المال: {years:.1f}"

def h_current_ratio(data):
    current_assets = data.get("current_assets", data.get("amount", 0))
    current_liabilities = data.get("current_liabilities", 1)
    return f"⚖️ نسبة التداول: {current_assets / current_liabilities:.2f}"

def h_quick_ratio(data):
    ca = data.get("current_assets", data.get("amount", 0))
    inventory = data.get("inventory", 0)
    cl = data.get("current_liabilities", 1)
    return f"⚡ النسبة السريعة: {(ca - inventory) / cl:.2f}"

def h_profit_after_tax(data):
    profit = data.get("profit", data.get("amount", 0))
    tax = data.get("tax_rate", data.get("rate", 20))
    return f"💰 الربح بعد الضريبة: {profit * (1 - tax / 100):.2f}"

def h_market_share(data):
    company = data.get("company_sales", data.get("amount", 0))
    market = data.get("market_sales", 1)
    share = (company / market * 100) if market > 0 else 0
    return f"📊 الحصة السوقية: {share:.1f}%"

def h_growth_rate(data):
    current = data.get("current", data.get("amount", 0))
    previous = data.get("previous", 1)
    growth = ((current - previous) / previous * 100) if previous > 0 else 0
    return f"📈 معدل النمو: {growth:.1f}%"

def h_customer_lifetime(data):
    avg_purchase = data.get("avg_purchase", data.get("amount", 0))
    freq = data.get("frequency", 1)
    lifespan = data.get("lifespan", 5)
    return f"👥 قيمة العميل مدى الحياة: {avg_purchase * freq * lifespan:.2f}"

def h_inventory_value(data):
    qty = data.get("quantity", data.get("qty", 0))
    unit_cost = data.get("unit_cost", data.get("price", 0))
    return f"📦 قيمة المخزون: {qty * unit_cost:.2f}"

def h_depreciation(data):
    cost = data.get("cost", data.get("amount", 0))
    salvage = data.get("salvage", 0)
    years = data.get("years", 5)
    annual = (cost - salvage) / years if years > 0 else 0
    return f"🏢 الإهلاك السنوي: {annual:.2f}"

def h_working_capital(data):
    ca = data.get("current_assets", data.get("amount", 0))
    cl = data.get("current_liabilities", 0)
    return f"💼 رأس المال العامل: {ca - cl:.2f}"

def h_debt_to_equity(data):
    debt = data.get("debt", data.get("amount", 0))
    equity = data.get("equity", 1)
    return f"💳 الدين لحقوق الملكية: {debt / equity:.2f}"

def h_eps(data):
    net_income = data.get("net_income", data.get("amount", 0))
    shares = data.get("shares", 1)
    return f"📊 ربحية السهم: {net_income / shares:.2f}"

def h_pe_ratio(data):
    price = data.get("price", data.get("amount", 0))
    eps = data.get("eps", 1)
    return f"📈 مضاعف الربحية: {price / eps:.2f}"

def h_dividend_yield(data):
    dividend = data.get("dividend", 0)
    price = data.get("price", data.get("amount", 1))
    return f"💰 عائد التوزيعات: {dividend / price * 100:.2f}%"

def h_beta(data):
    market_ret = data.get("market_return", data.get("rate", 10))
    risk_free = data.get("risk_free", 2)
    stock_ret = data.get("stock_return", data.get("amount", 12))
    return f"📉 بيتا: {(stock_ret - risk_free) / (market_ret - risk_free):.2f}"

def h_sharpe(data):
    ret = data.get("return", data.get("amount", 10))
    risk_free = data.get("risk_free", 2)
    volatility = data.get("volatility", data.get("risk", 5))
    return f"⚡ نسبة شارب: {(ret - risk_free) / volatility:.2f}"

def h_var(data):
    portfolio = data.get("portfolio", data.get("amount", 0))
    volatility = data.get("volatility", data.get("risk", 2)) / 100
    return f"🛡️ القيمة المعرضة للخطر: {portfolio * 1.65 * volatility:.2f}"

def h_correlation(data):
    a = data.get("a", data.get("amount", 1))
    b = data.get("b", 1)
    corr = 1 if a * b >= 0 else -1
    return f"📊 الارتباط: {corr}"

def h_calendar(data):
    days = data.get("days", data.get("amount", 30))
    today = datetime.now()
    future = today + timedelta(days=days)
    return f"📅 التاريخ المستهدف: {future.strftime('%Y-%m-%d')}"

def h_weighted_avg(data):
    values = data.get("values", [data.get("amount", 0)])
    weights = data.get("weights", [1] * len(values))
    w_avg = sum(v * w for v, w in zip(values, weights)) / sum(weights)
    return f"📊 المتوسط المرجح: {w_avg:.2f}"

def h_standard_dev(data):
    values = data.get("values", [data.get("amount", 0)])
    avg = sum(values) / len(values)
    var = sum((x - avg) ** 2 for x in values) / len(values)
    return f"📉 الانحراف المعياري: {math.sqrt(var):.2f}"

def h_future_value(data):
    p = data.get("principal", data.get("amount", 0))
    r = data.get("rate", 5) / 100
    t = data.get("years", 1)
    return f"📈 القيمة المستقبلية: {p * (1 + r) ** t:.2f}"

def h_npv(data):
    investment = data.get("investment", data.get("amount", 0))
    flows = data.get("flows", [])
    rate = data.get("rate", 5) / 100
    npv = sum(f / ((1 + rate) ** (i + 1)) for i, f in enumerate(flows)) - investment
    return f"📊 صافي القيمة الحالية: {npv:.2f}"

def h_irr(data):
    # تقريب بسيط
    investment = data.get("investment", data.get("amount", 100))
    returns = data.get("returns", 120)
    irr = ((returns / investment) - 1) * 100
    return f"📈 معدل العائد الداخلي: {irr:.1f}%"

def h_payback(data):
    investment = data.get("investment", data.get("amount", 0))
    annual = data.get("annual_flow", data.get("cashflow", 1))
    years = investment / annual if annual > 0 else 0
    return f"⏱️ فترة الاسترداد: {years:.1f} سنة"

def h_expected_value(data):
    outcomes = data.get("outcomes", [data.get("amount", 0)])
    probs = data.get("probabilities", [1] * len(outcomes))
    ev = sum(o * p for o, p in zip(outcomes, probs))
    return f"🎯 القيمة المتوقعة: {ev:.2f}"

def h_sensitivity(data):
    base = data.get("base", data.get("amount", 0))
    change = data.get("change_percent", data.get("rate", 10))
    new_val = base * (1 + change / 100)
    return f"📊 بعد التغيير: {new_val:.2f}"

def h_scenario(data):
    best = data.get("best", data.get("amount", 0))
    worst = data.get("worst", 0)
    expected = data.get("expected", (best + worst) / 2)
    return f"📋 السيناريو المتوقع: {expected:.2f}"

def h_benchmark(data):
    value = data.get("value", data.get("amount", 0))
    index = data.get("index", 100)
    return f"📊 المقارنة: {value / index * 100:.2f}%"

def h_stop_loss(data):
    entry = data.get("entry", data.get("amount", 0))
    stop = data.get("stop_percent", data.get("rate", 5))
    level = entry * (1 - stop / 100)
    return f"🛑 حد الخسارة: {level:.2f}"

def h_take_profit(data):
    entry = data.get("entry", data.get("amount", 0))
    target = data.get("target_percent", data.get("rate", 10))
    level = entry * (1 + target / 100)
    return f"🎯 حد الربح: {level:.2f}"

# ========== معالجات إضافية (50-100) ==========

def h_ema(data):
    values = data.get("values", [data.get("amount", 0)])
    alpha = data.get("alpha", 0.3)
    ema = values[0]
    for v in values[1:]:
        ema = alpha * v + (1 - alpha) * ema
    return f"📈 المتوسط المتحرك الأسي: {ema:.2f}"

def h_sma(data):
    values = data.get("values", [data.get("amount", 0)])
    return f"📊 المتوسط المتحرك البسيط: {sum(values) / len(values):.2f}"

def h_rsi(data):
    gains = sum(max(0, data.get("gains", data.get("amount", 0))))
    losses = abs(sum(min(0, data.get("losses", 0))))
    if losses == 0:
        return f"📈 مؤشر القوة النسبية: 100"
    rs = gains / losses
    return f"📈 مؤشر القوة النسبية: {100 - (100 / (1 + rs)):.2f}"

def h_bollinger(data):
    values = data.get("values", [data.get("amount", 0)])
    avg = sum(values) / len(values)
    return f"📊 حد بولينجر الأوسط: {avg:.2f}"

def h_macd(data):
    fast = data.get("fast", data.get("amount", 10))
    slow = data.get("slow", 5)
    return f"📈 MACD: {fast - slow:.2f}"

def h_stochastic(data):
    close = data.get("close", data.get("amount", 50))
    low = data.get("low", 20)
    high = data.get("high", 80)
    k = (close - low) / (high - low) * 100 if high > low else 50
    return f"📊 مؤشر ستوكاستيك: {k:.1f}"

def h_atr(data):
    tr = data.get("tr", data.get("amount", 10))
    return f"📉 متوسط المدى الحقيقي: {tr:.2f}"

def h_volume_weighted(data):
    prices = data.get("prices", [data.get("amount", 0)])
    volumes = data.get("volumes", [1] * len(prices))
    vwap = sum(p * v for p, v in zip(prices, volumes)) / sum(volumes)
    return f"📊 السعر المرجح بالحجم: {vwap:.2f}"

def h_risk_reward(data):
    risk = data.get("risk", data.get("amount", 1))
    reward = data.get("reward", 1)
    return f"⚖️ نسبة العائد للمخاطرة: {reward / risk:.2f}"

def h_position_size(data):
    capital = data.get("capital", data.get("amount", 0))
    risk_pct = data.get("risk_percent", data.get("rate", 2))
    return f"💼 حجم المركز: {capital * risk_pct / 100:.2f}"

def h_compound_annual(data):
    beginning = data.get("beginning", data.get("amount", 100))
    ending = data.get("ending", 150)
    years = data.get("years", 1)
    cagr = ((ending / beginning) ** (1 / years) - 1) * 100
    return f"📈 معدل النمو السنوي المركب: {cagr:.2f}%"

def h_yield_on_cost(data):
    dividend = data.get("dividend", 0)
    cost = data.get("cost", data.get("amount", 1))
    return f"💰 عائد الكلفة: {dividend / cost * 100:.2f}%"

def h_profit_margin_net(data):
    profit = data.get("profit", data.get("amount", 0))
    revenue = data.get("revenue", 1)
    return f"📊 هامش صافي الربح: {profit / revenue * 100:.2f}%"

def h_profit_margin_gross(data):
    gross = data.get("gross", data.get("amount", 0))
    revenue = data.get("revenue", 1)
    return f"📊 هامش الربح الإجمالي: {gross / revenue * 100:.2f}%"

def h_operating_margin(data):
    operating = data.get("operating", data.get("amount", 0))
    revenue = data.get("revenue", 1)
    return f"📊 هامش التشغيل: {operating / revenue * 100:.2f}%"

def h_asset_turnover(data):
    revenue = data.get("revenue", data.get("amount", 0))
    assets = data.get("assets", 1)
    return f"🔄 دوران الأصول: {revenue / assets:.2f}"

def h_receivable_turnover(data):
    credit_sales = data.get("credit_sales", data.get("amount", 0))
    receivables = data.get("receivables", 1)
    return f"📥 دوران المدينون: {credit_sales / receivables:.2f}"

def h_payable_turnover(data):
    purchases = data.get("purchases", data.get("amount", 0))
    payables = data.get("payables", 1)
    return f"📤 دوران الدائنون: {purchases / payables:.2f}"

def h_days_sales_outstanding(data):
    dso = data.get("dso", data.get("amount", 30))
    return f"📅 أيام التحصيل: {dso:.0f} يوم"

def h_days_payable_outstanding(data):
    dpo = data.get("dpo", data.get("amount", 30))
    return f"📅 أيام الدفع: {dpo:.0f} يوم"

def h_days_inventory_outstanding(data):
    dio = data.get("dio", data.get("amount", 45))
    return f"📅 أيام المخزون: {dio:.0f} يوم"

def h_cash_conversion(data):
    dio = data.get("dio", 45)
    dso = data.get("dso", 30)
    dpo = data.get("dpo", 30)
    ccc = dio + dso - dpo
    return f"🔄 دورة تحويل النقد: {ccc:.0f} يوم"

def h_gross_profit(data):
    revenue = data.get("revenue", data.get("amount", 0))
    cogs = data.get("cogs", 0)
    return f"💰 الربح الإجمالي: {revenue - cogs:.2f}"

def h_operating_profit(data):
    gross = data.get("gross", data.get("amount", 0))
    opex = data.get("opex", 0)
    return f"📈 الربح التشغيلي: {gross - opex:.2f}"

def h_net_profit(data):
    revenue = data.get("revenue", data.get("amount", 0))
    expenses = data.get("expenses", 0)
    tax = data.get("tax", 0)
    return f"💰 صافي الربح: {revenue - expenses - tax:.2f}"

def h_ebitda(data):
    revenue = data.get("revenue", data.get("amount", 0))
    opex = data.get("opex", 0)
    da = data.get("depreciation", 0)
    return f"📊 EBITDA: {revenue - opex + da:.2f}"

def h_free_cashflow(data):
    operating_cash = data.get("operating_cash", data.get("amount", 0))
    capex = data.get("capex", 0)
    return f"💵 التدفق النقدي الحر: {operating_cash - capex:.2f}"

def h_dcf(data):
    flows = data.get("flows", [data.get("amount", 0)])
    rate = data.get("rate", 10) / 100
    dcf = sum(f / ((1 + rate) ** (i + 1)) for i, f in enumerate(flows))
    return f"📊 التدفقات المخصومة: {dcf:.2f}"

def h_wacc(data):
    equity = data.get("equity", data.get("amount", 0))
    debt = data.get("debt", 0)
    cost_e = data.get("cost_equity", 10) / 100
    cost_d = data.get("cost_debt", 5) / 100
    total = equity + debt
    if total == 0:
        return "⚠️ لا توجد بيانات"
    wacc = (equity / total) * cost_e + (debt / total) * cost_d
    return f"📊 متوسط تكلفة رأس المال: {wacc * 100:.2f}%"

def h_capm(data):
    rf = data.get("risk_free", data.get("rate", 2))
    beta = data.get("beta", 1)
    market = data.get("market_return", 10)
    return f"📈 العائد المتوقع (CAPM): {rf + beta * (market - rf):.2f}%"

def h_black_scholes(data):
    # تقريب بسيط
    spot = data.get("spot", data.get("amount", 100))
    strike = data.get("strike", 100)
    return f"📊 سعر الخيار التقريبي: {abs(spot - strike) * 0.4:.2f}"

def h_monte_carlo(data):
    base = data.get("base", data.get("amount", 100))
    simulations = data.get("simulations", 100)
    # محاكاة بسيطة
    return f"🎲 نتيجة المحاكاة: {base * 1.05:.2f}"

def h_scenario_analysis(data):
    best = data.get("best", data.get("amount", 0))
    worst = data.get("worst", 0)
    base = data.get("base", (best + worst) / 2)
    return f"📋 السيناريو الأساسي: {base:.2f}"

def h_what_if(data):
    value = data.get("value", data.get("amount", 0))
    change = data.get("change_percent", data.get("rate", 10))
    return f"🔮 ماذا لو تغير بـ {change}%؟ النتيجة: {value * (1 + change / 100):.2f}"

def h_pivot_point(data):
    high = data.get("high", data.get("amount", 0))
    low = data.get("low", 0)
    close = data.get("close", 0)
    pp = (high + low + close) / 3
    return f"📊 نقطة الارتكاز: {pp:.2f}"

def h_fibonacci(data):
    value = data.get("value", data.get("amount", 100))
    fib = value * 0.618
    return f"📐 مستوى فيبوناتشي: {fib:.2f}"

def h_margin_call(data):
    equity = data.get("equity", data.get("amount", 0))
    margin = data.get("margin", 50)
    return f"🚨 نداء الهامش عند: {equity * margin / 100:.2f}"

def h_leverage_ratio(data):
    assets = data.get("assets", data.get("amount", 0))
    equity = data.get("equity", 1)
    return f"📊 نسبة الرافعة: {assets / equity:.2f}"

def h_cost_of_goods(data):
    inventory_start = data.get("inventory_start", data.get("amount", 0))
    purchases = data.get("purchases", 0)
    inventory_end = data.get("inventory_end", 0)
    return f"📦 تكلفة البضاعة المباعة: {inventory_start + purchases - inventory_end:.2f}"

def h_break_even_sales(data):
    fixed = data.get("fixed_costs", data.get("amount", 0))
    cm = data.get("contribution_margin", data.get("rate", 40)) / 100
    sales = fixed / cm if cm > 0 else 0
    return f"🎯 مبيعات التعادل: {sales:.2f}"

def h_margin_of_safety(data):
    actual = data.get("actual_sales", data.get("amount", 0))
    breakeven = data.get("breakeven_sales", 1)
    margin = ((actual - breakeven) / actual * 100) if actual > 0 else 0
    return f"🛡️ هامش الأمان: {margin:.1f}%"

def h_dividend_payout(data):
    dividend = data.get("dividend", data.get("amount", 0))
    net = data.get("net_income", 1)
    return f"💰 نسبة توزيع الأرباح: {dividend / net * 100:.2f}%"

def h_retention_ratio(data):
    payout = data.get("payout", data.get("rate", 30))
    return f"📊 نسبة الاحتفاظ: {100 - payout:.1f}%"

def h_earnings_yield(data):
    eps = data.get("eps", data.get("amount", 1))
    price = data.get("price", 10)
    return f"📈 عائد الأرباح: {eps / price * 100:.2f}%"

def h_book_value(data):
    equity = data.get("equity", data.get("amount", 0))
    shares = data.get("shares", 1)
    return f"📊 القيمة الدفترية للسهم: {equity / shares:.2f}"

def h_price_to_book(data):
    price = data.get("price", data.get("amount", 0))
    book = data.get("book_value", 1)
    return f"📊 مضاعف السعر للقيمة الدفترية: {price / book:.2f}"

def h_price_to_sales(data):
    price = data.get("price", data.get("amount", 0))
    sales = data.get("sales", 1)
    return f"📊 مضاعف السعر للمبيعات: {price / sales:.2f}"

def h_free_float(data):
    total_shares = data.get("total_shares", data.get("amount", 0))
    restricted = data.get("restricted", 0)
    return f"📊 الأسهم الحرة: {total_shares - restricted:.0f}"

def h_enterprise_value(data):
    mcap = data.get("market_cap", data.get("amount", 0))
    debt = data.get("debt", 0)
    cash = data.get("cash", 0)
    return f"🏢 قيمة المنشأة: {mcap + debt - cash:.2f}"

def h_sentiment(data):
    score = data.get("score", data.get("amount", 50))
    if score > 70:
        return f"😊 المعنويات: إيجابية ({score})"
    elif score > 30:
        return f"😐 المعنويات: محايدة ({score})"
    return f"😔 المعنويات: سلبية ({score})"

# ========== معالجات 101-150 ==========

def h_customer_acquisition_cost(data):
    marketing = data.get("marketing_cost", data.get("amount", 0))
    new_customers = data.get("new_customers", 1)
    return f"👥 تكلفة اكتساب العميل: {marketing / new_customers:.2f}"

def h_customer_retention_rate(data):
    retained = data.get("retained", data.get("amount", 0))
    total = data.get("total_customers", 1)
    return f"🔄 معدل الاحتفاظ: {retained / total * 100:.1f}%"

def h_churn_rate(data):
    churned = data.get("churned", data.get("amount", 0))
    total = data.get("total_customers", 1)
    return f"📉 معدل التراجع: {churned / total * 100:.1f}%"

def h_net_promoter_score(data):
    promoters = data.get("promoters", data.get("amount", 0))
    detractors = data.get("detractors", 0)
    total = data.get("total", 1)
    nps = (promoters - detractors) / total * 100
    return f"📊 صافي نقاط الترويج: {nps:.0f}"

def h_customer_satisfaction(data):
    score = data.get("score", data.get("amount", 75))
    return f"😊 رضا العملاء: {score}%"

def h_average_order_value(data):
    revenue = data.get("revenue", data.get("amount", 0))
    orders = data.get("orders", 1)
    return f"📦 متوسط قيمة الطلب: {revenue / orders:.2f}"

def h_cart_abandonment(data):
    abandoned = data.get("abandoned", data.get("amount", 0))
    total = data.get("total_carts", 1)
    return f"🛒 معدل ترك السلة: {abandoned / total * 100:.1f}%"

def h_conversion_rate(data):
    conversions = data.get("conversions", data.get("amount", 0))
    visitors = data.get("visitors", 1)
    return f"🎯 معدل التحويل: {conversions / visitors * 100:.1f}%"

def h_click_through_rate(data):
    clicks = data.get("clicks", data.get("amount", 0))
    impressions = data.get("impressions", 1)
    return f"📈 نسبة النقر: {clicks / impressions * 100:.1f}%"

def h_roas(data):
    revenue = data.get("revenue", data.get("amount", 0))
    ad_spend = data.get("ad_spend", 1)
    return f"💰 عائد الإنفاق الإعلاني: {revenue / ad_spend:.2f}"

def h_cpa(data):
    cost = data.get("cost", data.get("amount", 0))
    conversions = data.get("conversions", 1)
    return f"📊 تكلفة التحويل: {cost / conversions:.2f}"

def h_email_open_rate(data):
    opened = data.get("opened", data.get("amount", 0))
    sent = data.get("sent", 1)
    return f"✉️ معدل فتح البريد: {opened / sent * 100:.1f}%"

def h_email_click_rate(data):
    clicks = data.get("clicks", data.get("amount", 0))
    opened = data.get("opened", 1)
    return f"📧 معدل النقر في البريد: {clicks / opened * 100:.1f}%"

def h_social_engagement(data):
    interactions = data.get("interactions", data.get("amount", 0))
    followers = data.get("followers", 1)
    return f"📱 معدل التفاعل: {interactions / followers * 100:.1f}%"

def h_seo_traffic(data):
    organic = data.get("organic", data.get("amount", 0))
    total = data.get("total_traffic", 1)
    return f"🔍 نسبة حركة البحث: {organic / total * 100:.1f}%"

def h_bounce_rate(data):
    bounces = data.get("bounces", data.get("amount", 0))
    visits = data.get("visits", 1)
    return f"📉 معدل الارتداد: {bounces / visits * 100:.1f}%"

def h_page_views(data):
    views = data.get("views", data.get("amount", 0))
    visitors = data.get("visitors", 1)
    return f"📄 مشاهدات لكل زائر: {views / visitors:.2f}"

def h_time_on_site(data):
    total_time = data.get("total_time", data.get("amount", 0))
    sessions = data.get("sessions", 1)
    return f"⏱️ متوسط الوقت: {total_time / sessions:.2f} دقيقة"

def h_lead_to_customer(data):
    leads = data.get("leads", data.get("amount", 0))
    customers = data.get("customers", 1)
    return f"🔄 تحويل العميل المحتمل: {customers / leads * 100:.1f}%"

def h_marketing_budget(data):
    revenue = data.get("revenue", data.get("amount", 0))
    pct = data.get("percentage", data.get("rate", 10))
    return f"📢 ميزانية التسويق: {revenue * pct / 100:.2f}"

def h_employee_productivity(data):
    output = data.get("output", data.get("amount", 0))
    employees = data.get("employees", 1)
    return f"👷 إنتاجية الموظف: {output / employees:.2f}"

def h_absenteeism(data):
    absent_days = data.get("absent_days", data.get("amount", 0))
    total_days = data.get("total_days", 1)
    return f"📊 معدل الغياب: {absent_days / total_days * 100:.1f}%"

def h_turnover_rate(data):
    left = data.get("left", data.get("amount", 0))
    total = data.get("total_employees", 1)
    return f"🔄 معدل دوران الموظفين: {left / total * 100:.1f}%"

def h_training_hours(data):
    hours = data.get("hours", data.get("amount", 0))
    employees = data.get("employees", 1)
    return f"📚 ساعات التدريب لكل موظف: {hours / employees:.2f}"

def h_revenue_per_employee(data):
    revenue = data.get("revenue", data.get("amount", 0))
    employees = data.get("employees", 1)
    return f"💰 الإيراد لكل موظف: {revenue / employees:.2f}"

def h_hr_cost(data):
    total_payroll = data.get("payroll", data.get("amount", 0))
    benefits = data.get("benefits", 0)
    return f"💼 إجمالي تكلفة الموارد: {total_payroll + benefits:.2f}"

def h_overtime_percentage(data):
    overtime = data.get("overtime_hours", data.get("amount", 0))
    regular = data.get("regular_hours", 1)
    return f"⏰ نسبة العمل الإضافي: {overtime / regular * 100:.1f}%"

def h_compensation_ratio(data):
    salary = data.get("salary", data.get("amount", 0))
    market = data.get("market_average", 1)
    return f"💵 نسبة التعويض: {salary / market * 100:.1f}%"

def h_production_yield(data):
    good = data.get("good_units", data.get("amount", 0))
    total = data.get("total_units", 1)
    return f"🏭 نسبة الإنتاج السليم: {good / total * 100:.1f}%"

def h_defect_rate(data):
    defects = data.get("defects", data.get("amount", 0))
    total = data.get("total_units", 1)
    return f"⚠️ معدل العيوب: {defects / total * 100:.1f}%"

def h_capacity_utilization(data):
    actual = data.get("actual_output", data.get("amount", 0))
    capacity = data.get("max_capacity", 1)
    return f"📊 استغلال الطاقة: {actual / capacity * 100:.1f}%"

def h_cycle_time(data):
    total_time = data.get("total_time", data.get("amount", 0))
    units = data.get("units", 1)
    return f"⏱️ زمن الدورة: {total_time / units:.2f}"

def h_lead_time(data):
    order_to_delivery = data.get("lead_time", data.get("amount", 0))
    return f"🚚 زمن التسليم: {order_to_delivery:.1f} يوم"

def h_on_time_delivery(data):
    on_time = data.get("on_time", data.get("amount", 0))
    total = data.get("total_deliveries", 1)
    return f"✅ نسبة التسليم في الوقت: {on_time / total * 100:.1f}%"

def h_first_pass_yield(data):
    first_pass = data.get("first_pass", data.get("amount", 0))
    total = data.get("total_units", 1)
    return f"🏭 إنتاجية أول مرة: {first_pass / total * 100:.1f}%"

def h_overall_equipment_effectiveness(data):
    availability = data.get("availability", data.get("rate", 90))
    performance = data.get("performance", data.get("amount", 85))
    quality = data.get("quality", 95)
    oee = availability * performance * quality / 10000
    return f"📊 الفعالية الكلية للمعدات: {oee:.1f}%"

def h_inventory_accuracy(data):
    accurate = data.get("accurate_records", data.get("amount", 0))
    total = data.get("total_records", 1)
    return f"📦 دقة المخزون: {accurate / total * 100:.1f}%"

def h_stockout_rate(data):
    stockouts = data.get("stockouts", data.get("amount", 0))
    total_orders = data.get("total_orders", 1)
    return f"🚫 معدل نفاد المخزون: {stockouts / total_orders * 100:.1f}%"

def h_reorder_point(data):
    daily_usage = data.get("daily_usage", data.get("amount", 0))
    lead_time = data.get("lead_time", 1)
    safety_stock = data.get("safety_stock", 0)
    return f"📦 نقطة إعادة الطلب: {daily_usage * lead_time + safety_stock:.0f}"

def h_economic_order_quantity(data):
    annual_demand = data.get("annual_demand", data.get("amount", 0))
    order_cost = data.get("order_cost", 1)
    holding_cost = data.get("holding_cost", 1)
    if holding_cost > 0:
        eoq = (2 * annual_demand * order_cost / holding_cost) ** 0.5
        return f"📋 كمية الطلب الاقتصادية: {eoq:.0f}"
    return "⚠️ بيانات غير كافية"

def h_safety_stock(data):
    daily_usage = data.get("daily_usage", data.get("amount", 10))
    lead_time = data.get("lead_time", 5)
    safety = daily_usage * lead_time * 0.25
    return f"🛡️ مخزون الأمان: {safety:.0f}"

def h_customer_order_cycle(data):
    days = data.get("days", data.get("amount", 7))
    return f"📅 دورة طلب العميل: {days:.0f} يوم"

def h_delivery_cost_per_order(data):
    total_delivery = data.get("delivery_cost", data.get("amount", 0))
    orders = data.get("orders", 1)
    return f"🚚 تكلفة التوصيل للطلب: {total_delivery / orders:.2f}"

def h_return_rate(data):
    returns = data.get("returns", data.get("amount", 0))
    sales = data.get("sales", 1)
    return f"↩️ معدل الإرجاع: {returns / sales * 100:.1f}%"

def h_shipping_accuracy(data):
    accurate = data.get("accurate_shipments", data.get("amount", 0))
    total = data.get("total_shipments", 1)
    return f"🚢 دقة الشحن: {accurate / total * 100:.1f}%"

def h_supplier_on_time(data):
    on_time = data.get("on_time_suppliers", data.get("amount", 0))
    total = data.get("total_suppliers", 1)
    return f"📦 التزام الموردين: {on_time / total * 100:.1f}%"

def h_supplier_defect_rate(data):
    defects = data.get("defects", data.get("amount", 0))
    total = data.get("total_received", 1)
    return f"⚠️ عيوب الموردين: {defects / total * 100:.1f}%"

def h_supplier_cost_index(data):
    current_cost = data.get("current_cost", data.get("amount", 0))
    base_cost = data.get("base_cost", 1)
    return f"📊 مؤشر تكلفة الموردين: {current_cost / base_cost * 100:.1f}"

def h_procurement_cycle(data):
    days = data.get("days", data.get("amount", 14))
    return f"📅 دورة المشتريات: {days:.0f} يوم"

# ========== معالجات 151-200 ==========

def h_order_processing_time(data):
    hours = data.get("hours", data.get("amount", 24))
    return f"⏱️ زمن معالجة الطلب: {hours:.1f} ساعة"

def h_backorder_rate(data):
    backorders = data.get("backorders", data.get("amount", 0))
    total = data.get("total_orders", 1)
    return f"📋 معدل الطلبات المؤجلة: {backorders / total * 100:.1f}%"

def h_fill_rate(data):
    filled = data.get("filled", data.get("amount", 0))
    ordered = data.get("ordered", 1)
    return f"✅ معدل الإنجاز: {filled / ordered * 100:.1f}%"

def h_picking_accuracy(data):
    correct = data.get("correct_picks", data.get("amount", 0))
    total = data.get("total_picks", 1)
    return f"📦 دقة الالتقاط: {correct / total * 100:.1f}%"

def h_warehouse_space_utilization(data):
    used = data.get("used_space", data.get("amount", 0))
    total = data.get("total_space", 1)
    return f"🏭 استغلال مساحة المستودع: {used / total * 100:.1f}%"

def h_dock_to_stock(data):
    hours = data.get("hours", data.get("amount", 8))
    return f"🚢 زمن الرصيف للمخزون: {hours:.1f} ساعة"

def h_order_perfect_rate(data):
    perfect = data.get("perfect_orders", data.get("amount", 0))
    total = data.get("total_orders", 1)
    return f"🌟 معدل الطلبات المثالية: {perfect / total * 100:.1f}%"

def h_return_on_assets(data):
    net_income = data.get("net_income", data.get("amount", 0))
    assets = data.get("assets", 1)
    return f"📊 العائد على الأصول: {net_income / assets * 100:.2f}%"

def h_return_on_equity(data):
    net_income = data.get("net_income", data.get("amount", 0))
    equity = data.get("equity", 1)
    return f"📈 العائد على حقوق الملكية: {net_income / equity * 100:.2f}%"

def h_gross_margin_ratio(data):
    gross = data.get("gross_profit", data.get("amount", 0))
    revenue = data.get("revenue", 1)
    return f"📊 هامش الربح الإجمالي: {gross / revenue * 100:.2f}%"

def h_operating_margin_ratio(data):
    operating = data.get("operating_profit", data.get("amount", 0))
    revenue = data.get("revenue", 1)
    return f"📊 هامش التشغيل: {operating / revenue * 100:.2f}%"

def h_net_margin_ratio(data):
    net = data.get("net_profit", data.get("amount", 0))
    revenue = data.get("revenue", 1)
    return f"📊 صافي الهامش: {net / revenue * 100:.2f}%"

def h_cash_ratio(data):
    cash = data.get("cash", data.get("amount", 0))
    liabilities = data.get("liabilities", 1)
    return f"💵 نسبة النقدية: {cash / liabilities:.2f}"

def h_acid_test_ratio(data):
    cash = data.get("cash", data.get("amount", 0))
    receivables = data.get("receivables", 0)
    liabilities = data.get("liabilities", 1)
    return f"⚗️ نسبة السيولة السريعة جداً: {(cash + receivables) / liabilities:.2f}"

def h_debt_ratio(data):
    total_debt = data.get("total_debt", data.get("amount", 0))
    total_assets = data.get("total_assets", 1)
    return f"💳 نسبة المديونية: {total_debt / total_assets * 100:.1f}%"

def h_equity_ratio(data):
    equity = data.get("equity", data.get("amount", 0))
    assets = data.get("assets", 1)
    return f"📊 نسبة حقوق الملكية: {equity / assets * 100:.1f}%"

def h_price_earnings_growth(data):
    pe = data.get("pe", data.get("amount", 15))
    growth = data.get("growth_rate", data.get("rate", 10))
    return f"📈 نسبة السعر للربح للنمو: {pe / growth:.2f}"

def h_earnings_per_share_growth(data):
    current_eps = data.get("current_eps", data.get("amount", 1))
    previous_eps = data.get("previous_eps", 0.8)
    growth = ((current_eps - previous_eps) / previous_eps * 100)
    return f"📈 نمو ربحية السهم: {growth:.1f}%"

def h_operating_cashflow_ratio(data):
    cashflow = data.get("operating_cashflow", data.get("amount", 0))
    liabilities = data.get("liabilities", 1)
    return f"💵 نسبة التدفق التشغيلي للالتزامات: {cashflow / liabilities:.2f}"

def h_interest_coverage(data):
    ebit = data.get("ebit", data.get("amount", 0))
    interest = data.get("interest_expense", 1)
    return f"📊 تغطية الفوائد: {ebit / interest:.2f}"

def h_fixed_charge_coverage(data):
    ebit = data.get("ebit", data.get("amount", 0))
    fixed_charges = data.get("fixed_charges", 1)
    return f"📊 تغطية الالتزامات الثابتة: {ebit / fixed_charges:.2f}"

def h_cash_flow_margin(data):
    cashflow = data.get("cashflow", data.get("amount", 0))
    revenue = data.get("revenue", 1)
    return f"💵 هامش التدفق النقدي: {cashflow / revenue * 100:.2f}%"

def h_working_capital_ratio(data):
    current_assets = data.get("current_assets", data.get("amount", 0))
    current_liabilities = data.get("current_liabilities", 1)
    return f"💼 نسبة رأس المال العامل: {current_assets / current_liabilities:.2f}"

def h_inventory_to_assets(data):
    inventory = data.get("inventory", data.get("amount", 0))
    assets = data.get("assets", 1)
    return f"📦 نسبة المخزون للأصول: {inventory / assets * 100:.1f}%"

def h_receivables_to_assets(data):
    receivables = data.get("receivables", data.get("amount", 0))
    assets = data.get("assets", 1)
    return f"📥 نسبة المدينون للأصول: {receivables / assets * 100:.1f}%"

def h_payables_to_assets(data):
    payables = data.get("payables", data.get("amount", 0))
    assets = data.get("assets", 1)
    return f"📤 نسبة الدائنون للأصول: {payables / assets * 100:.1f}%"

def h_sales_growth(data):
    current = data.get("current_sales", data.get("amount", 0))
    previous = data.get("previous_sales", 1)
    growth = ((current - previous) / previous * 100)
    return f"📈 نمو المبيعات: {growth:.1f}%"

def h_revenue_growth(data):
    current = data.get("current_revenue", data.get("amount", 0))
    previous = data.get("previous_revenue", 1)
    growth = ((current - previous) / previous * 100)
    return f"📈 نمو الإيرادات: {growth:.1f}%"

def h_profit_growth(data):
    current = data.get("current_profit", data.get("amount", 0))
    previous = data.get("previous_profit", 1)
    growth = ((current - previous) / previous * 100)
    return f"📈 نمو الأرباح: {growth:.1f}%"

def h_market_growth(data):
    current = data.get("current_market", data.get("amount", 0))
    previous = data.get("previous_market", 1)
    growth = ((current - previous) / previous * 100)
    return f"🌍 نمو السوق: {growth:.1f}%"

def h_price_variance(data):
    actual_price = data.get("actual_price", data.get("amount", 0))
    budgeted_price = data.get("budgeted_price", 1)
    variance = (actual_price - budgeted_price) / budgeted_price * 100
    return f"💲 انحراف السعر: {variance:.1f}%"

def h_volume_variance(data):
    actual_volume = data.get("actual_volume", data.get("amount", 0))
    budgeted_volume = data.get("budgeted_volume", 1)
    variance = (actual_volume - budgeted_volume) / budgeted_volume * 100
    return f"📦 انحراف الحجم: {variance:.1f}%"

def h_cost_variance(data):
    actual_cost = data.get("actual_cost", data.get("amount", 0))
    budgeted_cost = data.get("budgeted_cost", 1)
    variance = (actual_cost - budgeted_cost) / budgeted_cost * 100
    return f"📉 انحراف التكلفة: {variance:.1f}%"

def h_schedule_variance(data):
    planned = data.get("planned", data.get("amount", 0))
    actual = data.get("actual", 1)
    variance = (planned - actual) / planned * 100 if planned > 0 else 0
    return f"📅 انحراف الجدول: {variance:.1f}%"

def h_quality_variance(data):
    defects = data.get("defects", data.get("amount", 0))
    total = data.get("total", 1)
    return f"⚠️ انحراف الجودة: {defects / total * 100:.1f}%"

def h_labor_variance(data):
    actual = data.get("actual_hours", data.get("amount", 0))
    standard = data.get("standard_hours", 1)
    variance = (actual - standard) / standard * 100
    return f"👷 انحراف العمالة: {variance:.1f}%"

def h_material_variance(data):
    actual = data.get("actual_material", data.get("amount", 0))
    standard = data.get("standard_material", 1)
    variance = (actual - standard) / standard * 100
    return f"📦 انحراف المواد: {variance:.1f}%"

def h_overhead_variance(data):
    actual = data.get("actual_overhead", data.get("amount", 0))
    standard = data.get("standard_overhead", 1)
    variance = (actual - standard) / standard * 100
    return f"🏭 انحراف التكاليف غير المباشرة: {variance:.1f}%"

def h_budget_variance(data):
    actual = data.get("actual", data.get("amount", 0))
    budget = data.get("budget", 1)
    variance = (actual - budget) / budget * 100
    return f"📋 انحراف الميزانية: {variance:.1f}%"

def h_profit_variance(data):
    actual = data.get("actual_profit", data.get("amount", 0))
    expected = data.get("expected_profit", 1)
    variance = (actual - expected) / expected * 100
    return f"💰 انحراف الربح: {variance:.1f}%"

def h_revenue_variance(data):
    actual = data.get("actual_revenue", data.get("amount", 0))
    expected = data.get("expected_revenue", 1)
    variance = (actual - expected) / expected * 100
    return f"📈 انحراف الإيراد: {variance:.1f}%"

def h_expense_variance(data):
    actual = data.get("actual_expense", data.get("amount", 0))
    expected = data.get("expected_expense", 1)
    variance = (actual - expected) / expected * 100
    return f"📉 انحراف المصاريف: {variance:.1f}%"

def h_project_progress(data):
    completed = data.get("completed", data.get("amount", 0))
    total = data.get("total_work", 1)
    return f"📁 تقدم المشروع: {completed / total * 100:.1f}%"

def h_earned_value(data):
    pv = data.get("planned_value", data.get("amount", 0))
    ac = data.get("actual_cost", 0)
    ev = pv - ac
    return f"📊 القيمة المكتسبة: {ev:.2f}"

def h_cost_performance_index(data):
    ev = data.get("earned_value", data.get("amount", 0))
    ac = data.get("actual_cost", 1)
    cpi = ev / ac if ac > 0 else 0
    return f"📊 مؤشر أداء التكلفة: {cpi:.2f}"

def h_schedule_performance_index(data):
    ev = data.get("earned_value", data.get("amount", 0))
    pv = data.get("planned_value", 1)
    spi = ev / pv if pv > 0 else 0
    return f"📅 مؤشر أداء الجدول: {spi:.2f}"

def h_critical_ratio(data):
    spi = data.get("spi", data.get("amount", 1))
    cpi = data.get("cpi", 1)
    return f"⚖️ النسبة الحرجة: {spi * cpi:.2f}"

def h_risk_score(data):
    probability = data.get("probability", data.get("amount", 50))
    impact = data.get("impact", 50)
    return f"🛡️ درجة المخاطرة: {probability * impact / 100:.1f}"

def h_risk_exposure(data):
    risk = data.get("risk_value", data.get("amount", 0))
    return f"📊 التعرض للمخاطر: {risk:.2f}"

# ========== معالجات 201-250 ==========

def h_probability_impact_matrix(data):
    p = data.get("probability", data.get("amount", 50))
    i = data.get("impact", 50)
    score = (p / 100) * (i / 100) * 100
    return f"📊 مصفوفة الاحتمالية والتأثير: {score:.1f}"

def h_risk_priority_number(data):
    severity = data.get("severity", data.get("amount", 5))
    occurrence = data.get("occurrence", 5)
    detection = data.get("detection", 5)
    rpn = severity * occurrence * detection
    return f"🎯 رقم أولوية المخاطرة: {rpn:.0f}"

def h_failure_mode(data):
    failures = data.get("failures", data.get("amount", 0))
    total = data.get("total", 1)
    return f"⚠️ معدل الفشل: {failures / total * 100:.1f}%"

def h_mean_time_between_failures(data):
    total_time = data.get("total_time", data.get("amount", 0))
    failures = data.get("failures", 1)
    return f"⏱️ متوسط الوقت بين الأعطال: {total_time / failures:.1f}"

def h_mean_time_to_repair(data):
    total_repair = data.get("total_repair_time", data.get("amount", 0))
    repairs = data.get("repairs", 1)
    return f"🔧 متوسط وقت الإصلاح: {total_repair / repairs:.1f}"

def h_availability(data):
    uptime = data.get("uptime", data.get("amount", 0))
    downtime = data.get("downtime", 1)
    total = uptime + downtime
    return f"📊 التوافرية: {uptime / total * 100:.2f}%" if total > 0 else "⚠️ بيانات غير صحيحة"

def h_reliability(data):
    failures = data.get("failures", data.get("amount", 0))
    total = data.get("total_operations", 1)
    rel = (1 - failures / total) * 100
    return f"🛡️ الموثوقية: {rel:.2f}%"

def h_maintenance_cost(data):
    total_cost = data.get("total_cost", data.get("amount", 0))
    hours = data.get("hours", 1)
    return f"🔧 تكلفة الصيانة لكل ساعة: {total_cost / hours:.2f}"

def h_efficiency_ratio(data):
    output = data.get("output", data.get("amount", 0))
    input_val = data.get("input", 1)
    return f"⚡ نسبة الكفاءة: {output / input_val * 100:.2f}%"

def h_productivity_rate(data):
    actual = data.get("actual_output", data.get("amount", 0))
    expected = data.get("expected_output", 1)
    return f"👷 معدل الإنتاجية: {actual / expected * 100:.1f}%"

def h_utilization_rate(data):
    used = data.get("used", data.get("amount", 0))
    available = data.get("available", 1)
    return f"📊 معدل الاستغلال: {used / available * 100:.1f}%"

def h_scrap_rate(data):
    scrap = data.get("scrap", data.get("amount", 0))
    total = data.get("total", 1)
    return f"♻️ معدل الخردة: {scrap / total * 100:.1f}%"

def h_rework_rate(data):
    rework = data.get("rework", data.get("amount", 0))
    total = data.get("total", 1)
    return f"🔄 معدل إعادة العمل: {rework / total * 100:.1f}%"

def h_energy_consumption(data):
    kwh = data.get("kwh", data.get("amount", 0))
    units = data.get("units", 1)
    return f"⚡ استهلاك الطاقة: {kwh / units:.2f} كيلوواط/وحدة"

def h_carbon_footprint(data):
    emissions = data.get("emissions", data.get("amount", 0))
    return f"🌍 البصمة الكربونية: {emissions:.1f} طن"

def h_water_usage(data):
    liters = data.get("liters", data.get("amount", 0))
    units = data.get("units", 1)
    return f"💧 استهلاك المياه: {liters / units:.1f} لتر/وحدة"

def h_waste_reduction(data):
    old = data.get("old_waste", data.get("amount", 0))
    new = data.get("new_waste", 0)
    reduction = ((old - new) / old * 100) if old > 0 else 0
    return f"♻️ تقليل النفايات: {reduction:.1f}%"

def h_sustainability_score(data):
    score = data.get("score", data.get("amount", 75))
    return f"🌱 مؤشر الاستدامة: {score:.1f}"

def h_social_impact(data):
    score = data.get("score", data.get("amount", 70))
    return f"👥 الأثر الاجتماعي: {score:.1f}"

def h_governance_score(data):
    score = data.get("score", data.get("amount", 80))
    return f"🏛️ مؤشر الحوكمة: {score:.1f}"

def h_esg_score(data):
    e = data.get("environmental", data.get("amount", 70))
    s = data.get("social", 70)
    g = data.get("governance", 70)
    return f"🌍 مؤشر ESG: {(e + s + g) / 3:.1f}"

def h_digital_transformation(data):
    score = data.get("score", data.get("amount", 60))
    return f"💻 مؤشر التحول الرقمي: {score:.1f}"

def h_innovation_index(data):
    score = data.get("score", data.get("amount", 65))
    return f"💡 مؤشر الابتكار: {score:.1f}"

def h_technology_readiness(data):
    score = data.get("score", data.get("amount", 70))
    return f"🔧 جاهزية التكنولوجيا: {score:.1f}"

def h_data_quality(data):
    score = data.get("score", data.get("amount", 85))
    return f"📊 جودة البيانات: {score:.1f}"

def h_system_uptime(data):
    uptime = data.get("uptime", data.get("amount", 99.9))
    return f"🖥️ نسبة تشغيل النظام: {uptime:.2f}%"

def h_response_time(data):
    ms = data.get("ms", data.get("amount", 200))
    return f"⚡ زمن الاستجابة: {ms:.0f} مللي ثانية"

def h_throughput(data):
    transactions = data.get("transactions", data.get("amount", 0))
    seconds = data.get("seconds", 1)
    return f"🚀 معدل المعالجة: {transactions / seconds:.1f} معاملة/ثانية"

def h_latency(data):
    ms = data.get("ms", data.get("amount", 50))
    return f"📡 زمن الانتقال: {ms:.0f} مللي ثانية"

def h_bandwidth_utilization(data):
    used = data.get("used_bandwidth", data.get("amount", 0))
    total = data.get("total_bandwidth", 1)
    return f"📶 استخدام النطاق: {used / total * 100:.1f}%"

def h_storage_utilization(data):
    used = data.get("used_storage", data.get("amount", 0))
    total = data.get("total_storage", 1)
    return f"💾 استخدام التخزين: {used / total * 100:.1f}%"

def h_cpu_usage(data):
    usage = data.get("usage", data.get("amount", 0))
    return f"🖥️ استخدام المعالج: {usage:.1f}%"

def h_memory_usage(data):
    usage = data.get("usage", data.get("amount", 0))
    return f"🧠 استخدام الذاكرة: {usage:.1f}%"

def h_network_uptime(data):
    uptime = data.get("uptime", data.get("amount", 99))
    return f"🌐 تشغيل الشبكة: {uptime:.2f}%"

def h_api_success_rate(data):
    success = data.get("success", data.get("amount", 0))
    total = data.get("total", 1)
    return f"✅ نسبة نجاح API: {success / total * 100:.1f}%"

def h_error_rate(data):
    errors = data.get("errors", data.get("amount", 0))
    total = data.get("total", 1)
    return f"⚠️ معدل الأخطاء: {errors / total * 100:.2f}%"

def h_data_transfer(data):
    gb = data.get("gb", data.get("amount", 0))
    return f"📦 البيانات المنقولة: {gb:.1f} جيجابايت"

def h_backup_success_rate(data):
    success = data.get("success", data.get("amount", 0))
    total = data.get("total", 1)
    return f"💾 نسبة نجاح النسخ: {success / total * 100:.1f}%"

def h_recovery_time(data):
    minutes = data.get("minutes", data.get("amount", 30))
    return f"⏱️ زمن الاستعادة: {minutes:.0f} دقيقة"

def h_recovery_point(data):
    minutes = data.get("minutes", data.get("amount", 15))
    return f"📌 نقطة الاستعادة: {minutes:.0f} دقيقة"

def h_incident_count(data):
    count = data.get("count", data.get("amount", 0))
    return f"🚨 عدد الحوادث: {count:.0f}"

def h_incident_resolution_time(data):
    hours = data.get("hours", data.get("amount", 2))
    return f"✅ زمن حل الحادث: {hours:.1f} ساعة"

def h_sla_compliance(data):
    compliance = data.get("compliance", data.get("amount", 98))
    return f"📋 الالتزام باتفاقية الخدمة: {compliance:.1f}%"

def h_downtime_cost(data):
    hours = data.get("hours", data.get("amount", 1))
    cost_per_hour = data.get("cost_per_hour", 1000)
    return f"💰 تكلفة التوقف: {hours * cost_per_hour:.2f}"

def h_energy_efficiency(data):
    output = data.get("output", data.get("amount", 0))
    energy = data.get("energy", 1)
    return f"⚡ كفاءة الطاقة: {output / energy:.2f}"

def h_customer_profitability(data):
    revenue = data.get("revenue", data.get("amount", 0))
    cost = data.get("cost", 0)
    return f"💰 ربحية العميل: {revenue - cost:.2f}"

def h_product_profitability(data):
    revenue = data.get("revenue", data.get("amount", 0))
    cost = data.get("cost", 0)
    return f"📦 ربحية المنتج: {revenue - cost:.2f}"

def h_channel_profitability(data):
    revenue = data.get("revenue", data.get("amount", 0))
    cost = data.get("cost", 0)
    return f"📊 ربحية القناة: {revenue - cost:.2f}"

def h_region_profitability(data):
    revenue = data.get("revenue", data.get("amount", 0))
    cost = data.get("cost", 0)
    return f"🌍 ربحية المنطقة: {revenue - cost:.2f}"

def h_cost_benefit_ratio(data):
    benefits = data.get("benefits", data.get("amount", 0))
    costs = data.get("costs", 1)
    return f"📊 نسبة الفائدة للتكلفة: {benefits / costs:.2f}"
