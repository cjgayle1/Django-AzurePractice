import uuid
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from djangotest.models import Document
from .serializers import DocumentSerializer, DocumentGUIDSerializer
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta
from azure.common import AzureMissingResourceHttpError
from azure.storage.common.storageclient import StorageClient
# from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ResourceTypes, AccountSasPermissions, generate_account_sas
from azure.storage.blob import baseblobservice, BlockBlobService, sharedaccesssignature, models, AppendBlobService, BlobPermissions, ContentSettings
from azure.storage.blob.baseblobservice import BaseBlobService
from azure.storage.common.models import ResourceTypes, AccountPermissions
from djtest.settings import AZURE_ACCOUNT_NAME, AZURE_CONTAINER, AZURE_CONNECTION_STRING

class DocumentUploadView(APIView):
    parser_class = (FileUploadParser,)
    def post(self, request, *args, **kwargs):

      doc_serializer = DocumentSerializer(data=request.data)

      if doc_serializer.is_valid():
          doc_serializer.save()
          return Response(doc_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(doc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentURLView(APIView):
    def get(self, request, *args, **kwargs):
        blob_service_client = BaseBlobService(connection_string=AZURE_CONNECTION_STRING)
        qryParams = request.query_params
        guid = qryParams['guid']

        try:
            docInstance = Document.objects.get(doc_id= qryParams['guid'])
        except ValidationError:
            return Response('Not a valid GUID')
        except Document.DoesNotExist:
            return Response('This file does not exist') 
        except(Exception):
            raise Exception
        sas_uri = "https://" + AZURE_ACCOUNT_NAME + ".blob.core.windows.net/" + AZURE_CONTAINER + "/" + str(docInstance.document_file) + "?"
        # sas_token = blob_service_client.generate_account_shared_access_signature(
        #     ResourceTypes(object=True),
        #     AccountPermissions(read=True, write=True, delete=True, list=True, add=True, create=True, update=True, process= True, _str='e7254eeb-3c5f-45da-8652-a020ee2a4b7c'),
        #     datetime.utcnow() + timedelta(minutes=1)
        # )
        sas_token = blob_service_client.generate_blob_shared_access_signature(AZURE_CONTAINER, str(docInstance.document_file), permission=AccountPermissions(read=True), expiry=datetime.utcnow() + timedelta(minutes=1)
        )

        return Response(sas_uri + sas_token)

class DeleteDocument(APIView):
    def delete(self, request, *args, **kwargs):
        blob_service_client = BaseBlobService(connection_string=AZURE_CONNECTION_STRING)
        qryParams = request.query_params
        guid = qryParams['guid']
        try:
            docInstance = Document.objects.get(doc_id= guid)
        except ValidationError:
            return Response('Not a valid GUID')
        except Document.DoesNotExist:
            return Response('This file does not exist')
        except(Exception):
            raise Exception
        try:
            blob_service_client.delete_blob(AZURE_CONTAINER, docInstance.document_file)
        except AzureMissingResourceHttpError:
            return Response('This file does not exist')
        docInstance.delete()
        # if(docInstance.exists()):
        #     return Response('Did not delete from django')
        return Response('Success')

class GetAllDocuments(APIView):
    def get(self, request, *args, **kwargs):
        all_docs = Document.objects.all()
        total_docs = 0
        b = []
        for Document.object in all_docs:
            total_docs += 1
            cur_doc = Document.object
            b.append(cur_doc.document_text + ' - ' + str(cur_doc.doc_id))
        b.insert(0, 'Total Documents: ' + str(total_docs))
        return Response(b)

class DeleteAllDocuments(APIView):
     def delete(self, request, *args, **kwargs):
        all_docs = Document.objects.all()
        blob_service_client = BaseBlobService(connection_string=AZURE_CONNECTION_STRING)
        for Document.object in all_docs:
            try:
                blob_service_client.delete_blob(AZURE_CONTAINER, Document.object.document_file)
            except AzureMissingResourceHttpError:
                return Response('Document in Django is not in azure')
        try:
            all_docs.delete()
        except AssertionError:
            return Response('No files to delete')
        return Response('Success')