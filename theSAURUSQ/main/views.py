from django.shortcuts import render
from .models import Question
from django.core.paginator import Paginator

# Create your views here.

#Homepage
def home(request):
    if 'q' in request.GET:
        q=request.GET['q']
        quests=Question.objects.filter(title__icontains=q).order_by('-id')
    else:

        quests=Question.objects.all().order_by('-id')
    paginator=Paginator(quests,1)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request, 'home.html', {'quests':quests})


    #Detail

    def detail(request,id):
        quest=Question.objects.get(pk=id)
        tags=quest.tags.split(',')
        answers=Answer.objects.filter(question=quest)
        answerform=Answerform
        if request.method=='POST':
            answerData=AnswerForm(request.POST)
            if answerData.is_valid():
                answer=answerData.save(commit=False)
                answer.question=quest
                answer.user=request.user
                answer.save()
                messages.success(request,'Answer has been submitted.')
        return render(request, 'detail.html', {
            'quest':quest,
            'tags':tags,
            'answers':answers,
            'answerform':answerform})