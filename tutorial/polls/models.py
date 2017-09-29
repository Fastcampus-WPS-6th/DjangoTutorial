from datetime import timedelta

from django.db import models
from django.utils import timezone

"""
class Question
    -> 설문조사 질문
    title = 설문조사 제목 (CharField)
    published_date = 발행 날짜 (DateTimeField)
    
    __str__
    print(Question instance)
        설문조사 ({제목})

class Choice
    -> 선택지
    question = 해당 설문조사 (ForeignKey)
    title = 선택지 제목 (CharField)
    votes = 선택 횟수 (IntegerField)
    
    __str__
    print(Choice instance)
        설문조사 ({설문조사의 제목}) - 선택지 ({제목})
"""


class Question(models.Model):
    title = models.CharField(max_length=50)
    published_date = models.DateTimeField(
        blank=True, null=True
    )

    def __str__(self):
        return f'설문조사 ({self.title})'

    def is_recently(self):
        """
        :return:
        이 Question의 published_date가
        현재시각 기준으로 7일 이내인지 여부 리턴
        (published_date가 None일경우엔 무조건 False)
        """
        return bool(self.published_date) and \
            timezone.now() - self.published_date <= timedelta(days=7)


class Choice(models.Model):
    question = models.ForeignKey(Question)
    title = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} (설문: {self.question.title})'
