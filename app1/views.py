from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Event, Attendee, generate_short_ticket_code
import pandas as pd  
import qrcode
from io import BytesIO
from django.core.files import File

@login_required
def live_camera_scanner(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'camera_scanner.html', {'event': event})

@login_required
def event_control_dashboard(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == "POST" and "add_guest" in request.POST:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        if name:
            Attendee.objects.create(event=event, name=name, phone=phone)
            messages.success(request, f"✅ تم إضافة {name} بنجاح.")
            return redirect('event_control_dashboard', event_id=event.id)
            
    guests = event.guests.all().order_by('-id')
    return render(request, 'event_dashboard.html', {
        'event': event, 
        'guests': guests
    })

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
            return JsonResponse({'success': False, 'error': 'الرمز غير مسجل بالنظام'}, status=404)
            
    return JsonResponse({'success': False}, status=400)

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

@login_required
def delete_attendee_api(request, attendee_id):
    if request.method == "POST":
        attendee = get_object_or_404(Attendee, id=attendee_id)
        attendee.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def import_attendees_api(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        event_id = request.POST.get('event_id')
        
        if not event_id:
            return JsonResponse({'success': False, 'error': 'معرف الفعالية مفقود في الطلب.'}, status=400)
            
        event = get_object_or_404(Event, id=event_id)
        
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            df.columns = [str(c).strip().lower() for c in df.columns]
            
            name_col = None
            phone_col = None
            
            for col in df.columns:
                if any(kw in col for kw in ['اسم', 'name', 'full name', 'المدعو', 'الحاضر']):
                    name_col = col
                if any(kw in col for kw in ['هاتف', 'جوال', 'phone', 'mobile', 'tel', 'رقم']):
                    phone_col = col

            if not name_col:
                return JsonResponse({
                    'success': False, 
                    'error': f'لم يتم العثور على عمود الاسم. الأعمدة المتوفرة في ملفك هي: {list(df.columns)}'
                }, status=400)
            
            attendees_to_create = []
            
            for _, row in df.iterrows():
                name = str(row[name_col]).strip()
                phone = str(row[phone_col]).strip() if phone_col and pd.notna(row[phone_col]) else ''
                
                if phone.endswith('.0'):
                    phone = phone[:-2]
                
                if name and name.lower() != 'nan' and name != '':
                    ticket_code = generate_short_ticket_code()
                    
                    attendee = Attendee(
                        event=event, 
                        name=name, 
                        phone=phone, 
                        ticket_code=ticket_code
                    )
                    
                    check_in_url = f"http://127.0.0.1:8000/verify/{ticket_code}/"
                    
                    qr = qrcode.QRCode(version=1, box_size=10, border=3)
                    qr.add_data(check_in_url)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    
                    blob = BytesIO()
                    img.save(blob, 'PNG')
                    blob.seek(0)
                    
                    attendee.qr_code.save(f'qr-{ticket_code}.png', File(blob), save=False)
                    
                    attendees_to_create.append(attendee)
            
            if attendees_to_create:
                Attendee.objects.bulk_create(attendees_to_create)
                
            return JsonResponse({'success': True, 'count': len(attendees_to_create)})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
            
    return JsonResponse({'success': False, 'error': 'طلب غير صالح أو لم يتم رفع ملف.'}, status=400)