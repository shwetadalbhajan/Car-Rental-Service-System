import razorpay
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.validators import validate_email
import random
from django.conf import settings
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import *

def landing_page_view(request):
    return render(request, 'landing.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        # Save data to the database
        ContactSubmission.objects.create(name=name, email=email, phone=phone, message=message)

        # Send confirmation email to user
        try:
            send_mail(
                "Thank You for Contacting DriveEase",
                f"Dear {name},\n\nWe have received your message:\n\n{message}\n\nWe will get back to you soon.\n\nBest regards,\nDriveEase Team",
                "car.rental.services.0@gmail.com",
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email Error: {e}")
        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")  # Redirect after successful submission
    return render(request, "contact.html")

def register_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format!")
            return redirect('register')

        if not phone.isdigit() or len(phone)!=10:
            messages.error(request, "Phone number must contain only digits and 10 characters!")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        request.session['email'] = email
        request.session['password'] = password
        request.session['name'] = name
        request.session['phone'] = phone

        send_mail(
            subject="Your Verification OTP",
            message=f"Your OTP for Car Rental registration is {otp}.",
            from_email='car.rental.services.0@gmail.com',
            recipient_list=[email],
        )

        messages.success(request, "OTP sent to your email!")
        return redirect('verify_otp')  # Redirect to OTP verification page

    return render(request, 'register.html')

def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        stored_otp = request.session.get('otp')

        if str(entered_otp) == str(stored_otp):
            User.objects.create_user(
                name=request.session['name'],
                email=request.session['email'],
                phone=request.session['phone'],
                password=request.session['password']
            )
            messages.success(request, "Registration successful!")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP!")
            return redirect('verify_otp')

    return render(request, 'verify_otp.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            otp = random.randint(100000, 999999)
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email

            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP for password reset is {otp}.",
                from_email='car.rental.services.0@gmail.com',
                recipient_list=[email],
            )
            messages.success(request, "OTP sent to your email!")
            return redirect('reset_password_otp')
        else:
            messages.error(request, "Email not registered!")
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')

def reset_password_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        stored_otp = request.session.get('reset_otp')

        if str(entered_otp) == str(stored_otp):
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP!")
            return redirect('reset_password_otp')

    return render(request, 'reset_password_otp.html')

User = get_user_model()

def reset_password_view(request):
    if request.method == 'POST':
        # Retrieve data from the form
        new_password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Validate password fields
        if not new_password or not confirm_password:
            messages.error(request, "Both password fields are required.")
            return redirect('reset_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('reset_password')

        # Retrieve the user's email stored in the session
        email = request.session.get('reset_email')

        if not email:
            messages.error(request, "Session expired. Please try again.")
            return redirect('forgot_password')  # Redirect to forgot password page

        # Fetch the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User not found. Please try again.")
            return redirect('forgot_password')

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Provide feedback to the user
        messages.success(request, "Your password has been reset successfully! Please log in.")
        return redirect('login')  # Redirect to login page

    # Render the password reset form
    return render(request, 'reset_password.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password!")
            return redirect('login')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

def home_view(request):
    cars = Car.objects.all().order_by('?')  # Fetch all cars from the database

    # Apply search query
    search_query = request.GET.get('search', '')

    if search_query:
        cars = cars.filter(
            brand__icontains=search_query) | cars.filter(
            model__icontains=search_query) | cars.filter(
            transmission__icontains=search_query) | cars.filter(
            fuel_type__icontains=search_query) | cars.filter(
            seating_capacity__icontains=search_query)

    # Paginate the car list
    paginator = Paginator(cars, 6)  # Show 6 cars per page
    page_number = request.GET.get('page')  # Get the page number from the query string
    page_obj = paginator.get_page(page_number)

    # Fetch distinct values for car attributes (to show them in the search bar)
    brands = Car.objects.values_list('brand', flat=True).distinct()
    transmissions = Car.objects.values_list('transmission', flat=True).distinct()
    fuel_types = Car.objects.values_list('fuel_type', flat=True).distinct()
    seating_capacities = Car.objects.values_list('seating_capacity', flat=True).distinct()

    context = {
        'page_obj': page_obj,
        'brands': brands,
        'transmissions': transmissions,
        'fuel_types': fuel_types,
        'seating_capacities': seating_capacities,
    }

    return render(request, 'home.html', context)


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'car_detail.html', {'car': car})


@login_required
def add_to_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, car=car)

    if created:
        messages.success(request, f"{car.brand} {car.model} added to your wishlist!")
    else:
        messages.info(request, f"{car.brand} {car.model} is already in your wishlist.")

    return redirect('home')

@login_required
def view_wishlist(request):
    wishlist_cars = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_cars': wishlist_cars})

@login_required
def remove_from_wishlist(request, car_id):
    try:
        # Filter by both the car and the user to ensure only one wishlist entry is removed
        wishlist_item = Wishlist.objects.get(car_id=car_id, user=request.user)
        wishlist_item.delete()
        messages.success(request, "Car removed from wishlist.")
    except Wishlist.DoesNotExist:
        messages.error(request, "This car is not in your wishlist.")
    except Wishlist.MultipleObjectsReturned:
        messages.error(request, "Multiple entries found for this car in your wishlist.")
    return redirect('view_wishlist')


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    total_price = None
    razorpay_order_id = None
    booking = None

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        hours = int(request.POST.get("hours"))
        address = request.POST.get("address")
        driver_needed = request.POST.get("driver_needed") == "on"

        total_price = car.rent_per_hour * hours
        if driver_needed:
            total_price += 500  # Add driver cost

        booking = Booking.objects.create(
            user=request.user,
            car=car,
            name=name,
            phone=phone,
            date=date,
            start_time=start_time,
            hours=hours,
            address=address,
            driver_needed=driver_needed,
            total_price=total_price,
        )

        # Create Razorpay order
        razorpay_order = razorpay_client.order.create(
            {
                "amount": int(total_price * 100),  # Convert to paisa
                "currency": "INR",
                "payment_capture": "1",
            }
        )
        booking.razorpay_payment_id = razorpay_order["id"]
        booking.save()

        return render(
            request,
            "booking_and_payment_page.html",
            {
                "car": car,
                "booking": booking,
                "razorpay_order_id": razorpay_order["id"],
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                "total_price": total_price,
            },
        )

    return render(request, "booking_and_payment_page.html", {"car": car})


@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Create a history record
    BookingHistory.objects.create(
        user=booking.user,
        car=booking.car,
        name=booking.name,
        phone=booking.phone,
        date=booking.date,
        start_time=booking.start_time,
        hours=booking.hours,
        address=booking.address,
        driver_needed=booking.driver_needed,
        total_price=booking.total_price,
        razorpay_payment_id=booking.razorpay_payment_id,
    )

    # Prepare the email content with detailed booking and car information
    email_subject = "Booking Confirmation"
    email_message = (
        f"Dear {booking.name},\n\n"
        f"Thank you for your booking with us! Your booking for a car rental has been confirmed. "
        f"Below are the details of your booking:\n\n"

        f"Booking Details:\n"
        f"Name: {booking.name}\n"
        f"Phone: {booking.phone}\n"
        f"Booking Date: {booking.date}\n"
        f"Start Time: {booking.start_time}\n"
        f"Rental Hours: {booking.hours} hours\n"
        f"Address: {booking.address}\n"
        f"Driver Needed: {'Yes' if booking.driver_needed else 'No'}\n"
        f"Total Price: ₹{booking.total_price}\n\n"

        f"Car Details:\n"
        f"Car Brand: {booking.car.brand}\n"
        f"Car Model: {booking.car.model}\n\n"

        f"Payment Details:\n"
        f"Payment ID: {booking.razorpay_payment_id}\n\n"

        f"We look forward to serving you! If you have any questions, feel free to reach out to us.\n\n"
        f"Best regards,\n"
        f"Car Rental Services\n"
    )

    # Send the confirmation email
    send_mail(
        email_subject,
        email_message,
        "car.rental.services.0@gmail.com",
        [request.user.email],
    )

    # Delete the booking from the main model
    booking.delete()

    messages.success(request, "Payment successful! Booking confirmed.")
    return redirect("booking_history")
@login_required
def booking_history(request):
    history = BookingHistory.objects.filter(user=request.user)
    return render(request, "booking_history.html", {"history": history})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(BookingHistory, id=booking_id)
    return render(request, 'booking_detail.html', {'booking': booking})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def user_profile(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        user = request.user

        # Update name and phone directly
        user.name = name
        user.phone = phone

        # If the email has changed, send OTP to the new email
        if user.email != email:
            otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
            request.session['otp'] = otp
            request.session['new_email'] = email

            # Send OTP to the new email address
            send_mail(
                "Email Change OTP",
                f"Your OTP for updating the email is: {otp}",
                "car.rental.services.0@gmail.com",
                [email],
            )
            messages.info(request, "An OTP has been sent to your new email address.")
            return redirect('verify_email')  # Redirect to the OTP verification page

        # Save the user data if no email change
        user.save()
        messages.success(request, "Your profile has been updated successfully.")
        return redirect("profile")

    return render(request, "profile.html", {"user": request.user})


@login_required
def verify_email(request):
    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        new_email = request.session.get('new_email')

        if otp_entered == request.session.get('otp'):
            # OTP is correct, update the email
            user = request.user
            user.email = new_email
            user.save()
            del request.session['otp']  # Clear OTP from session
            del request.session['new_email']  # Clear new email from session
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "verify_otp.html")