from django.db import models

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


class Choice(models.Model):
    question = models.ForeignKey(Question)
    title = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)
