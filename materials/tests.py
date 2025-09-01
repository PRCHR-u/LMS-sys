from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import Course, Lesson, Subscription

User = get_user_model()


class MaterialsTestCase(APITestCase):

    def setUp(self):
        """Заполнение базы данных тестовыми данными"""
        self.moderator_group, _ = Group.objects.get_or_create(name='Moderator')

        self.user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='testpassword'
        )

        self.moderator = User.objects.create_user(
            email='moderator@test.com',
            username='testmoderator',
            password='modpassword'
        )
        self.moderator.groups.add(self.moderator_group)
        
        self.course = Course.objects.create(
            title='Test Course',
            description='Course for testing purposes',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Lesson for testing purposes',
            course=self.course,
            owner=self.user,
            video_url='https://www.youtube.com/watch?v=example'
        )

    def test_lesson_create(self):
        """Тестирование создания урока"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Lesson',
            'description': 'A brand new lesson',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com/watch?v=new_example'
        }
        response = self.client.post(reverse('materials:lesson-list'), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(title='New Lesson').exists())

    def test_lesson_list(self):
        """Тестирование получения списка уроков"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('materials:lesson-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(response.data.get('results')[0]['title'], self.lesson.title)

    def test_lesson_retrieve(self):
        """Тестирование получения одного урока"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('materials:lesson-detail', args=[self.lesson.pk]))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_lesson_update_by_owner(self):
        """Тестирование обновления урока владельцем"""
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Lesson Title'}
        response = self.client.patch(reverse('materials:lesson-detail', args=[self.lesson.pk]), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson Title')

    def test_lesson_update_by_moderator(self):
        """Тестирование обновления урока модератором"""
        self.client.force_authenticate(user=self.moderator)
        data = {'title': 'Updated by Moderator'}
        response = self.client.patch(reverse('materials:lesson-detail', args=[self.lesson.pk]), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated by Moderator')

    def test_lesson_delete_by_owner(self):
        """Тестирование удаления урока владельцем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('materials:lesson-detail', args=[self.lesson.pk]))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())
        
    def test_lesson_delete_by_moderator_is_forbidden(self):
        """Тестирование запрета удаления урока модератором"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(reverse('materials:lesson-detail', args=[self.lesson.pk]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_subscription_create(self):
        """Тестирование создания подписки на курс"""
        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.id}
        response = self.client.post(reverse('materials:subscription'), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_delete(self):
        """Тестирование удаления подписки на курс"""
        Subscription.objects.create(user=self.user, course=self.course)
        
        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.id}
        response = self.client.post(reverse('materials:subscription'), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
