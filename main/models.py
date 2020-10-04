from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    class STATUS(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'ОПУБЛИКОВАН'

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор статьи')
    name = models.CharField('Название', max_length=200)
    text = models.TextField('Текст')
    img = models.ImageField('Изображение', upload_to='img/', blank=True, null=True)
    date_create = models.DateTimeField('дата создания', auto_now_add=True)
    date_change = models.DateTimeField('дата редактирования', auto_now=True)
    date_pub = models.DateTimeField('дата публикации', blank=True, null=True)
    status = models.PositiveSmallIntegerField('статус', choices=STATUS.choices, default=STATUS.DRAFT)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='Статью'
        verbose_name_plural='Статьи'