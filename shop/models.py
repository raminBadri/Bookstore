from django.contrib.auth.models import User
from django.db import models


class AbstractModel(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Genre(AbstractModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Author(AbstractModel):
    name = models.CharField(max_length=255)
    birth = models.IntegerField(null=True)
    death = models.IntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='author-profile-pic/', blank=True, null=True)

    def __str__(self):
        return '{}- from {} to {}'.format(self.name, self.birth, self.death or 'now')


class Publisher(AbstractModel):
    title = models.CharField(max_length=255)
    tel = models.IntegerField(null=True, max_length=11)
    address = models.TextField(null=True)
    logo = models.ImageField(upload_to='publisher-logo/', null=True, blank=True)

    def __str__(self):
        return '{} - tel: {} - address: {}'.format(self.title, self.tel, self.address)


class Score(AbstractModel):
    amount = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return '{} to {}'.format(self.user, self.amount)


class Comment(AbstractModel):
    context = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return '{} has said: {}'.format(self.user.username, self.context)


class Book(AbstractModel):
    title = models.CharField(max_length=255)
    year = models.IntegerField(null=True)
    cover = models.ImageField(upload_to='book-covers/', blank=True, null=True)
    available_count = models.IntegerField(default=1)
    price = models.IntegerField(null=False, blank=False)
    page_count = models.IntegerField(null=False, blank=False)
    about = models.TextField()
    genre = models.ManyToManyField(Genre)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    comment = models.ForeignKey(Comment, on_delete=models.PROTECT)
    score = models.ForeignKey(Score, on_delete=models.PROTECT)

    def __str__(self):
        return '{} ({})'.format(self.title, self.author.name)

