from django.urls import path
from . import views

app_name = 'app1'

urlpatterns = [
    path('<int:event_id>/dashboard/', views.event_control_dashboard, name='event_control_dashboard'),
    path('<int:event_id>/scanner/', views.live_camera_scanner, name='live_camera_scanner'),
    path('attendee/<str:ticket_code>/toggle/', views.toggle_checkin_api, name='toggle_checkin_api'),
    path('attendee/<int:attendee_id>/edit/', views.edit_attendee_api, name='edit_attendee_api'),
    path('attendee/<int:attendee_id>/delete/', views.delete_attendee_api, name='delete_attendee_api'),
    path('attendee/import/', views.import_attendees_api, name='import_attendees_api'),
]