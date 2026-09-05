```markdown
# ⚡ EventHub - Smart Event Check-In & Gate Management System

---

## 📖 نبذة عن المشروع
**EventHub** هو تطبيق ويب مبني باستخدام Django لإدارة البوابات وتنظيم الحضور في الفعاليات. يتيح للمنظمين مسح تذاكر الـ QR بسرعة، المزامنة اللحظية لحالة الحاضرين (بالداخل / بالخارج)، إدارة وتعديل السجلات، وتصدير واستيراد البيانات.

---

## ✨ المميزات الرئيسية

* **📊 لوحة تحكم وإحصائيات حية (Live Dashboard):**
  * حساب فوري لإجمالي المقيدين، المتواجدين بالداخل، والمتبقين بالخارج.
  * مؤشر بصري يوضح نسبة الحضور الفعلية تلقائياً دون الحاجة لتحديث الصفحة.

* **📷 عدسة المسح السريع (QR Scanner Engine):**
  * واجهة مسح للكاميرا مخصصة للبوابات للتحقق من صلاحية التذكرة وتسجيل الدخول/الخروج لحظياً (`camera_scanner.html`).

* **🔍 محرك بحث وفلترة ذكي (Smart Search & Filters):**
  * بحث فوري بناءً على الاسم، رقم الهاتف، البريد الإلكتروني، أو كود التذكرة.
  * فلترة السجلات حسب الحالة: **الجميع** | **بالداخل** | **بالخارج**.

* **🖨️ طباعة وإرسال التذاكر:**
  * دعم كامل للطباعة الحرارية السريعة (Thermal Printing) لطباعة التذاكر عند البوابات.
  * إرسال التذاكر وقوالب البريد الإلكتروني (`ticket_email.html`) والمشاركة عبر **WhatsApp**.
  * توليد وحفظ صور الـ QR Code تلقائياً داخل المجلد الإعلامي للمشروع.

* **📁 إدارة واستيراد/تصدير البيانات:**
  * استيراد قوائم المدعوين دفعة واحدة عبر ملفات **Excel / CSV**.
  * تصدير التقرير الحالي لبيانات الحضور بصيغة **CSV**.
  * إضافة، تعديل، وحذف الحاضرين فوريًا عبر طلبات AJAX مع دعم حماية CSRF.

---

## 🛠️ التقنيات المستخدمة (Tech Stack)

### Backend
* **Python 3.x**
* **Django Framework**
* **SQLite3**

### Frontend
* **HTML5 / CSS3** (Cyberpunk Theme)
* **JavaScript (Vanilla JS / Fetch API)**
* **FontAwesome 6.5**
* **Google Cairo Font**

---

## 📂 هيكلية المشروع (Project Structure)

```text
eventhub/
├── app1/                        # التطبيق الرئيسي للفعاليات
│   ├── migrations/              # تهيئة وترحيل قاعدة البيانات
│   ├── templates/               # قوالب HTML الخاصة بالتطبيق
│   │   ├── camera_scanner.html  # واجهة مسح الـ QR عبر الكاميرا
│   │   ├── event_dashboard.html # لوحة التحكم الرئيسية والتحضير
│   │   └── ticket_email.html    # قالب البريد الإلكتروني للتذكرة
│   ├── admin.py                 # لوحة إشراف Django Admin
│   ├── apps.py                  # إعدادات التطبيق
│   ├── models.py                # نماذج الفعاليات والحاضرين (Events & Attendees)
│   ├── tests.py                 # الاختبارات البرمجية
│   ├── urls.py                  # مسارات التطبيق الفرعية
│   └── views.py                 # معالجة منطق التحكم والـ APIs
├── core/                        # المجلد الرئيسي لإعدادات المشروع
│   ├── asgi.py                  # إعدادات ASGI
│   ├── settings.py              # إعدادات Django الرئيسية
│   ├── urls.py                  # توجيه المسارات العامة للمشروع
│   └── wsgi.py                  # إعدادات WSGI
├── media/                       # الملفات المرفوعة والمولدة
│   └── qr_codes/                # صور أكواد الـ QR الخاصة بالمدعوين
├── db.sqlite3                   # قاعدة بيانات المشروع
├── manage.py                    # أداة إدارة مشروع Django
└── .gitignore                   # استبعاد الملفات غير المرغوبة من Git

```

---

## 🚀 طريقة التشغيل والتهيئة المحلية

### 1. استكشاط المشروع وتفعيل البيئة الافتراضية

```bash
git clone https://github.com/your-username/eventhub.git
cd eventhub

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

```

### 2. تثبيت الحزم البرمجية المطلوبة

```bash
pip install django qrcode pillow pandas openpyxl

```

### 3. تطبيق الهجرات وقاعدة البيانات

```bash
python manage.py makemigrations
python manage.py migrate

```

### 4. تشغيل خادم التطوير

```bash
python manage.py runserver

```

---

## 📡 مسارات العمليات والـ URLs الرئيسية (app1)

| المسار (Path) | الوظيفة |
| --- | --- |
| `/<event_id>/dashboard/` | عرض لوحة التحكم وإحصائيات الفعالية |
| `/<event_id>/scanner/` | فتح عدسة المسح بالكاميرا (`camera_scanner.html`) |
| `/attendee/<ticket_code>/toggle/` | تبديل حالة الحضور (داخل / خارج) |
| `/attendee/<id>/update/` | تعديل بيانات الحاضر |
| `/attendee/<id>/delete/` | حذف الحاضر نهائياً |
| `/attendee/import/` | استيراد ملفات Excel/CSV |

```

```
