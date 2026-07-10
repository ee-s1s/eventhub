from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Event, Attendee

# ==========================================
# 1. واجهات البوابة واللوحة الشاملة للفعاليات
# ==========================================

# أ. صفحة الكاميرا الذكية (بوابة المسح المستمر عند الباب)
@login_required
def live_camera_scanner(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'camera_scanner.html', {'event': event})


# ب. لوحة التحكم والإدارة الشاملة (All-in-One Dashboard)
@login_required
def event_control_dashboard(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # التعامل مع إضافة شخص جديد مباشرة من نفس لوحة التحكم
    if request.method == "POST" and "add_guest" in request.POST:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        if name:
            Attendee.objects.create(event=event, name=name, phone=phone)
            messages.success(request, f"✅ تم إضافة {name} بنجاح.")
            return redirect('event_control_dashboard', event_id=event.id)
            
    # جلب جميع الحاضرين المرتبطين بالفعالية (الأحدث أولاً)
    guests = event.guests.all().order_by('-id')
    return render(request, 'event_dashboard.html', {
        'event': event, 
        'guests': guests
    })


# ==========================================
# 2. واجهات برمجية خلفية (AJAX APIs) 
# ==========================================

# أ. تبديل حالة الحضور (تستقبل ticket_code لتدعم الكاميرا والجدول معاً)
@login_required
def toggle_checkin_api(request, ticket_code):
    if request.method == "POST":
        try:
            attendee = Attendee.objects.get(ticket_code=ticket_code)
            
            if attendee.is_checked_in:
                attendee.is_checked_in = False
                status = "checked_out"
            else:
                attendee.is_checked_in = True
                attendee.check_in_time = timezone.now()
                status = "checked_in"
                
            attendee.save()
            
            return JsonResponse({
                'success': True, 
                'status': status,
                'attendee_name': attendee.name,
                'is_checked_in': attendee.is_checked_in,
                'check_in_time': attendee.check_in_time.strftime('%H:%M') if attendee.check_in_time else ''
            })
        except Attendee.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'الرمز غير مسجل بالنظام'}, status=404)
            
    return JsonResponse({'success': False}, status=400)


# ب. التعديل الفوري (الاسم والهاتف) عبر اللوحة الرئيسية
@login_required
def edit_attendee_api(request, attendee_id):
    if request.method == "POST":
        attendee = get_object_or_404(Attendee, id=attendee_id)
        attendee.name = request.POST.get('name', attendee.name)
        attendee.phone = request.POST.get('phone', attendee.phone)
        attendee.save()
        return JsonResponse({
            'success': True, 
            'name': attendee.name, 
            'phone': attendee.phone if attendee.phone else ''
        })
    return JsonResponse({'success': False}, status=400)


# ج. الحذف الفوري وإلغاء الـ QR
@login_required
def delete_attendee_api(request, attendee_id):
    if request.method == "POST":
        attendee = get_object_or_404(Attendee, id=attendee_id)
        attendee.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)