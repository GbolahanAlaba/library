# Generated by Django 5.1.1 on 2024-09-12 17:25

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Library', '0010_book_available_copies'),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('return_date', models.DateTimeField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Library.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Library.user')),
            ],
        ),
    ]
