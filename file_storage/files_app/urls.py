from django.urls import path
from files_app.views import DocumentList, AddDocumentView, UpdateDocumentView, \
    download_document_json, export_document_json

urlpatterns = [
    path(r'', DocumentList.as_view(), name='document_list'),
    path(r'create/', AddDocumentView.as_view(), name='document_create'),
    path(r'update/<int:id>/', UpdateDocumentView.as_view(), name='document_update'),
    path(r'json/download/', download_document_json, name='download_documents_json'),
    path(r'json/export/', export_document_json, name='export_documents_json'),
]
