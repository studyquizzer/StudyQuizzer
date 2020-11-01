from django.core.mail import send_mail
from django.db.models import Count
from threading import Thread

from . import models

# !!!Needs Review


def check_question():
    questions = models.Question.objects.annotate(
        num_flag=Count("flag_count")
    ).filter(num_flag__gte=3)
    if questions.exists():
        users = [user_.user for user_ in questions]
        for user in users:
            user.is_advanced = False
            user.is_resolver = False
            user.is_reader = True
            user.save()


def check_answer():
    answer = models.Answer.objects.annotate(
        num_flag=Count("flag_count")
    ).filter(num_flag__gte=3)
    if answer.exists():
        users = [user_.user for user_ in answer]
        for user in users:
            user.is_advanced = False
            user.is_resolver = False
            user.is_reader = True
            user.save()


def check_answer_comment():
    answer_comment = models.AnswerComment.objects.annotate(
        num_flag=Count("flag_count")
    ).filter(num_flag__gte=3)
    if answer_comment.exists():
        users = [user_.user for user_ in answer_comment]
        for user in users:
            user.is_advanced = False
            user.is_resolver = False
            user.is_reader = True
            user.save()


def check_question_comment():
    queston_comment = models.QuestionComment.objects.annotate(
        num_flag=Count("flag_count")
    ).filter(num_flag__gte=3)
    if queston_comment.exists():
        users = [user_.user for user_ in queston_comment]
        for user in users:
            user.is_advanced = False
            user.is_resolver = False
            user.is_reader = True
            user.save()


def process_flags():
    check_question_ = Thread(target=check_question)
    check_answer_ = Thread(target=check_answer)
    check_answer_comment_ = Thread(target=check_answer_comment)
    check_question_comment_ = Thread(target=check_question_comment)
    threads = []
    threads.append(check_question_)
    threads.append(check_answer_)
    threads.append(check_answer_comment_)
    threads.append(check_question_comment_)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    sendemail("illustriousht@gmail.com")


# process_flags()


def sendemail(userEmail):
    subject = "Flag Report"
    message = " Flagging done succesfully "
    email_from = models.settings.EMAIL_HOST_USER
    recipient_list = [
        userEmail,
    ]
    send_mail(subject, message, email_from, recipient_list)
