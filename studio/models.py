from django.db import models,transaction

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=15)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
class Type(models.Model):
    name = models.CharField(max_length=255)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Type"
    

class Blog(models.Model):
    type = models.ForeignKey(Type,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=10000)
    date = models.DateTimeField(blank=True,null=True)
    image = models.ImageField(blank=True,null=True)   
    author = models.CharField(max_length=50) 


    def __str__(self):
        return self.title
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url
    
    class Meta:
        ordering = ['date']
        verbose_name_plural = "Blogs"

    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    commenter_name = models.CharField(max_length=100)
    commenter_email = models.EmailField(blank=True)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter_name} on {self.blog.title}"

class Gallery(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True,null=True) 

    
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url
    
    class Meta:
        verbose_name_plural = "Gallery"
class Booking(models.Model):

    SERVICE_TYPE_CHOICES = [
        ('live_stream', 'Live Stream'),
        ('video_editing', 'Video Editing'),
        ('Event Planning', 'Event Planning')
    ]
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    event = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default='live_stream')
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.event} on {self.date} at {self.time}"

    def save(self, *args, **kwargs):
        # Use transaction.atomic() to ensure that the status is only created if the booking is successfully saved
        with transaction.atomic():
            super().save(*args, **kwargs)
            # Create a BookingStatus if it doesn't exist
            if not hasattr(self, 'status'):
                BookingStatus.objects.create(booking=self)

class BookingStatus(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='status')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking.name} - {self.get_status_display()}"
    class Meta:
        verbose_name_plural = "Booking Status"
   
class Radio_Comment(models.Model):
    commenter_name = models.CharField(max_length=100)
    commenter_email = models.EmailField(blank=True)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:20]

     
class Program_Schedule(models.Model):
    days = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday','Thursday'),
        ('friday','Friday'),
        ('saturday','Saturday'),
        ('sunday','Sunday')
    ]
    program_name = models.CharField(max_length=255)
    day = models.CharField(max_length= 10,choices=days)
    start= models.TimeField(blank=True,null=True)
    end = models.TimeField(blank=True,null=True) 
