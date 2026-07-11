import string
import random
import qrcode
import requests
from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

def generate_short_ticket_code():
    """توليد كود عشوائي فريد مكون من 8 خانات (حروف كبيرة وأرقام)"""
    length = 8
    chars = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        # التأكد من أن الكود غير مكرر في قاعدة البيانات
        if not Attendee.objects.filter(ticket_code=code).exists():
            return code


class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    location_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Attendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='guests')
    name = models.CharField(max_length=150)  # اسم الشخص المدعو
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)  # جعله مرناً يقبل الفراغ إذا لم يتوفر إيميل
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)  # معرف التليجرام للأتمتة
    ticket_code = models.CharField(max_length=20, unique=True, blank=True, default=generate_short_ticket_code)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    
    # حالات الدخول
    is_checked_in = models.BooleanField(default=False)  # هل دخل الفعالية أم لا؟
    check_in_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"

    def send_telegram_ticket(self):
        """إرسال التذكرة والـ QR كود عبر بوت التليجرام للمشترك تلقائياً"""
        if not self.telegram_chat_id or not self.qr_code:
            return
            
        BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # ضع توكن البوت الخاص بك هنا
        caption_text = (
            f"مرحباً بك يا {self.name} 🎉\n\n"
            f"تذكرتك الرسمية لفعالية: *{self.event.title}* أصبحت جاهزة! 🎫\n"
            f"📍 المكان: {self.event.location_name}\n"
            f"📅 التاريخ: {self.event.date.strftime('%Y-%m-%d %H:%M')}\n"
            f"🔑 كود التذكرة: `{self.ticket_code}`\n\n"
            f"الرجاء إبراز كود الـ QR المرفق عند بوابة الدخول للتحضير السريع."
        )
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        try:
            self.qr_code.seek(0)
            files = {'photo': self.qr_code.read()}
            data = {
                'chat_id': self.telegram_chat_id,
                'caption': caption_text,
                'parse_mode': 'Markdown'
            }
            response = requests.post(url, data=data, files=files)
            if response.status_code != 200:
                print(f"Telegram API Error: {response.text}")
        except Exception as e:
            print(f"حدث خطأ أثناء إرسال التليجرام: {e}")

    def send_email_ticket(self):
        """إرسال إيميل ترحيبي فاخر مدمج بداخلة تذكرة الـ QR كود تلقائياً"""
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags
        from email.mime.image import MIMEImage

        if not self.email:
            return
            
        subject = f"تذكرتك الرسمية لفعالية {self.event.title} 🎫"
        
        # البيانات الممررة لتصميم قالب الـ HTML
        context = {
            'name': self.name,
            'event_title': self.event.title,
            'date': self.event.date.strftime('%Y-%m-%d %H:%M'),
            'location': self.event.location_name,
            'ticket_code': self.ticket_code,
        }
        
        # قراءة قالب الـ HTML وتحويله إلى نصوص مدعومة للإيميلات
        html_content = render_to_string('ticket_email.html', context)
        text_content = strip_tags(html_content) 
        
        email_message = EmailMultiAlternatives(
            subject, 
            text_content, 
            'no-reply@yourdomain.com',  # بريد المرسل (يمكن ضبطه في settings.py)
            [self.email]
        )
        email_message.attach_alternative(html_content, "text/html")
        
        # تضمين صورة الـ QR كود لتفتح بداخل جسم الإيميل مباشرة عبر المعرف cid
        if self.qr_code:
            try:
                self.qr_code.seek(0)
                mime_image = MIMEImage(self.qr_code.read())
                mime_image.add_header('Content-ID', '<qr_code_cid>')
                mime_image.add_header('Content-Disposition', 'inline', filename=f"qr-{self.ticket_code}.png")
                email_message.attach(mime_image)
            except Exception as e:
                print(f"Error embedding QR code in Email: {e}")
            
        try:
            email_message.send(fail_silently=False)
        except Exception as e:
            print(f"Error sending Email: {e}")

    def save(self, *args, **kwargs):
        # التحقق هل السجل جديد تماماً في قاعدة البيانات أم مجرد تعديل؟
        is_new = self.pk is None 
        
        # 1. إذا لم يكن هناك كود تذكرة، قم بتوليد كود قصير
        if not self.ticket_code:
            self.ticket_code = generate_short_ticket_code()

        # 2. توليد الـ QR كود تلقائياً إذا لم يكن موجوداً
        if not self.qr_code:
            check_in_url = f"http://127.0.0.1:8000/verify/{self.ticket_code}/"
            
            qr = qrcode.QRCode(version=1, box_size=10, border=3)
            qr.add_data(check_in_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            
            self.qr_code.save(f"qr-{self.ticket_code}.png", ContentFile(buffer.getvalue()), save=False)
            
        # حفظ البيانات أولاً لضمان وجود الملف على السيرفر والحصول على الـ Primary Key
        super().save(*args, **kwargs)
        
        # 3. إطلاق الأتمتة الفورية للإيميل والتليجرام فقط عند الإضافة لأول مرة (وليس مع كل تعديل)
        if is_new:
            if self.telegram_chat_id:
                self.send_telegram_ticket()
            if self.email:
                self.send_email_ticket()