from django.test import TestCase
from .forms import AddUrlForm
from django_webtest import WebTest
	

# Create your tests here.

class InputUrlTests(TestCase):

	def test_homepage(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	def test_add_url_form_label(self):
		form = AddUrlForm()
		print form.fields["Add_URL"].label
		self.assertTrue(form.fields['Add_URL'].label == None)


class EntryViewTest(WebTest):

	def test_view_page(self):
		page = self.app.get('/')
		self.assertEqual(len(page.forms), 1)