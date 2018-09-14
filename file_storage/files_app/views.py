# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponse

from files_app.utils import search_documents
from files_app import forms
from files_app import models
from files_app.admin import DocumentResource


# Create your views here.


class DocumentList(ListView):
    """
    View to get list of documents
    """
    template_name = "document_list.html"
    model = models.Document
    context_object_name = 'document_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search'] = self.request.GET.get('search', '')
        return context

    def get_queryset(self):
        search_str = self.request.GET.get('search', '')

        object_list = search_documents(search_str)
        return object_list[:10]


class AddDocumentView(CreateView):
    """
    View to add new document
    """

    template_name = 'document_form.html'
    form_class = forms.DocumentForm
    success_url = reverse_lazy('document_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddDocumentView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(AddDocumentView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class UpdateDocumentView(UpdateView):
    """
    View to add modify existing document
    """

    template_name = 'document_form.html'
    form_class = forms.DocumentForm
    success_url = reverse_lazy('document_list')

    def get_object(self, *args, **kwargs):
        document = get_object_or_404(
            models.Document, id=self.kwargs['id']
        )

        if not document.can_be_edited_by_user(self.request.user):
            raise Http404('You are not allowed to edit this object')

        return document

    def form_valid(self, form):

        if not form.instance.can_be_edited_by_user(self.request.user):
            raise Http404('You are not allowed to edit this object')

        obj = form.save()
        return super(UpdateDocumentView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


def download_document_json(request):
    """
        This view will accept filter for documents and return them in JSON format to user
    """

    search_str = request.GET.get('search', '')
    object_list = search_documents(search_str)

    data = DocumentResource().export(object_list)

    response = HttpResponse(content=data.json, content_type='text/plain')
    response['Content-Disposition'] = 'attachment;filename="Documents.json"'

    return response


def export_document_json(request):
    """
        This view will accept filter for documents and then save JSON file to local storage
    """
    from files_app.tasks import export_documents
    search_str = request.GET.get('search', '')

    export_documents.apply_async((search_str,))

    return redirect('document_list')

