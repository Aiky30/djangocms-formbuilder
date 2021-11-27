from django.contrib import admin

from djangocms_versioning.admin import ExtendedVersionAdminMixin

from .models import Form, FormContent


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    pass


@admin.register(FormContent)
class FormContentAdmin(ExtendedVersionAdminMixin, admin.ModelAdmin):
    pass
