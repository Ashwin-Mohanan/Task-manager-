from django.db import models

# Create your models here.
class Task(models.Model):
    taskid = models.AutoField(db_column='taskid',primary_key=True)
    title = models.CharField(db_column = 'title',max_length=100)
    description = models.TextField(db_column = 'description')
    due_date = models.DateField(db_column = 'due_date')
    tag_type = models.TextField(db_column = 'tag_type')
    tag = models.TextField(db_column = 'tag')
    created_at = models.DateTimeField(auto_now_add=True)

   
    class Meta:
        managed=True
        db_table='Task'