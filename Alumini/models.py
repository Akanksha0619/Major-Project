from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Alumni(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_role = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    skills = models.TextField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    


class Post(models.Model):
    alumni = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image')
    description = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name='liked_posts', blank=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text}"
    
class Connection(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username} - {self.status}"