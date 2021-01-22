# Generated by Django 3.1.2 on 2021-01-22 14:43

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.custom_validators.username_validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[main.custom_validators.username_validators.CustomUnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Apps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('google_play_id', models.TextField()),
                ('app_store_id', models.TextField(default=None)),
                ('app_gallery', models.TextField(default=None)),
            ],
            options={
                'db_table': 'Apps',
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'Platform',
            },
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.apps')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Subscriptions',
                'unique_together': {('user', 'app')},
            },
        ),
        migrations.CreateModel(
            name='PeriodData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_5', models.IntegerField(default=0)),
                ('score_4', models.IntegerField(default=0)),
                ('score_3', models.IntegerField(default=0)),
                ('score_2', models.IntegerField(default=0)),
                ('score_1', models.IntegerField(default=0)),
                ('update_date', models.DateTimeField()),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.apps')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.platform')),
            ],
            options={
                'db_table': 'Period Data',
                'unique_together': {('app', 'platform')},
            },
        ),
        migrations.CreateModel(
            name='HistoricalData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_5', models.IntegerField(default=0)),
                ('score_4', models.IntegerField(default=0)),
                ('score_3', models.IntegerField(default=0)),
                ('score_2', models.IntegerField(default=0)),
                ('score_1', models.IntegerField(default=0)),
                ('update_date', models.DateTimeField()),
                ('last_update_app', models.DateTimeField()),
                ('last_update_data', models.DateTimeField()),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.apps')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.platform')),
            ],
            options={
                'db_table': 'Historical Data',
                'unique_together': {('app', 'platform')},
            },
        ),
    ]
