import string
import random
import qrcode
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
    ticket_code = models.CharField(max_length=20, unique=True, blank=True, default=generate_short_ticket_code)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    
    # حالات الدخول
    is_checked_in = models.BooleanField(default=False)  # هل دخل الفعالية أم لا؟
    check_in_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"

    def save(self, *args, **kwargs):
        # 1. إذا لم يكن هناك كود تذكرة (في الإضافة الفردية مثلاً عبر الـ Admin)، قم بتوليد كود قصير
        if not self.ticket_code:
            self.ticket_code = generate_short_ticket_code()

        # 2. توليد الـ QR كود تلقائياً إذا لم يكن موجوداً
        if not self.qr_code:
            # الـ QR يحتوي على رابط الفحص المباشر في السيرفر ليسهل فحصها بالكاميرا فوراً
            # يمكنك تعديل الـ domain لاحقاً عند رفع الموقع
            check_in_url = f"http://127.0.0.1:8000/verify/{self.ticket_code}/"
            
            qr = qrcode.QRCode(version=1, box_size=10, border=3) # تقليل الـ border إلى 3 يعطي مظهر أفضل
            qr.add_data(check_in_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            
            self.qr_code.save(f"qr-{self.ticket_code}.png", ContentFile(buffer.getvalue()), save=False)
            
        super().save(*args, **kwargs)