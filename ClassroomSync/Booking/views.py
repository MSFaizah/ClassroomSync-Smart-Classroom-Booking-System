from django.shortcuts import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from Booking.models import *
from datetime import datetime, timedelta

alerts = Alert.objects.all().order_by('-created_at')

# Create your views here.
def home(request):
    return render(request, "home.html")

def admin_login(request):
    if 'login_tries' not in request.session:
        request.session['login_tries'] = 0

    if request.method == "POST":
        username = request.POST['login-user']
        password = request.POST['login-pass']
        user = authenticate(request, username=username, password=password)

        if user is not None and request.session['login_tries']<=5:
            login(request, user)
            request.session['login_tries'] = 0  # reset on success
            return redirect('admin_dashboard')
        
        elif request.session['login_tries']>5:
            return render(request, "admin_login.html", {'error':'Too many attempts. Account Locked','disabled_fields':True})

        else:
            request.session['login_tries'] += 1
            return render(request, "admin_login.html", {'error':'Invalid Credentials'})
    else:
        return render(request, 'admin_login.html')

@login_required
def admin_dashboard(request):
    if request.method == "POST":
        action = request.POST.get('action') # 'check', 'book', or 'cancel'
        #Get form data
        room_no = request.POST.get('m-room')
        date = request.POST.get('m-date')
        start = request.POST.get('m-start')
        end = request.POST.get('m-end')
        requester = request.POST.get('m-request')
        dept = request.POST.get('m-dept', 'General') # Default to General if empty

        # Ensures times are valid
        if start and end and start >= end:
            messages.error(request, "End time must be after start time.")
            return redirect('admin_dashboard')
        
        if action == 'check':
            return redirect(f"{request.path}?date={date}&start={start}&end={end}")
        
        if action == 'book':
            # Check for overlaps
            overlap = Bookings.objects.filter(
                room_number_id = room_no,
                date = date
            ).filter(
                start_time__lt = end,
                end_time__gt = start
            ).exists()

            if overlap:
                messages.error(request, f"Room {room_no} is already booked for that slot")
            else:
                # Create booking
                Bookings.objects.create(
                    room_number_id = room_no,
                    date = date,
                    start_time =  start,
                    end_time = end,
                    department = dept,
                    requested_by = requester,
                    status = "BOOKED"
                )
                messages.success(request, f"Room {room_no} booked successfully!✅")
            
        elif action == "cancel":
            # don't have to worry about status because if the row exists, it means it's booked. If it doesn't exist, it's available.
            # Find exact booking
            booking_to_cancel = Bookings.objects.filter(room_number_id = room_no, date = date).filter(start_time__lte = start, end_time__gte = end).first()

            if booking_to_cancel:
                booking_to_cancel.delete()
                messages.info(request, f"Booking for Room {room_no} cancelled!")
            else:
                messages.warning(request, f"No booking found for Room {room_no} at that slot")
        
        elif action in ['Approve', 'Reject']:
            req_id = request.POST.get('req_id')
            booking_req = RequestApplications.objects.get(id=req_id)
            if action == 'Reject':
                booking_req.status = 'Rejected'
                booking_req.save()
                messages.warning(request, f"Request from {booking_req.requester} rejected.")

            elif action == 'Approve':
                if booking_req.aim == 'To Book':
                    # Check for overlaps
                    overlap = Bookings.objects.filter(
                        room_number_id = booking_req.room,
                        date = booking_req.date,
                        start_time__lt = booking_req.end_time,
                        end_time__gt = booking_req.start_time
                    ).exists()
                    if overlap:
                        messages.error(request, f"Cannot approve! Room {booking_req.room} is already booked during this time.")
                    else:
                        # Create booking
                        Bookings.objects.create(
                            room_number_id = booking_req.room,
                            date = booking_req.date,
                            start_time = booking_req.start_time,
                            end_time = booking_req.end_time,
                            department = booking_req.dept,
                            requested_by = booking_req.requester,
                            status = "Booked"
                        )
                        booking_req.status = "Approved"
                        booking_req.save()
                        messages.success(request, f"Booking approved and created for {booking_req.requester}!")
                
                elif booking_req.aim == 'To Cancel':
                    # Find the exact booking and delete it
                    booking_to_cancel = Bookings.objects.filter(
                        room_number_id = booking_req.room,
                        date = booking_req.date,
                        start_time__lte = booking_req.start_time,
                        end_time__gte = booking_req.end_time
                    ).first()
                    if booking_to_cancel:
                        booking_to_cancel.delete()
                        booking_req.status = 'Approved'
                        booking_req.save()
                        messages.info(request, f"Cancellation approved. Room {booking_req.room} is now free.")
                    else:
                        messages.error(request, "Cannot approve cancellation: No matching booking found.")
        return redirect('admin_dashboard')

    selected_floor = int(request.GET.get('floor', 1))
    selected_aim = request.GET.get('selected_aim', 'book')
    floor = Rooms.objects.values_list('floor', flat=True).distinct().order_by('floor')
    rooms = Rooms.objects.filter(floor=selected_floor).order_by('room_number')

    # Default room overview to Now if url has no parametres
    now = datetime.now()
    sel_date = request.GET.get('date', now.strftime('%Y-%m-%d'))
    sel_start = request.GET.get('start', now.strftime('%H:%M'))
    # Default end time to 1 hour from now
    one_hour_later = now + timedelta(hours=1)
    sel_end = request.GET.get('end', one_hour_later.strftime('%H:%M'))

    # Finding Overlapping bookings-> Store those data in collection
    overlap_bookings = Bookings.objects.filter(
        date = sel_date,
        start_time__lt = sel_end,
        end_time__gt = sel_start,
    )
    booked_dict = {b.room_number_id : b for b in overlap_bookings}

    for r in rooms:
        if r.room_number in booked_dict:
            b = booked_dict[r.room_number]
            r.dynamic_status = "Booked"
            r.book_req = b.requested_by
            r.book_dept = b.department
            r.book_start = b.start_time.strftime('%H:%M')
            r.book_end = b.end_time.strftime('%H:%M')
        else:
            r.dynamic_status = "Available"
            r.book_req = ""
            r.book_dept = ""
            r.book_start = ""
            r.book_end = ""
    
    Alert.objects.filter(alert_end_time__lte = timezone.now()).update(status='expired')
    alerts = Alert.objects.filter(status='active').order_by('-created_at')
    # Fetch only pending requests to send to the HTML
    pending_books = RequestApplications.objects.filter(aim='To Book', status='Pending')
    pending_cancels = RequestApplications.objects.filter(aim='To Cancel Booking', status='Pending')
    
    context = {
        'alerts': alerts,
        'floors': floor,
        'rooms': rooms,
        'selected_floor': selected_floor,
        'selected_aim': selected_aim,
        'sel_date':sel_date,
        'sel_start':sel_start,
        'sel_end': sel_end,
        'pending_books': pending_books,
        'pending_cancels': pending_cancels
    }
    return render(request, 'admin_dashboard.html', context)

def add_alert(request):
    if request.method == 'POST':
        title = request.POST['title']
        message = request.POST['message']
        if title and message:
            Alert.objects.create(
                type=request.POST['type'],
                title = title,
                message = message,
                alert_date = request.POST['date'],
                alert_start_time = request.POST['alert_start_time'],
                alert_end_time = request.POST['alert_end_time']
            )
        return redirect('admin_dashboard')

def delete_alert(request, id):
    if request.method == "POST":
        Alert.objects.filter(id=id).delete()
    return redirect('admin_dashboard')

def student_dashboard(request):
    today = timezone.now().date()
    alerts = Alert.objects.filter(status='active', alert_date__gte=today).order_by('-created_at')

    selected_floor = int(request.GET.get('floor', 1))
    floor = Rooms.objects.values_list('floor', flat=True).distinct().order_by('floor')
    rooms = Rooms.objects.filter(floor=selected_floor).order_by('room_number')

    # Default room overview to Now if url has no parametres
    now = datetime.now()
    sel_date = request.GET.get('date', now.strftime('%Y-%m-%d'))
    sel_start = request.GET.get('start', now.strftime('%H:%M'))
    # Default end time to 1 hour from now
    one_hour_later = now + timedelta(hours=1)
    sel_end = request.GET.get('end', one_hour_later.strftime('%H:%M'))

    # Finding Overlapping bookings-> Store those data in collection
    overlap_bookings = Bookings.objects.filter(
        date = sel_date,
        start_time__lt = sel_end,
        end_time__gt = sel_start,
    )
    booked_dict = {b.room_number_id : b for b in overlap_bookings}

    for r in rooms:
        if r.room_number in booked_dict:
            b = booked_dict[r.room_number]
            r.dynamic_status = "Booked"
            r.book_req = b.requested_by
            r.book_dept = b.department
            r.book_start = b.start_time.strftime('%H:%M')
            r.book_end = b.end_time.strftime('%H:%M')
        else:
            r.dynamic_status = "Available"
            r.book_req = ""
            r.book_dept = ""
            r.book_start = ""
            r.book_end = ""

    if request.method == "POST":
        RequestApplications.objects.create(
            aim=request.POST.get('aim'),
            room=request.POST.get('room'),
            requester=request.POST.get('name'),
            uid=request.POST.get('uid'),
            dept=request.POST.get('department'),
            date=request.POST.get('req-date'),
            start_time=request.POST.get('req-start'),
            end_time=request.POST.get('req-end'),
            purpose=request.POST.get('message'),
            status='Pending'
        )
        messages.success(request, "Request submitted to Admin! 🚀")
        return redirect('student_dashboard')
    
    context = {
        'alerts':alerts,
        'floors': floor,
        'rooms': rooms,
        'selected_floor': selected_floor,
        'sel_date':sel_date,
        'sel_start':sel_start,
        'sel_end': sel_end,
    }
    return render(request, "student_dashboard.html", context)

def classroom_details(request, room_number):
    room = get_object_or_404(Rooms, room_number=room_number)

    now = datetime.now()
    one_hour_later = now + timedelta(hours=1)
    sel_date  = request.GET.get('date',  now.strftime('%Y-%m-%d'))
    sel_start = request.GET.get('start', now.strftime('%H:%M'))
    sel_end   = request.GET.get('end',   one_hour_later.strftime('%H:%M'))

    booking = Bookings.objects.filter(
        room_number=room,
        date=sel_date,
        start_time__lt=sel_end,
        end_time__gt=sel_start
    ).first()

    if booking:
        room.dynamic_status = "Booked"
        room.book_dept  = booking.department
        room.book_date  = booking.date
        room.book_start = booking.start_time.strftime('%H:%M')
        room.book_end   = booking.end_time.strftime('%H:%M')
    else:
        room.dynamic_status = "Available"
        room.book_dept  = None
        room.book_date  = None
        room.book_start = None
        room.book_end   = None

    context = {
        'room': room,
        'bookings': Bookings.objects.filter(room_number=room),
        'sel_date': sel_date,
        'sel_start': sel_start,
        'sel_end': sel_end,
    }
    return render(request, "classroom_details.html", context)

def logout_view(request):
    logout(request)
    return redirect('home')