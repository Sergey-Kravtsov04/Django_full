from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    date_published = models.DateField(default=timezone.now, verbose_name="Дата публикации")
    image = models.ImageField(upload_to="images/", verbose_name="Изображение")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", null=True, blank=True)

    def __str__(self):  #Дандр-метод. Возвращает строковое представление объекта. Возвращаем название блога, чтобы в панели админа они не отображались как BlogPost.obj
        return str(self.title)
    class Meta:  #Представление в ед и мн числе
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"

    def get_absolute_url(self):
        return reverse("main:main_detail", kwargs={"pk": self.pk})

class Comment(models.Model):  #Модель комментов
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, verbose_name="Блок")
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Автор",null=True,blank=True)
    text = models.TextField(verbose_name="Текст комментария")
    date_published = models.DateField(default=timezone.now, verbose_name="Дата публикации")

    def __str__(self):
        return str(self.text)
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
