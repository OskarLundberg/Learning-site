from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Course, Step


class CourseModelTests(TestCase):
    def test_course_creation(self):
        """
        Tests so the course created_at time is less or equal to the time 'now'
        """
        course = Course.objects.create(
            title="Python Regular Expressions",
            description="Lear to write regular expressions in Python"
        )
        now = timezone.now()
        self.assertLessEqual(course.created_at, now)


class StepModelTests(TestCase):
    def test_step_order(self):
        """
        Tests so a Step's default order is 0
        """
        step = Step.objects.create(
            title="Do the thing",
            description="m2m2",
            content = "m3m3",
            course=Course.objects.create(
            title="Python Regular Expressions",
            description="Lear to write regular expressions in Python"
            )
        )
        self.assertEqual(step.order, 0)


class CourseViewsTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Testing",
            description="Lear to write tests in python",
        )
        self.course2 = Course.objects.create(
            title="New Course",
            description="A new course"
        )
        self.step = Step.objects.create(
            title="Introduction to Doctests",
            description="Learn to write tests in your docstrings.",
            course=self.course
        )

    def test_course_list_view(self):
        resp = self.client.get(reverse("courses:list"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context["courses"])
        self.assertIn(self.course2, resp.context["courses"])
        self.assertNotIn(self.step, resp.context["courses"])
        self.assertTemplateUsed(resp, "courses/course_list.html")
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        """
        Checks so 'course' can be found in the view with pk=1
        """
        resp = self.client.get(reverse("courses:detail", args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course, resp.context["course"])
        self.assertNotEqual(self.course2, resp.context["course"])
        self.assertTemplateUsed(resp, "courses/course_detail.html")
        self.assertContains(resp, self.course.title)

    def test_step_detail_view(self):
        resp = self.client.get(reverse("courses:step", kwargs={
                    "course_pk": self.course.pk,
                    "step_pk": self.step.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.step, resp.context["step"])

        self.assertTemplateUsed(resp, "courses/step_detail.html")
        self.assertContains(resp, self.step.title)
