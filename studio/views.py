
from django.shortcuts import render ,get_object_or_404,redirect
from .forms import *
from .models import *
from django.db.models import Count
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth, ExtractYear
from django.core.paginator import Paginator
# Create your views here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(post_save, sender=Booking)
def create_booking_status(sender, instance, created, **kwargs):
    if created:
        BookingStatus.objects.create(booking=instance)

def index(request):
    return render(request,'index.html')

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the same page with a success message
            return redirect('contact')  # Or any other URL you want to redirect to
        else:
            # Render the form with errors
            return render(request, 'contact_us.html', {'form': form})
    else:
        # Handle GET request by rendering the form
        form = ContactForm()
    
    return render(request, 'contact_us.html', {'form': form})

def blog(request):
    blogs = Blog.objects.all().order_by('-date')

    archive_dates = Blog.objects.annotate(
        year=ExtractYear('date'),
        month=ExtractMonth('date')
    ).values('year', 'month').annotate(count=Count('id')).order_by('-year', '-month')

    paginator = Paginator(blogs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    types = Type.objects.all()
    

    if request.method == 'POST':
        form = RadioCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return redirect('blog')
    else:
        form = RadioCommentForm()
    comments = Radio_Comment.objects.all()

    schedules = Program_Schedule.objects.all()
    context = {
        'page_obj': page_obj,
        'types': types,
        'archive_dates': archive_dates,
        'form': form,
        'comments':comments,
        'schedules':'schedules',

    }
    return render(request, 'blog.html', context)


def post(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            return JsonResponse({'success': True})
        else:
     
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)


    form = CommentForm()
    return render(request, 'post.html', {'blog': blog, 'form': form, 'comments': comments})
def blog_by_type(request, type_id):
    blog_type = get_object_or_404(Type, pk=type_id)
    blogs = Blog.objects.filter(type=blog_type).select_related('type').order_by('-date')

    paginator = Paginator(blogs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'blog_type': blog_type,
        'page_obj': page_obj,
    }
    return render(request, 'blog_by_type.html', context)


def archive(request, year=None, month=None):
    blogs = Blog.objects.all()
    
    paginator = Paginator(blogs,12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if year is not None and month is not None:
        archive_dates = Blog.objects.filter(date__year=year, date__month=month).annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        ).values('year', 'month').annotate(count=Count('id'))
    elif year is not None:
        archive_dates = Blog.objects.filter(date__year=year).annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        ).values('year', 'month').annotate(count=Count('id'))
    else:
        archive_dates = Blog.objects.annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        ).values('year', 'month').annotate(count=Count('id'))
    


  
    context = {'archive_dates': archive_dates, 'blogs': blogs,'page_obj':page_obj}
    return render(request, 'archive.html', context)
def gallery(request):
    pictures = Gallery.objects.all()
    context ={'pictures':pictures}


    return render(request,'gallery.html',context)
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_instance = form.save()
            
            # Check if BookingStatus already exists for this booking
            booking_status, created = BookingStatus.objects.get_or_create(
                booking=booking_instance,
                defaults={'status': 'pending'}
            )

            if not created:
                # If it already exists, update the status
                booking_status.status = 'pending'
                booking_status.save()

            # Send email notification
            send_mail(
                subject='New Booking Submitted',
                message=f"A new booking has been submitted:\n\n"
                        f"Name: {booking_instance.name}\n"
                        f"Service Type: {booking_instance.service_type}\n"
                        f"Address: {booking_instance.address}\n"
                        f"Event: {booking_instance.event}\n"
                        f"Date: {booking_instance.date}\n"
                        f"Time: {booking_instance.time}\n",
                from_email='your_email@gmail.com',
                recipient_list=['ranchomhyc2019@gmail.com'],
                fail_silently=False,
            )

            # Render the response with a success message
            return render(request, 'booking.html', {'form': BookingForm(), 'success_message': 'Form submitted successfully!'})
        else:
            # Render the form with errors
            return render(request, 'booking.html', {'form': form})
    
    # Handle the GET request
    form = BookingForm()
    return render(request, 'booking.html', {'form': form})
