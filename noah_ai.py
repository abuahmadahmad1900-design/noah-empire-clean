# -*- coding: utf-8 -*-
"""
🤖 نوح AI — منصة الذكاء الاصطناعي الأسطورية
"""
from flask import Flask, request
import datetime

app = Flask(__name__)

STYLE = """
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:Tahoma; background:radial-gradient(ellipse at top,#0a0a2e,#000); min-height:100vh; color:#fff; }
.container { max-width:1200px; margin:0 auto; padding:40px 20px; }
.legendary-title { text-align:center; font-size:3em; font-weight:900; background:linear-gradient(135deg,#FFD700,#FFA500,#FFD700); -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-shadow:0 0 100px rgba(255,215,0,0.8); margin-bottom:30px; animation:glow 2s infinite; }
@keyframes glow { 0%,100%{filter:brightness(1)} 50%{filter:brightness(1.5)} }
.ai-box { background:rgba(20,20,60,0.9); border-radius:30px; padding:40px; border:2px solid #FFD700; box-shadow:0 0 80px rgba(255,215,0,0.3); margin:30px 0; }
.ai-input { width:70%; padding:20px 30px; border-radius:50px; border:2px solid #FFD700; background:#0a0a2e; color:#FFD700; font-size:1.2em; outline:none; }
.ai-btn { padding:18px 35px; border-radius:50px; border:2px solid #FFD700; background:linear-gradient(145deg,#1a1a4e,#0d0d2b); color:#FFD700; font-weight:900; font-size:1.1em; cursor:pointer; }
.ai-response { background:rgba(10,10,40,0.8); border-radius:20px; padding:30px; margin:20px 0; border:1px solid rgba(255,215,0,0.4); color:#fff; font-size:1.1em; line-height:1.8; }
.stat-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:20px; margin:30px 0; }
.stat-card { background:rgba(20,20,60,0.9); border-radius:20px; padding:25px; text-align:center; border:1px solid #FFD700; }
.stat-num { font-size:2em; font-weight:900; color:#FFD700; }
.stat-label { color:#ccc; margin-top:10px; }
</style>
"""

MEMORY = []
LEARNING_LOG = []

ENCYCLOPEDIA = {
    "الذكاء الاصطناعي": "مجال علمي يهدف لبناء أنظمة تفكر وتتعلم مثل البشر",
    "التعلم الآلي": "فرع من الذكاء الاصطناعي يتعلم من البيانات",
    "الشبكات العصبية": "نماذج مستوحاة من الدماغ البشري",
    "البيانات الضخمة": "كميات هائلة من البيانات تحتاج تحليلاً",
    "الحوسبة السحابية": "خدمات حاسوبية عبر الإنترنت",
    "البلوكشين": "سلسلة كتل مشفرة للمعاملات",
    "انترنت الأشياء": "أجهزة متصلة بالإنترنت",
    "الواقع المعزز": "دمج العالم الرقمي بالحقيقي",
    "الواقع الافتراضي": "عالم رقمي كامل",
    "الروبوتات": "آلات ذكية تنفذ مهام",
}


TASKS = []

def add_task(task):
    """مساعد شخصي — ينظم المهام"""
    TASKS.append({"task": task, "status": "قيد التنفيذ", "time": datetime.datetime.now().strftime("%H:%M")})
    return "تمت إضافة المهمة: " + task


def list_tasks():
    """عرض المهام"""
    if not TASKS:
        return "لا توجد مهام"
    result = []
    for i, t in enumerate(TASKS, 1):
        result.append(str(i) + ". " + t["task"] + " (" + t["status"] + ")")
    return "\n".join(result)


def writing_assistant(topic):
    """مساعد كتابة — يكتب رسائل ومقالات"""
    templates = {
        "رسالة": "عزيزي/عزيزتي،\n\nأتمنى أن يصلك هذا الخطاب وأنت بخير.\n\nأكتب إليك بخصوص " + topic + " وأود مناقشة هذا الموضوع المهم.\n\nمع خالص التحية والتقدير.",
        "مقال": "مقدمة:\n" + topic + " من المواضيع الحيوية في عصرنا.\n\nالعرض:\nهناك عدة جوانب مهمة لهذا الموضوع تستحق التحليل والدراسة.\n\nالخاتمة:\nفي النهاية، يبقى " + topic + " مجالاً خصبًا للتطوير.",
        "طلب": "أتقدم بطلبي بخصوص " + topic + "، آملاً من سيادتكم النظر فيه بعين الاعتبار.\n\nشاكراً حسن تعاونكم.",
    }
    for key, value in templates.items():
        if key in topic:
            return value
    return "سأكتب لك نصًا عن: " + topic


def creative_mode(topic):
    """وضع الإبداع — قصص وخيال"""
    stories = [
        "في عالم بعيد، كان هناك " + topic + " يغير مصير البشرية...",
        "حكاية " + topic + " بدأت في ليلة مظلمة مليئة بالأسرار...",
        "عندما ظهر " + topic + " لأول مرة، لم يتوقع أحد ما سيحدث...",
    ]
    import random
    return random.choice(stories)


def smart_advisor(topic):
    """مستشار ذكي — نصائح في كل المجالات"""
    advice = {
        "عمل": "طور مهاراتك يوميًا، وابنِ شبكة علاقات قوية، ولا تتوقف عن التعلم",
        "دراسة": "نظم وقتك، وركز على الفهم لا الحفظ، ومارس ما تتعلمه",
        "صحة": "نم جيدًا، واشرب ماء كافيًا، ومارس الرياضة بانتظام",
        "مال": "ادخر 20% من دخلك، واستثمر بحكمة، وتجنب الديون غير الضرورية",
        "علاقات": "استمع أكثر مما تتكلم، وكن صادقًا، واحترم مشاعر الآخرين",
        "تطوير": "اقرأ يوميًا، وتعلم مهارة جديدة كل شهر، وحدد أهدافك",
    }
    for key, value in advice.items():
        if key in topic:
            return value
    return "نصيحتي: فكر بإيجابية، وخطط جيدًا، ونفذ بثبات"


def idea_generator(topic):
    """مولّد أفكار — يبتكر أفكارًا جديدة"""
    ideas = {
        "مشروع": ["منصة تعليمية عربية", "تطبيق توصيل ذكي", "متجر منتجات رقمية", "خدمة استشارات أونلاين"],
        "تطبيق": ["تطبيق تنظيم المهام", "تطبيق تعلم اللغات", "تطبيق صحة ولياقة", "تطبيق ميزانية شخصية"],
        "محتوى": ["سلسلة تعليمية", "بودكاست أسبوعي", "قناة يوتيوب", "مدونة احترافية"],
        "تجارة": ["منتجات يدوية", "استيراد وتصدير", "تجارة إلكترونية", "خدمات استشارية"],
    }
    for key, value in ideas.items():
        if key in topic:
            import random
            return "أقترح عليك: " + random.choice(value)
    return "أفكار إبداعية: ابدأ بمشروع صغير، واختبر السوق، وتوسع تدريجيًا"


def deep_chat(topic):
    """محادثة عميقة — حوار فلسفي"""
    responses = {
        "حياة": "الحياة رحلة مليئة بالمعاني — كل يوم فرصة للتعلم والنمو",
        "موت": "الموت جزء من دورة الحياة — يذكرنا بقيمة كل لحظة",
        "حب": "الحب أقوى قوة في الوجود — يربط القلوب والعقول",
        "نجاح": "النجاح ليس نهاية الطريق — بل بداية رحلة جديدة",
        "فشل": "الفشل هو المعلم الأكبر — منه نتعلم أقوى الدروس",
        "وقت": "الوقت أثمن ما نملك — لا يعود أبدًا",
        "معرفة": "المعرفة نور — كلما تعلمت أكثر، أدركت كم لا أعرف",
        "حرية": "الحرية أثمن من الذهب — وهي مسؤولية قبل أن تكون حقًا",
    }
    for key, value in responses.items():
        if key in topic:
            return value
    return "سؤال عميق — دعني أفكر... " + topic


def remember(question, response):
    """ذاكرة طويلة المدى — يتذكر المحادثات"""
    MEMORY.append({"q": question, "r": response, "t": datetime.datetime.now().strftime("%H:%M")})
    if len(MEMORY) > 50:
        MEMORY.pop(0)


def learn(question):
    """تعلم مستمر — يسجل كل سؤال"""
    LEARNING_LOG.append(question)
    return "تعلمت سؤالاً جديدًا: " + question


AI_KNOWLEDGE = {
    "من انت": "أنا نوح AI — منصة الذكاء الاصطناعي الأسطورية لإمبراطورية نوح",
    "ماذا تفعل": "أحلل البيانات، أجب على الأسئلة، أتوقع المستقبل، وأتعلم من كل تفاعل",
    "قدراتك": "معالجة اللغة العربية، التحليل الذكي، التعلم المستمر، التنبؤ، الإبداع",
    "مبروك": "مبروك! أنت الآن تتحدث مع أقوى منصة AI عربية",
    "مرحبا": "أهلاً بك في نوح AI! أنا هنا لخدمتك",
    "شكرا": "العفو! أنا سعيد بمساعدتك",
}

def generate_text(topic):
    """مولّد نصوص — يكتب مقالات قصيرة"""
    templates = [
        "موضوع {topic} من أهم المواضيع في عصرنا الحالي. يتطلب فهمًا عميقًا ورؤية شاملة.",
        "عندما نتحدث عن {topic}، نجد أنفسنا أمام فرص وتحديات كبيرة تستحق الدراسة.",
        "يعتبر {topic} مجالًا واعدًا للمستقبل، ويستحق المزيد من الاهتمام والبحث.",
    ]
    import random
    return random.choice(templates).replace("{topic}", topic)


def get_ai_stats():
    """لوحة معلومات — إحصائيات المنصة"""
    stats = {
        "name": "نوح AI",
        "knowledge": len(AI_KNOWLEDGE),
        "capabilities": 6,
        "languages": "عربي + إنجليزي",
        "status": "يعمل بكفاءة",
        "uptime": "24/7"
    }
    return stats


def analyze_sentiment(text):
    """محلل مشاعر — يكتشف العواطف"""
    positive = ["حب", "فرح", "سعيد", "ممتاز", "رائع", "جميل", "نجاح", "مبروك"]
    negative = ["حزين", "غاضب", "سيء", "فشل", "مشكلة", "صعب", "ألم"]
    
    text_lower = text.lower()
    pos_count = sum(1 for w in positive if w in text_lower)
    neg_count = sum(1 for w in negative if w in text_lower)
    
    if pos_count > neg_count:
        return "إيجابي — أشعر بالسعادة معك!"
    elif neg_count > pos_count:
        return "سلبي — أنا هنا لمساعدتك"
    else:
        return "محايد — أنا معك"


def smart_translate(text):
    """مترجم ذكي — كلمات شائعة"""
    translations = {
        "مرحبا": "Hello",
        "شكرا": "Thank you",
        "كيف": "How",
        "حال": "are",
        "انت": "you",
        "انا": "I",
        "احب": "love",
        "سلام": "Peace",
    }
    words = text.split()
    translated = []
    for w in words:
        translated.append(translations.get(w, w))
    return " ".join(translated)


def ai_respond(question):
    q = question.lower()
    for key, value in AI_KNOWLEDGE.items():
        if key in q:
            return value
    for key, value in ENCYCLOPEDIA.items():
        if key in q:
            return value
    response = "فهمت سؤالك: " + question + " — أنا أتعلم باستمرار وسأصبح أقوى مع كل تفاعل."
    remember(question, response)
    return response

@app.route('/add-task', methods=['POST'])
def add_task_route():
    task = request.form.get('task', '')
    if task:
        result = add_task(task)
    else:
        result = "أرسل مهمة"
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>المهام</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">المساعد الشخصي</h1>'
    html += '<div class="ai-response">' + result + '</div>'
    html += '<a href="/list-tasks" style="padding:14px 30px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">عرض المهام</a> '
    html += '<a href="/" style="padding:14px 30px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">رجوع</a>'
    html += '</div></body></html>'
    return html


@app.route('/list-tasks')
def list_tasks_route():
    result = list_tasks()
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>المهام</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">قائمة المهام</h1>'
    html += '<div class="ai-response">' + result + '</div>'
    html += '<a href="/" style="padding:14px 30px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">رجوع</a>'
    html += '</div></body></html>'
    return html


@app.route('/writing', methods=['POST'])
def writing():
    topic = request.form.get('topic', '')
    if topic:
        result = writing_assistant(topic)
    else:
        result = "أرسل موضوعًا"
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>كتابة</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">مساعد الكتابة</h1>'
    html += '<div class="ai-response">' + result.replace(chr(10), '<br>') + '</div>'
    html += '<a href="/" style="padding:14px 30px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">رجوع</a>'
    html += '</div></body></html>'
    return html


@app.route('/creative', methods=['POST'])
def creative():
    topic = request.form.get('topic', '')
    if topic:
        result = creative_mode(topic)
    else:
        result = "أرسل موضوعًا"
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>إبداع</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">وضع الإبداع</h1>'
    html += '<div class="ai-response">' + result + '</div>'
    html += '<a href="/" style="padding:14px 30px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">رجوع</a>'
    html += '</div></body></html>'
    return html


@app.route('/advisor', methods=['POST'])
def advisor():
    topic = request.form.get('topic', '')
    if topic:
        result = smart_advisor(topic)
    else:
        result = "أرسل موضوعًا"
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>مستشار</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">المستشار الذكي</h1>'
    html += '<div class="ai-response">' + result + '</div>'
    html += '<a href="/" style="padding:14px 30px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">رجوع</a>'
    html += '</div></body></html>'
    return html


@app.route('/ideas', methods=['POST'])
def ideas():
    topic = request.form.get('topic', '')
    if topic:
        result = idea_generator(topic)
    else:
        result = "أرسل موضوعًا"
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>أفكار</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">مولّد الأفكار</h1>'
    html += '<div class="ai-response">' + result + '</div>'
    html += '<a href="/" style="padding:14px 30px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">رجوع</a>'
    html += '</div></body></html>'
    return html


@app.route('/deep-chat', methods=['POST'])
def deep_chat_route():
    topic = request.form.get('topic', '')
    if topic:
        result = deep_chat(topic)
    else:
        result = "أرسل موضوعًا"
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>محادثة عميقة</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">المحادثة العميقة</h1>'
    html += '<div class="ai-response">' + result + '</div>'
    html += '<a href="/" style="padding:14px 30px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">رجوع</a>'
    html += '</div></body></html>'
    return html


@app.route('/generate', methods=['POST'])
def generate():
    topic = request.form.get('topic', '')
    if topic:
        result = generate_text(topic)
    else:
        result = "أرسل موضوعًا"
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>توليد نصوص</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">النص المولد</h1>'
    html += '<div class="ai-response">' + result + '</div>'
    html += '<a href="/" style="padding:14px 30px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">رجوع</a>'
    html += '</div></body></html>'
    return html


@app.route('/stats')
def stats():
    s = get_ai_stats()
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>إحصائيات</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">لوحة المعلومات</h1>'
    html += '<div style="display:flex;justify-content:center;gap:15px;flex-wrap:wrap;">'
    for key, value in s.items():
        html += '<span class="stat-card"><div class="stat-num">' + str(value) + '</div><div class="stat-label">' + key + '</div></span>'
    html += '</div><br><a href="/" class="legendary-btn" style="padding:14px 30px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">رجوع</a></div></body></html>'
    return html


@app.route('/sentiment', methods=['POST'])
def sentiment():
    text = request.form.get('text', '')
    if text:
        result = analyze_sentiment(text)
    else:
        result = "أرسل نصًا"
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>تحليل المشاعر</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">نتيجة تحليل المشاعر</h1>'
    html += '<div class="ai-response">' + result + '</div>'
    html += '<a href="/" style="padding:14px 30px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">رجوع</a>'
    html += '</div></body></html>'
    return html


@app.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text', '')
    if text:
        result = smart_translate(text)
    else:
        result = "أرسل نصًا"
    html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>الترجمة</title>' + STYLE + '</head>'
    html += '<body><div class="container"><h1 class="legendary-title">نتيجة الترجمة</h1>'
    html += '<div class="ai-response">' + result + '</div>'
    html += '<a href="/" style="padding:14px 30px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">رجوع</a>'
    html += '</div></body></html>'
    return html


@app.route('/', methods=['GET', 'POST'])
def home():
    response = ""
    question = ""
    if request.method == 'POST':
        question = request.form.get('question', '')
        if question:
            response = ai_respond(question)
    
    return f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head>
    <meta charset="UTF-8"><title>🤖 نوح AI</title>{STYLE}</head>
    <body><div class="container">
        <h1 class="legendary-title">🤖 نوح AI</h1>
        <div class="stat-grid">
            <div class="stat-card"><div class="stat-num">∞</div><div class="stat-label">قدرات لا محدودة</div></div>
            <div class="stat-card"><div class="stat-num">24/7</div><div class="stat-label">يعمل دائمًا</div></div>
            <div class="stat-card"><div class="stat-num">283+</div><div class="stat-label">نوع معرفة</div></div>
            <div class="stat-card"><div class="stat-num">100%</div><div class="stat-label">عربي</div></div>
        </div>
        <div class="ai-box">
            <form method="POST" style="display:flex;gap:15px;flex-wrap:wrap;justify-content:center;">
                <input type="text" name="question" class="ai-input" placeholder="اسألني أي شيء..." required value="{question}">
                <button type="submit" class="ai-btn">🤖 اسأل نوح</button>
            </form>
        </div>
        {f'<div class="ai-response">{response}</div>' if response else ''}
        <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin:20px 0;">
            <a href="/stats" style="padding:12px 25px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">📊 لوحة المعلومات</a>
        </div>
        <div class="ai-box">
            <h2 style="color:#FFD700;text-align:center;margin-bottom:20px;">تحليل المشاعر</h2>
            <form method="POST" action="/sentiment" style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">
                <input type="text" name="text" class="ai-input" placeholder="اكتب نصًا لتحليل مشاعره..." required>
                <button type="submit" class="ai-btn">تحليل</button>
            </form>
        </div>
        <div class="ai-box">
            <h2 style="color:#FFD700;text-align:center;margin-bottom:20px;">المحادثة العميقة</h2>
            <form method="POST" action="/deep-chat" style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">
                <input type="text" name="topic" class="ai-input" placeholder="موضوع فلسفي: حياة، حب، نجاح..." required>
                <button type="submit" class="ai-btn">حوار</button>
            </form>
        </div>
        <div class="ai-box">
            <h2 style="color:#FFD700;text-align:center;margin-bottom:20px;">المساعد الشخصي</h2>
            <form method="POST" action="/add-task" style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">
                <input type="text" name="task" class="ai-input" placeholder="أضف مهمة..." required>
                <button type="submit" class="ai-btn">إضافة</button>
                <a href="/list-tasks" style="padding:18px 25px;border-radius:50px;border:2px solid #FFD700;background:linear-gradient(145deg,#1a1a4e,#0d0d2b);color:#FFD700;font-weight:900;text-decoration:none;">عرض المهام</a>
            </form>
        </div>
        <div class="ai-box">
            <h2 style="color:#FFD700;text-align:center;margin-bottom:20px;">توليد نصوص</h2>
            <form method="POST" action="/generate" style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">
                <input type="text" name="topic" class="ai-input" placeholder="اكتب موضوعًا..." required>
                <button type="submit" class="ai-btn">توليد</button>
            </form>
        </div>
        <div class="ai-box">
            <h2 style="color:#FFD700;text-align:center;margin-bottom:20px;">الترجمة الذكية</h2>
            <form method="POST" action="/translate" style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">
                <input type="text" name="text" class="ai-input" placeholder="اكتب نصًا للترجمة..." required>
                <button type="submit" class="ai-btn">ترجمة</button>
            </form>
        </div>
        <div class="ai-box">
            <h2 style="color:#FFD700;text-align:center;margin-bottom:20px;">المستشار الذكي</h2>
            <form method="POST" action="/advisor" style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">
                <input type="text" name="topic" class="ai-input" placeholder="عمل، دراسة، صحة، مال..." required>
                <button type="submit" class="ai-btn">نصيحة</button>
            </form>
        </div>
        <div class="ai-box">
            <h2 style="color:#FFD700;text-align:center;margin-bottom:20px;">مولّد الأفكار</h2>
            <form method="POST" action="/ideas" style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">
                <input type="text" name="topic" class="ai-input" placeholder="مشروع، تطبيق، محتوى..." required>
                <button type="submit" class="ai-btn">فكرة</button>
            </form>
        </div>
        <div class="ai-box">
            <h2 style="color:#FFD700;text-align:center;margin-bottom:20px;">مساعد الكتابة</h2>
            <form method="POST" action="/writing" style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">
                <input type="text" name="topic" class="ai-input" placeholder="رسالة، مقال، طلب..." required>
                <button type="submit" class="ai-btn">اكتب</button>
            </form>
        </div>
        <div class="ai-box">
            <h2 style="color:#FFD700;text-align:center;margin-bottom:20px;">وضع الإبداع</h2>
            <form method="POST" action="/creative" style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">
                <input type="text" name="topic" class="ai-input" placeholder="اكتب موضوعًا لقصتك..." required>
                <button type="submit" class="ai-btn">أبدع</button>
            </form>
        </div>
    </div></body></html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5063)
