from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    avatar = models.FileField(upload_to='user_avatar')
    background_img = models.FileField(upload_to='user_background'),
    phone = models.CharField(max_length=15)
    about_user = models.TextField(max_length=255)

    def get_avatar_url(self):
        try:
            url = self.avatar.url
        except:
            url = static("image/default.png")
        return url

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created =  UserProfile.objects.get_or_create(user=instance)
