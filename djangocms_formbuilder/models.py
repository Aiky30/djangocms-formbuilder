from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models, transaction
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin, Placeholder
from cms.models.fields import PlaceholderRelationField
from cms.toolbar.utils import get_object_preview_url
from cms.utils.i18n import get_current_language


class Form(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)


class FormContent(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    placeholders = PlaceholderRelationField()
    placeholder_slotname = 'content'
    language = models.CharField(
        max_length=10,
        choices=settings.LANGUAGES,
        default=get_current_language,
    )

    class Meta:
        verbose_name = _('form content')
        verbose_name_plural = _('form contents')

    def __str__(self):
        return '{} ({})'.format(self.name, self.language)

    @cached_property
    def placeholder(self):
        try:
            return self.placeholders.get(slot=self.placeholder_slotname)
        except Placeholder.DoesNotExist:
            from cms.utils.placeholder import rescan_placeholders_for_obj

            rescan_placeholders_for_obj(self)
            return self.placeholders.get(slot=self.placeholder_slotname)

    def get_placeholders(self):
        return [self.placeholder]

    def get_absolute_url(self):
        # FIXME: Will need to supply language here!!!
        return get_object_preview_url(self)

    def get_template(self):
        return 'djangocms_formbuilder/form_content_structure.html'
