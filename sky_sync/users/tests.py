from django.test import TestCase
from django.urls import reverse
from users.models import User


class AboutViewTest(TestCase):
    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/about.html')


class LandingViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_authenticated_user_redirect_to_dashboard(self):
        self.client.login(username='testuser', password='testpassword')

        response = self._call_url('landing-page', 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_unauthenticated_user_render_template(self):
        response = self._call_url('landing-page', 200)
        self.assertTemplateUsed(response, 'users/landing_page.html')

    def _call_url(self, url: str, status_code: int):
        url = reverse(url)
        result = self.client.get(url)
        self.assertEqual(result.status_code, status_code)
        return result
