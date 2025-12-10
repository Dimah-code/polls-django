from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from polls.models import Question

import datetime

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def view_response(self):
    return self.client.get(reverse('polls:index'))

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = view_response(self)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question", days=-30)
        response = view_response(self)
        self.assertQuerySetEqual(
            response.context['latest_question_list'],
            [question]
        )
    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question", days=30)
        response = view_response(self)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question", days=-30)
        create_question(question_text="Future question", days=30)

        response = view_response(self)
        self.assertQuerySetEqual(
            response.context['latest_question_list'],
            [question]
        )
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="First Question", days=-30)
        question2 = create_question(question_text="Second Question", days=-5)

        response = view_response(self)
        self.assertQuerySetEqual(
            response.context['latest_question_list'],
            [question2, question1]
        )
