from django.db import models


class CustomUser(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    sex_variants = (
        (MALE, 'M'),
        (FEMALE, 'F'),
        (OTHER, 'O')
    )

    sex = models.CharField(max_length=1, choices=sex_variants, null=True)
    basic_user = models.OneToOneField('auth.User', on_delete=models.CASCADE)


class Post(models.Model):

    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    liked_by = models.ManyToManyField(CustomUser, related_name='liked',
                                      null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             default=None, null=True)
