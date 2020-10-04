# Generated by Django 3.1.1 on 2020-09-12 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20200912_1742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articles',
            name='create_date',
        ),
        migrations.AddField(
            model_name='articles',
            name='date_change',
            field=models.DateTimeField(auto_now=True, verbose_name='дата редактирования'),
        ),
        migrations.AddField(
            model_name='articles',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articles',
            name='date_pub',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата публикации'),
        ),
        migrations.AddField(
            model_name='articles',
            name='status',
            field=models.CharField(choices=[('d', 'Черновик'), ('p', 'ОПУБЛИКОВАН'), ('w', 'СНЯТ с публикации')], default='d', max_length=1, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='Автор статьи'),
        ),
    ]
