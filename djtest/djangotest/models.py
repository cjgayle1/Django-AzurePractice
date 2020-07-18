import uuid
from django.db import models
from django.db.models.manager import EmptyManager
# from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient

# Create your models here.
def getUploadFolder(instance, fileName):
    return '{0}/{1}'.format(str(instance.doc_id), fileName)
class Document(models.Model):
    document_text = models.CharField(('Document Title'), max_length=25)
    doc_id = models.UUIDField(('Document ID'), primary_key=True, max_length=35, unique=True, default= uuid.uuid4, editable=False)
    document_file = models.FileField(("Document File"),upload_to=getUploadFolder, default='.txt', blank= False)
    def __str__(self):
        return self.doc_id
    # class Meta:
    #     verbose_name = ('document')
    #     verbose_name_plural = ('documents')



# class DocumentStorage(models.Model):
#     name = models.CharField(max_length=100)
#     doc = models.FileField(upload_to='docstorage')
#     def __str__(self):
#         return self.name