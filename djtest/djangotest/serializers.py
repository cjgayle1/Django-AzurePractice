from django.contrib.auth.models import User, Group
from djangotest.models import Document
from rest_framework import serializers


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name', ]

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['document_text', 'doc_id', 'document_file']

class DocumentGUIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['guid']