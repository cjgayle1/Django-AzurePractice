from django.urls import path

from djangotest.views import DocumentUploadView, DocumentURLView, DeleteDocument, GetAllDocuments, DeleteAllDocuments

urlpatterns = [
    # path('file/', FileUploadView.as_view(), name='file_upload'),
    path('doc/', DocumentUploadView.as_view(), name='doc_upload'),
    path('getdoc/', DocumentURLView.as_view(), name='doc_view'),
    path('deldoc/', DeleteDocument.as_view(), name= 'doc_delete'),
    path('alldocs/', GetAllDocuments.as_view(), name= 'doc_all'),
    path('delalldocs/', DeleteAllDocuments.as_view(), name= 'delete_docs_all')
]