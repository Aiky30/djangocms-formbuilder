from cms.api import create_page
from cms.test_utils.testcases import CMSTestCase


class CMSIntegrationTestCase(CMSTestCase):

    def test_can_create_page(self):
        page = create_page("my page", "nav_playground.html", "en")

        self.assertTrue(page)
