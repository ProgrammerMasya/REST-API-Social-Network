# Generated by Django 2.0 on 2019-03-29 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("home", "0004_auto_20190329_2214")]

    operations = [
        migrations.RemoveField(model_name="post", name="likes"),
        migrations.AddField(
            model_name="post",
            name="likes",
            field=models.IntegerField(default=0, verbose_name="Нравится"),
        ),
    ]
