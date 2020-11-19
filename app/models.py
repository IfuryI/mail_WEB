from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by("-creation_time")

    def hot_questions(self):
        return self.filter(creation_time__gte=(timezone.now() - timezone.timedelta(days=1))).order_by("-rating")

    def questions_with_tag(self, tag):
        return self.filter(tags__name=tag)


class Question(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Автор')
    creation_time = models.DateTimeField(verbose_name='Время создания')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    votes = models.ManyToManyField('Profile', blank=True, verbose_name='Оценки', through='QuestionVote', related_name="voted_questions", related_query_name="voted_questions")
    tags = models.ManyToManyField('Tag', verbose_name='Теги', related_name='tags', related_query_name='tag')

    title = models.CharField(max_length=60, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def update_rating(self):
        self.rating = QuestionVote.objects.get_rating(self.id)
        self.save()

    def get_answers_count(self):
        return self.answers.count()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerManager(models.Manager):
    def best_answers(self):
        return self.order_by("-rating")


class Answer(models.Model):
    to_Question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='К вопросу', related_name="answers",
                                         related_query_name="answer")

    author = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Автор')
    creation_time = models.DateTimeField(verbose_name='Время создания')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    votes = models.ManyToManyField('Profile', blank=True, verbose_name='Оценки', through='AnswerVote', related_name="voted_answer", related_query_name="voted_answer")

    text = models.CharField(max_length=60, verbose_name='Ответ')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ли')

    objects = AnswerManager()

    def __str__(self):
        return self.text

    def update_rating(self):
        self.rating = AnswerVote.objects.get_rating(self.id)
        self.save()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class TagManager(models.Manager):
    def popular_tag(self):
        pass

class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=30, verbose_name='Тег')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


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


class VoteManager(models.Manager):
    LIKE = 1
    NOT_CLICKED = 1
    DISLIKE = -1

    def get_likes(self, pk):
        return self.filter(id=pk, mark=VoteManager.LIKE).count()

    def get_dislikes(self, pk):
        return self.filter(id=pk, mark=VoteManager.DISLIKE).count()

    def get_rating(self, pk):
        return self.get_likes(pk) - self.get_dislikes(pk)


class QuestionVote(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Кто оценил')
    mark = models.IntegerField(default=VoteManager.NOT_CLICKED, verbose_name='Оценка')

    objects = VoteManager()

    to_Question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='К вопросу')

    def __str__(self):
        return str(self.mark)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class AnswerVote(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Кто оценил')
    mark = models.IntegerField(default=VoteManager.NOT_CLICKED, verbose_name='Оценка')

    objects = VoteManager()

    related_answer = models.ForeignKey('Answer', verbose_name='Оцениваемый ответ', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.mark)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
