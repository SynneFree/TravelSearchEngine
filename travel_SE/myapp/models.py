from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=128, primary_key=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

class Collect(models.Model):
    user_name=models.CharField(max_length=128)
    attraction_name=models.CharField(max_length=128)
    location = models.CharField(max_length=128)

    def __str__(self):
        return self.attraction_name

    class Meta:
        db_table = 'collect'
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
    class META:
        ordering = ['id']

class Search_record(models.Model):
    user_name=models.CharField(max_length=128)
    search_field=models.CharField(max_length=128)
    timestamp= models.CharField(max_length=128)
    def __str__(self):
        return self.search_field
    class Meta:
        db_table = 'search_record'
        verbose_name = '搜索记录'
        verbose_name_plural = '搜索记录'
    class META:
        ordering = ['id']



class Comment(models.Model):
    user_name=models.CharField(max_length=128)
    attration_name=models.CharField(max_length=128)
    comment_text= models.CharField(max_length=512)
    timestamp = models.CharField(max_length=128)
    def __str__(self):
        return self.comment_content
    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = '评论'
    class META:
        ordering = ['id']


class Hot_attraction(models.Model):
    attraction_name=models.CharField(max_length=128)
    location=models.CharField(max_length=128)
    hot_rank = models.IntegerField()
    def __str__(self):
        return self.attraction_name
    class Meta:
        db_table = 'hot_attraction'
        verbose_name = '景点热度'
        verbose_name_plural = '景点热度'
    class META:
        ordering = ['id']

