from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users_and_accounts/users_photo/%Y/%m/%d',
                              default='users_and_accounts/users_photo/no_user_photos.png',
                              blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
