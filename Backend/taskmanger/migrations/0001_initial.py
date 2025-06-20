# Generated by Django 5.2 on 2025-05-30 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('taskid', models.AutoField(db_column='taskid', primary_key=True, serialize=False)),
                ('title', models.CharField(db_column='title', max_length=100)),
                ('description', models.TextField(db_column='description')),
                ('due_date', models.DateField(db_column='due_date')),
                ('tag_type', models.TextField(db_column='tag_type')),
                ('tag', models.TextField(db_column='tag')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Task',
                'managed': True,
            },
        ),
    ]
