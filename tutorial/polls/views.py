from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from .models import Question, Choice


def index(request):
    """
    1. 모든 Question을 출력하는 View(Controller)구현
    context dict객체를 생성,
        'questions'키에
        모든 Question객체를 DB에서 가져온 QuerySet을 할당

    render함수를 사용해서 'polls/index.html'을
    context와 함께 rendering한 결과를 리턴

    2. 템플릿 파일들이 있는 디렉토리를 settings.py에 설정
        settings.py에 TEMPLATE_DIR를 지정
        TEMPLATE = ...설정의 'DIRS'키를 갖는 리스트에 TEMPLATE_DIR추가

    3. 템플릿 파일 생성, Question들을 출력
        polls/index.html파일을 생성
        해당 템플릿에 'questions'키로 전달된 QuerySet을 for loop하며
        각 loop에 해당하는 Question객체의 title을 출력
    :param request:
    :return:
    """
    context = {
        'questions': Question.objects.all(),
    }
    return render(request, 'polls/index.html', context)


def question_detail(request, pk):
    """
    context에 pk에 해당하는 Question을 전달
    polls/question.html 에서 Question의 title을 표시

    url
        polls/<question_pk>/$
    :param request:
    :param pk:
    :return:
    """
    question = Question.objects.get(pk=pk)
    context = {
        'question': question,
    }
    return render(request, 'polls/question.html', context)


def vote(request, pk):
    """
    choice_pk에 request.POST로 전달된 choice의 pk값을 할당
    선택한 Choice를 choice변수에 할당
    votes값을 1증가 후 DB에 저장
    이후 투표한 Choice가 속한 question_detail로 이동

    0. question변수에 pk가 question_pk인 Question객체를 DB에서 가져와 할당
    1. choice변수에 pk가 choice_pk인 Choice객체를 DB에서 가져와 할당
    2. choice의 votes속성값을 1증가
    3. choice의 변경사항을 DB에 저장
    4. redirect(<view_name>, question_pk=question.pk) 를 사용해서 리디렉션 리턴
    """
    if request.method == 'POST':

        # 누군가 form의 action에 있는 question_pk값을 변형해서 보냈을 경우 발생 가능
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return redirect('index')

        try:
            # 누군가 input의 value에 있는 choice_pk값을 변형해서 보냈을 경우
            # Choice.DoesNotExist발생 가능
            choice_pk = request.POST['choice_pk']
            choice = question.choice_set.get(pk=choice_pk)
            choice.votes += 1
            choice.save()
        except MultiValueDictKeyError:
            # choice_pk가 전달되지 않았을 경우 (선택하지 않았을 경우)
            print('KeyError!')
        except Choice.DoesNotExist:
            print('Choice.DoesNotExist! (진짜 없거나, question에 해당하는 Choice가 아니거나)')
        return redirect('question_detail', pk=question.pk)
    return HttpResponse('Permission denied', status=403)
