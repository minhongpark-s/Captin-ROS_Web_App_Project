from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
#from django.db.models import Q, Count

from ..models import Question
import logging
logger = logging.getLogger('pybo')


def index(request):
    logger.info("INFO 레벨로 출력")
    return render(request, 'pybo/index.html')

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
