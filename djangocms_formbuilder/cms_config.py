from cms.app_base import CMSAppConfig
from cms.models import Placeholder
from cms.utils.i18n import get_language_tuple

from djangocms_versioning.datastructures import VersionableItem

from .models import FormContent
from .rendering import render_form_content


def copy_form_content(original_content):
    """
    Copy the FormContent object and deepcopy its
    placeholders and plugins.
    """
    # Copy content object
    content_fields = {
        field.name: getattr(original_content, field.name)
        for field in FormContent._meta.fields
        # Don't copy the pk as we're creating a new obj.
        # The creation date should reflect the date it was copied on,
        # so don't copy that either.
        if field.name not in (FormContent._meta.pk.name, "creation_date")
    }

    new_content = FormContent.objects.create(**content_fields)

    # Copy placeholders
    new_placeholders = []
    for placeholder in original_content.placeholders.all():
        placeholder_fields = {
            field.name: getattr(placeholder, field.name)
            for field in Placeholder._meta.fields
            # don't copy primary key because we're creating a new obj
            # and handle the source field later
            if field.name not in [Placeholder._meta.pk.name, "source"]
        }
        if placeholder.source:
            placeholder_fields["source"] = new_content
        new_placeholder = Placeholder.objects.create(**placeholder_fields)
        # Copy plugins
        placeholder.copy_plugins(new_placeholder)
        new_placeholders.append(new_placeholder)
    new_content.placeholders.add(*new_placeholders)

    return new_content


class FormBuilderCMSConfig(CMSAppConfig):
    cms_enabled = True
    cms_toolbar_enabled_models = [(FormContent, render_form_content)]
    djangocms_versioning_enabled = True
    versioning = [
        VersionableItem(
            content_model=FormContent,
            grouper_field_name='form',
            extra_grouping_fields=["language"],
            version_list_filter_lookups={"language": get_language_tuple},
            copy_function=copy_form_content,
        ),
    ]
