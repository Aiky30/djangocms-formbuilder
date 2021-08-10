from django.contrib import admin

from .models import Form, FormContent


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    pass


@admin.register(FormContent)
class FormContentAdmin(admin.ModelAdmin):
    pass
