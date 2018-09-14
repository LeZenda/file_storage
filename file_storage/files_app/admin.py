from django.contrib import admin
from import_export import resources

from files_app import models
# Register your models here.


class DocumentResource(resources.ModelResource):

    class Meta:
        model = models.Document


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'user', 'source', 'created', 'updated', 'date_added')
    list_per_page = 100
    search_fields = ('source__name', 'source__sid', 'source__url',
                     'user__username',
                     'created', 'updated', 'title', 'text')


admin.site.register(models.Source)
admin.site.register(models.Document, DocumentAdmin)
