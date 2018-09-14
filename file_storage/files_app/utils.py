from django.db.models import Q

from files_app import models


def search_documents(search_str):
    """
    :param search_str: search string by which Documents are searched
    :return: QuerySet of resulting documents
    """

    if search_str != '':
        object_list = models.Document.objects.filter(Q(source__name__icontains=search_str) |
                                                     Q(source__sid__icontains=search_str) |
                                                     Q(source__url__icontains=search_str) |
                                                     Q(user__username__icontains=search_str) |
                                                     Q(created__icontains=search_str) |
                                                     Q(updated__icontains=search_str) |
                                                     Q(title__icontains=search_str) |
                                                     Q(text__icontains=search_str))
    else:
        object_list = models.Document.objects.all()
    return object_list
