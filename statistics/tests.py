from django.test import TestCase
from django.urls import reverse


class QuestionIndexViewTests(TestCase):
    def test_form(self):
        response = self.client.get(reverse('statistics:url'))
        self.assertContains(response, "Please enter URL to check", status_code=200)

    def test_valid_url_with_keywords(self):
        session = self.client.session
        session['url'] = r"http://wp.pl"
        session.save()
        response = self.client.get(reverse('statistics:statistic'))
        self.assertContains(response, r"Statistic for http://wp.pl", status_code=200)
        self.assertContains(response, "Keyword: number of occurrences", status_code=200)
        self.assertContains(response, "Wirtualna Polska", status_code=200)

    def test_valid_url_without_keywords(self):
        session = self.client.session
        session['url'] = r"http://rp.pl"
        session.save()
        response = self.client.get(reverse('statistics:statistic'))
        self.assertContains(response, r"Statistic for http://rp.pl", status_code=200)
        self.assertContains(response, "No keywords are available", status_code=200)

    def test_non_existent_url(self):
        session = self.client.session
        session['url'] = r"http://shasldhasdasdfs.pl"
        session.save()
        response = self.client.get(reverse('statistics:statistic'))
        self.assertEqual(response.client.session['error'], True)
        self.assertRedirects(response, '/url/')
