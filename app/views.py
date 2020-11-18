from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

questions = [
    {
        'id': i,
        'title': 'Мой вопрос ' + str(i),
        'text': "Text text Text text Text text Text text Text text",
        'answer_count': 80,
        'like_count': 10,
        'tags': ["tag1", "tag2"]
    } for i in range(80)
]

def paginate(objects_list, request, per_page=20):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return page

def hot_questions(request):
    one_page_questions = paginate(questions, request, 20)
    return render(request, 'hot_questions.html', {
        'blocks': one_page_questions
        })

def new_questions(request):
    one_page_questions = paginate(questions, request, 20)
    return render(request, 'new_questions.html', {
        'blocks': one_page_questions,
        })

def questions_by_tag(request, tag):
    one_page_questions = paginate(questions, request, 20)
    return render(request, 'questions_by_tag.html', {
        'tag': tag,
        'blocks': one_page_questions,
    })

def question(request, pk):
    question = questions[pk - 1]
    answers = [
        {
            'id': i,
            'title': 'Ответ ' + str(i),
            'text': "Text text Text text Text text Text text Text text",
            'like_count': 10,
            'isRight': 0
        } for i in range(80)
    ] 

    content = paginate(answers, request, 5);

    return render(request, 'question.html', {
        'question': question,
        'blocks': content,
        })

def login(request):
    return render(request, 'login.html', {})

def signup(request):
    return render(request, 'signup.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def create_question(request):
    return render(request, 'create_question.html', {})