الهيكل واضح تماماً! المشروع عبارة عن تطبيق **Django** باسم **`eventhub`** يحتوي على تطبيق رئيسي باسم **`app1`** مع إعدادات المشروع في مجلد **`core`** ونظام لتوليد وحفظ رموز **QR Code** وإرسال التذاكر عبر البريد الإلكتروني.

إليك ملف **`README.md`** مصمم بشكل احترافي ومتناسق تماماً مع المجلدات والملفات الموضحة في الصورة:

---

```markdown
# 🎟️ EventHub

**EventHub** هو تطبيق ويب متكامل مبني باستخدام إطار العمل **Django** لإدارة الفعاليات والتذاكر الإلكترونية. يتيح النظام إنشاء الفعاليات، توليد رموز QR فريدة لكل تذكرة، إرسال التذاكر عبر البريد الإلكتروني، وفحص التذاكر باستخدام كاميرا الجهاز عبر شاشة الماسح الضوئي.

---

## 🌟 المميزات الرئيسية (Features)

* **لوحة تحكم الفعاليات (Event Dashboard):** استعراض وإدارة جميع الفعاليات المسجلة والحالات الخاصة بكل فعالية.
* **توليد رموز QR تلقائياً:** إنشاء وحفظ رموز QR فريدة للتذاكر في المجلد المخصص (`media/qr_codes`).
* **إرسال التذاكر عبر البريد:** قوالب جاهزة لإرسال التذاكر والمستندات مباشرة إلى بريد المستخدمين الإلكتروني (`ticket_email.html`).
* **مسح التذاكر عبر الكاميرا (Camera Scanner):** واجهة مخصصة تفحص رموز QR مباشرة باستخدام كاميرا الويب أو الجوال لحظر التذاكر المكررة أو غير الصالحة.

---

## 📂 هيكل المشروع (Project Structure)

```text
eventhub/
│
├── app1/                     # التطبيق الرئيسي للعمليات
│   ├── migrations/           # ترحيلات قاعدة البيانات
│   ├── templates/            # قوالب HTML
│   │   ├── camera_scanner.html    # شاشة فحص الـ QR بالكاميرا
│   │   ├── event_dashboard.html   # لوحة تحكم الفعاليات
│   │   └── ticket_email.html      # قالب إرسال التذكرة للإيميل
│   ├── admin.py              # إعدادات لوحة التحكم
│   ├── models.py             # نماذج قاعدة البيانات (Events, Tickets, etc.)
│   ├── urls.py               # المسارات الخاصة بتطبيق app1
│   └── views.py              # المنطق المبرمج للواجهات والمسح
│
├── core/                     # إعدادات المشروع الرئيسية (Django Config)
│   ├── settings.py           # الإعدادات العامة وقواعد البيانات
│   └── urls.py               # المسارات الرئيسية للارتباط
│
├── media/                    # الملفات المرفوعة والمولدة
│   └── qr_codes/             # المجلد المخصص لحفظ صور الـ QR Code
│
├── db.sqlite3                # قاعدة البيانات المحلية
├── .gitignore                # استبعاد الملفات غير الضرورية من Git
└── manage.py                 # أداة إدارة Django

```

---

## 🛠️ التقنيات المستخدمة (Tech Stack)

* **Backend:** Python 3.x, Django Framework
* **Frontend:** HTML5, CSS3, JavaScript (QR Scanner Library / WebRTC)
* **Database:** SQLite3 (افتراضي للبيئة التطويرية)

---

## 🚀 طريقة التشغيل والتركيب (Getting Started)

### 1. الاستنساخ والتهيئة (Prerequisites)

قم باستنساخ المستودع والانتقال للمشروع:

```bash
git clone [https://github.com/your-username/eventhub.git](https://github.com/your-username/eventhub.git)
cd eventhub

```

### 2. إنشاء البيئة الافتراضية (Virtual Environment)

* **على Windows:**
```bash
python -m venv venv
venv\Scripts\activate

```


* **على Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate

```



### 3. تثبيت المتطلبات (Install Dependencies)

```bash
pip install django qrcode pillow

```

### 4. تطبيق ترحيلات قاعدة البيانات (Database Migrations)

```bash
python manage.py makemigrations
python manage.py migrate

```

### 5. إنشاء حساب مسؤول (Superuser)

```bash
python manage.py createsuperuser

```

### 6. تشغيل السيرفر المحلي (Run Server)

```bash
python manage.py runserver

```

افتح المتصفح وانتقل إلى: `http://127.0.0.1:8000/`

---

## 📝 ملاحظات البيئة والملفات المرفقة

* تأكد من إعطاء الصلاحيات للكاميرا عند فتح صفحة `camera_scanner.html` لتتمكن الأداة من قراءة الـ QR Code.
* يتم حفظ صور الـ QR المنسوخة داخل مجلد `media/qr_codes/` تلقائياً عند إنشاء أي تذكرة جديدة.

```

---

**طريقة الاستخدام:**
1. أنشئ ملفاً جديداً باسم `README.md` في مجلد المشروع الرئيسي (بجانب `manage.py`).
2. انسخ المحتوى أعلاه والصقه داخل الملف وسيكون جاهزاً ومكتتملاً!

```
