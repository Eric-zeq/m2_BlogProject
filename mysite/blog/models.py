from django.db import models
from django.contrib.auth.models import User
# Create your models here.

STATUS=(
    (0,'Draft'),
    (1,'Publish')
)

class Post(models.Model):
        title = models.CharField(max_length=200, unique=True)
        slug = models.SlugField(max_length=200, unique=True)
        author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
        updated_on = models.DateTimeField(auto_now= True)
        content = models.TextField()
        created_on = models.DateTimeField(auto_now_add=True)
        status = models.IntegerField(choices=STATUS, default=0)

        class Meta:
            #查询数据库时根据created_on 字段降序，'-'negative  符号表示降序
            ordering = ['-created_on']

        def __str__(self):
            return self.title
        
        def save(self, *args, **kwargs):
        # 确保至少有一个默认的 User 对象存在
            if not User.objects.exists():
                User.objects.create_superuser(username='default_user', password='default_password')
            # 设置默认的 User 对象
            default_user = User.objects.get(username='default_user')
            if not self.author:
                self.author = default_user
            super().save(*args, **kwargs)



class Comment(models.Model):
        user = models.ForeignKey(User, on_delete= models.CASCADE,related_name='posts_comment')
        post =models.ForeignKey(Post,on_delete=models.CASCADE,default=1)
        content = models.TextField()
        created_on = models.DateTimeField(auto_now_add=True)
        active = models.BooleanField(default=False)

        class Meta:
            #查询数据库时根据created_on 字段降序，'-'negative  符号表示降序
            ordering = ['-created_on']

            def __str__(self):
                return f"Comment by {self.user} on {self.post}"
    