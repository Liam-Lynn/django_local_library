# Generated by Django 3.1.3 on 2021-01-02 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_return', 'Set book as returned'),)},
        ),
    ]
