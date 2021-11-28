from django.contrib.sites.models import Site

from cms.api import add_plugin, create_page
from cms.models import PageContent
from cms.test_utils.testcases import CMSTestCase
from cms.toolbar.utils import get_object_edit_url

from djangocms_versioning.models import Version

from djangocms_formbuilder.models import Form, FormContent


class VersioningIntegrationTestCase(CMSTestCase):
    def test_version_copy_method(self):
        """
        Creating a draft version from a published version copies the form correctly
        """
        self.assertTrue(False)


class VersioningCMSPageIntegrationTestCase(CMSTestCase):
    def setUp(self):
        self.language = "en"
        self.user = self.get_superuser()
        self.site = Site.objects.first()
        self.form = Form.objects.create(site=self.site)
        self.form_content = FormContent.objects.create(
            form=self.form,
            name="Draft form",
            language=self.language,
        )
        # Publish the form
        self.form_content_version = Version.objects.create(
            content=self.form_content,
            created_by=self.user,
        )

        # Create a page
        self.page = create_page(
            title="help",
            template="page.html",
            language=self.language,
            created_by=self.user,
        )
        # Publish the page content
        self.published_pagecontent = PageContent._base_manager.filter(page=self.page, language=self.language).first()
        published_pagecontent_version = self.published_pagecontent.versions.first()
        published_pagecontent_version.publish()
        # Create a draft page_content
        draft_pagecontent_version = published_pagecontent_version.copy(self.user)
        self.draft_pagecontent = draft_pagecontent_version.content

    def test_edit_url_published_page_rendering_published_form(self):
        self.form_content_version.publish(user=self.get_superuser())

        add_plugin(
            self.published_pagecontent.placeholders.get(slot="content"),
            "FormPlugin",
            self.language,
            form=self.form,
        )

        request_url = get_object_edit_url(self.published_pagecontent, self.language)
        with self.login_user_context(self.user):
            response = self.client.get(request_url)

        self.assertContains(response, "Published form")
        self.assertNotIn("Draft form", str(response.content))

    def test_edit_url_draft_page_rendering_published_form(self):
        self.form_content_version.publish(user=self.get_superuser())

        add_plugin(
            self.draft_pagecontent.placeholders.get(slot="content"),
            "FormPlugin",
            self.language,
            form=self.form,
        )

        request_url = get_object_edit_url(self.draft_pagecontent, self.language)
        with self.login_user_context(self.user):
            response = self.client.get(request_url)

        self.assertContains(response, "Published form")
        self.assertNotIn("Draft form", str(response.content))

    def test_edit_url_published_page_rendering_draft_form(self):
        add_plugin(
            self.published_pagecontent.placeholders.get(slot="content"),
            "FormPlugin",
            self.language,
            form=self.form,
        )

        request_url = get_object_edit_url(self.published_pagecontent, self.language)
        with self.login_user_context(self.user):
            response = self.client.get(request_url)

        self.assertContains(response, "Draft form")
        self.assertNotIn("Published form", str(response.content))

    def test_edit_url_draft_page_rendering_draft_form(self):
        add_plugin(
            self.draft_pagecontent.placeholders.get(slot="content"),
            "FormPlugin",
            self.language,
            form=self.form,
        )

        request_url = get_object_edit_url(self.draft_pagecontent, self.language)
        with self.login_user_context(self.user):
            response = self.client.get(request_url)

        self.assertContains(response, "Draft form")
        self.assertNotIn("Published form", str(response.content))

    def test_live_url_published_page_draft_form(self):
        add_plugin(
            self.published_pagecontent.placeholders.get(slot="content"),
            "FormPlugin",
            self.language,
            form=self.form,
        )

        request_url = self.page.get_absolute_url(self.language)
        with self.login_user_context(self.user):
            response = self.client.get(request_url)

        self.assertContains(response, "Draft form")
        self.assertNotIn("Published form", str(response.content))

    def test_live_url_published_page_published_form(self):
        self.form_content_version.publish(user=self.get_superuser())

        add_plugin(
            self.published_pagecontent.placeholders.get(slot="content"),
            "FormPlugin",
            self.language,
            form=self.form,
        )

        request_url = self.page.get_absolute_url(self.language)
        with self.login_user_context(self.user):
            response = self.client.get(request_url)

        self.assertContains(response, "Published form")
        self.assertNotIn("Draft form", str(response.content))
