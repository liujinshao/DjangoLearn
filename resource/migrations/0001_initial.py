# Generated by Django 3.1.1 on 2020-09-06 15:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('aixxuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StarConf',
            fields=[
                ('star', models.IntegerField(primary_key=True, serialize=False, verbose_name='星级')),
                ('num', models.IntegerField(verbose_name='评论数')),
            ],
            options={
                'db_table': 't_star_conf',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource', models.FileField(upload_to='resource', verbose_name='资源')),
                ('resource_name', models.CharField(max_length=100, verbose_name='资源名称')),
                ('keywords', models.CharField(help_text='关键字以空格进行分割', max_length=200, verbose_name='关键字')),
                ('score', models.IntegerField(verbose_name='资源积分')),
                ('resource_desc', models.TextField(blank=True, null=True, verbose_name='资源描述')),
                ('ext', models.CharField(blank=True, max_length=50, null=True, verbose_name='资源后缀')),
                ('size', models.IntegerField(blank=True, null=True, verbose_name='资源大小')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='资源上传时间')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='resources', to='aixxuser.axxuser')),
            ],
            options={
                'db_table': 't_resource',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('proof', models.CharField(blank=True, max_length=10, null=True, verbose_name='收藏的凭据')),
                ('resource', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='favorite', to='resource.resource')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='favorite', to='aixxuser.axxuser')),
            ],
            options={
                'db_table': 't_favorite',
            },
        ),
        migrations.CreateModel(
            name='DownloadResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('download_time', models.DateTimeField(auto_now=True)),
                ('download_user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='downloads', to='aixxuser.axxuser')),
                ('resource', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='downloads', to='resource.resource')),
            ],
            options={
                'db_table': 't_resource_download',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CommentResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论的内容')),
                ('star', models.IntegerField(default=1, verbose_name='评论的星级')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('resource', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='resource.resource')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='aixxuser.axxuser')),
            ],
            options={
                'db_table': 't_resource_comment',
            },
        ),
    ]
