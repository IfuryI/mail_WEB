from django.db import models

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	name = models.CharField(max_length=30, verbose_name='Имя')
	nickname = models.CharField(max_length=30, verbose_name='Никнейм')
	email = models.EmailField(max_length=50, verbose_name='Почта')

	profile_pic = models.ImageField(verbose_name='Фото')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'


class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=30, verbose_name='Тег')

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Question(models.Model):

	creator = models.ForeignKey('Profile', on_delete=models.CASCADE)

	title = models.CharField(max_length=60, verbose_name='Заголовок')
	text = models.TextField(verbose_name='Текст')

	rating = models.IntegerField(default=0, verbose_name='Рейтинг')

 	creation_time = models.DateTimeField(verbose_name='Время создания')
 	