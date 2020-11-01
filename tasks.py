# from django.core.management.base import BaseCommand, CommandError
# import shelve
# from users.models import User
# from django.conf import settings
# from qa.models import Answer, AnswerComment, QuestionComment
# from crackerbox_.models import Document
# from django.core.mail import send_mail
# from datetime import datetime, timedelta
# from django.utils import timezone


# def sendemail(userEmail, u, q, a, qc, ac, start, end):
#     subject = 'Usage Report'
#     message = f'''Dear Administrator,
#             between {start} and {end},
#             {u} users registered,
#             {q} questions were asked,
#             {a} answer were given,
#             {qc} question comments were made,
#             {ac} answer comments were made.
#              '''
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [userEmail,]
#     send_mail( subject, message, email_from, recipient_list )

# # User = settings.AUTH_USER_MODEL

# # Question = settings.QUESTION_MODEL

# # Answer = settings.ANSWER_MODEL

# # AnswerComment = settings.ANSWER_COMMENT_MODEL

# # QuestionComment = settings.QUESTION_COMMENT_MODEL

# # Document = settings.DOCUMENT_MODEL


# class Command(BaseCommand):
#     help = 'Command to do........'

#     def add_argument(self, parser):
#         pass

#     def handle(self, *args, **options):
#         try:
#             range = shelve.open("time.dat")
#             first = range['first']
#             last = None

#             if first:
#                 last = timezone.make_aware(datetime(2019, 4, 30))
#             else:
#                 last = range["last"]

#             now = timezone.now

#             no_users = len(User.objects.filter(timestamp__gte = last, timestamp__lt = now))
#             no_question = len(Question.objects.filter(pub_date__gte = last, pub_date__lt = now))
#             no_answer = len(Answer.objects.filter(pub_date__gte = last, pub_date__lt = now))
#             no_question_comment = len(QuestionComment.objects.filter(pub_date__gte = last, pub_date__lt = now))
#             no_answer_comment = len(AnswerComment.objects.filter(pub_date__gte = last, pub_date__lt = now))

#             sendemail('samajisegiri@gmail.com',
#                         no_users,
#                         no_question,
#                         no_answer,
#                         no_question_comment,
#                         no_answer_comment
#                         )


#             range['first'] = False
#             range['last'] = timezone.now()
#             range.close()

#         except Exception as e:
#             CommandError(repr(e))
