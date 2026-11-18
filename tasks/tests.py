from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse("task-list"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('task-list')}",
            fetch_redirect_response=False,
        )

    def test_authenticated_user_only_sees_their_tasks(self):
        own_task = Task.objects.create(
            user=self.user,
            title="My task",
            description="",
            due_date="2026-11-18",
            priority="Medium",
        )
        other_user = User.objects.create_user(
            username="otheruser",
            password="testpassword",
        )
        Task.objects.create(
            user=other_user,
            title="Other task",
            description="",
            due_date="2026-11-18",
            priority="Low",
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse("task-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, own_task.title)
        self.assertNotContains(response, "Other task")
