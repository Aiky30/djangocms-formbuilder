from django.template.response import TemplateResponse


def render_form_content(request, form_content):
    template = 'djangocms_formbuilder/form_content_preview.html'
    context = {'form_content': form_content}
    return TemplateResponse(request, template, context)
