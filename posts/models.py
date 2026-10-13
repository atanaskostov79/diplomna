from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Posts(models.Model):
    title = models.CharField(max_length=100)
    entry_title = models.CharField(max_length=200, default="N/A")
    content = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'пост'
        verbose_name_plural = 'постове'

    def __str__(self):
        return self.entry_title


class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=80)
    email = models.EmailField(blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'коментар'
        verbose_name_plural = 'коментари'

    def __str__(self):
        return f'{self.author} on {self.post}'
