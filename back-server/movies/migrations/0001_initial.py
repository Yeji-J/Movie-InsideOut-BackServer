# Generated by Django 3.2.13 on 2022-11-24 00:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('actor_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('gerne_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('title', models.CharField(max_length=100)),
                ('overview', models.TextField(null=True)),
                ('poster_path', models.TextField(null=True)),
                ('release_date', models.DateField()),
                ('adult', models.BooleanField()),
                ('vote_average', models.FloatField()),
                ('vote_count', models.IntegerField()),
                ('backdrop_path', models.TextField(null=True)),
                ('movie_id', models.IntegerField(primary_key=True, serialize=False)),
                ('vedio_url', models.CharField(blank=True, max_length=100)),
                ('actors', models.ManyToManyField(related_name='actors', to='movies.Actor')),
                ('genres', models.ManyToManyField(related_name='movies', to='movies.Genre')),
                ('like_users', models.ManyToManyField(related_name='like_movies', to=settings.AUTH_USER_MODEL)),
                ('user_picks', models.ManyToManyField(related_name='watch_list', to=settings.AUTH_USER_MODEL)),
                ('watched_users', models.ManyToManyField(related_name='watched_movies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('vote', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
