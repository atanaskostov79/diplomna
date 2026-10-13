import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_posts_entry_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('slug', models.SlugField(max_length=80, unique=True)),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='posts',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='posts.category'),
        ),
        migrations.AddField(
            model_name='posts',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='posts',
            options={'ordering': ['-created_at'], 'verbose_name': 'пост', 'verbose_name_plural': 'постове'},
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=80)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.posts')),
            ],
            options={
                'verbose_name': 'коментар',
                'verbose_name_plural': 'коментари',
                'ordering': ['created_at'],
            },
        ),
    ]
