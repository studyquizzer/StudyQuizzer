from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from user_profile.models import Profile
from users.models import User
from rest_framework import serializers

# from crackerbox_.models import Document, Question
import datetime
from MultiChoice.models import Question as MQuestion
from MultiChoice.models import Vote, Comments, Category

# from crackerbox.utils import unique_slug_generator

# class UserSerializer(serializers.ModelSerializer):
#     email = serializers.CharField(read_only=True, source="user.email")
#     lookup_field = 'slug'
#     class Meta:
#         model = Profile
#         fields = ('id','first_name','last_name', 'email','slug')


class UserSerializer(serializers.ModelSerializer):
    # email = serializers.CharField(read_only=True, source="user.email")
    # username = serializers.CharField(read_only=True, source="user.username")
    lookup_field = "slug"

    class Meta:
        model = User
        fields = ["email", "username"]


class MultiQuestionSerializer(serializers.ModelSerializer):
    # creator = UserSerializer()
    # category = serializers.CharField()
    lookup_field = "slug"

    class Meta:
        model = MQuestion
        fields = "__all__"
        read_only_fields = ["edited", "creator", "slug", "docfile", "category"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"
        read_only_fields = ["creator"]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"
        read_only_fields = ["creator"]


# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ('doc', 'qnNo', 'qnText', 'option1', 'option2', 'option3', 'option4', 'ans')

# class DocumentSerializer(serializers.ModelSerializer):
#     questions = serializers.SerializerMethodField()
#     lookup_field = 'slug'
#     email = serializers.CharField(read_only=True, source="owner.email") #QuestionSerializer(many=True, read_only=True)
#     class Meta:
#         model = Document
#         fields = ('id', 'status', 'questions','email','created_time')

#     def get_questions(self,doc):
#         data = self.context['request'].query_params
#         qns = doc.questions.all()
#         if 'start' in data:
#             try:
#                 startId = int(data['start'])
#                 qns = qns.filter(qnNo__gte=startId)
#             except ValueError:
#                 raise serializers.ValidationError('start is not an integer')

#         if 'end' in data:
#             try:
#                 endId = int(data['end'])
#                 qns = qns.filter(qnNo__lte=endId)
#             except ValueError:
#                 raise serializers.ValidationError('end is not an integer')

#         return QuestionSerializer(qns,many=True).data

# class DocumentOverviewSerializer(serializers.HyperlinkedModelSerializer):
#     #slug = serializers.SlugRelatedField( read_only= True, slug_field='slug')
#     detail = serializers.HyperlinkedIdentityField(view_name='document-detail', lookup_field = 'slug')
#     #lookup_field = 'slug'
#     #docmethod = serializers.ChoiceField(['file','text'], write_only=True)
#     owner = serializers.CharField(read_only=True, source="user")
#     #profile = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='slug')
#     doctext = serializers.CharField(write_only=True, required=False)
#     docTitle = serializers.CharField(write_only=True, required=False)
#     class Meta:
#         model = Document
#         fields = (
#             'id', 'status', 'owner', 'detail',
#             #'docmethod',
#             #'docfile',
#             'doctext','docTitle'
#         )
#         read_only_fields = ('status', 'owner',)
#         extra_kwargs = {
#             'docfile': {
#                 'write_only': True,
#                 'required': False,
#                 'max_length': settings.CRACKERBOX_MAX_UPLOAD
#             },
#             'url':{
#             'lookup_field':'slug'
#             }
#         }

#     def validate(self,data):
#         #if data['docmethod'] == 'text':
#         if not 'doctext' in data:
#             raise serializers.ValidationError('No text supplied!')
#         #dfile = data['doc']
#         doctitle__ = data['docTitle']
#         doctitle_ = data['docTitle'].replace(' ','_')
#         doctitle = doctitle_.lower()
#         date_ = datetime.date.today()
#         date= date_.strftime('%d %b %Y %H %M %S')
#         fpath = default_storage.get_available_name(f'{doctitle}_{date}.txt')
#         savedDoc = default_storage.save(fpath, ContentFile(data['doctext']))
#         docfile = savedDoc
#         # else:
#         #     if not 'docfile' in data:
#         #         raise serializers.ValidationError('No file supplied!')
#         #     docfile = data['docfile']

#         return {
#             'docfile': docfile,
#             'status': Document.COMPLETE,
#             'title':doctitle__
#         }
