from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse
from memories.models import Memory
from vk_auth.models import VkUser
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver


class HomePageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = VkUser.objects.create(vk_id=1)
        cls.user2 = VkUser.objects.create(vk_id=2)
        cls.user3 = VkUser.objects.create(vk_id=3)

        cls.user1_memories_count = 6
        cls.user2_memories_count = 5

        for memory_num in range(cls.user1_memories_count):
            Memory.objects.create(
                user=cls.user1,
                name=f'Palce {memory_num}',
                comment=f'Comment',
                latitude=89.90,
                longitude=54.45,
            )
        for memory_num in range(cls.user2_memories_count):
            Memory.objects.create(
                user=cls.user2,
                name=f'Palce {memory_num + cls.user1_memories_count}',
                comment=f'Comment',
                latitude=89.90,
                longitude=54.45,
            )

    def setUp(self):
        self.guest_client = Client()

        self.user1_client = Client()
        self.user1_client.force_login(self.user1)

        self.user2_client = Client()
        self.user2_client.force_login(self.user2)

    def test_guest_home_page_request(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_authorized_user_home_page_request(self):
        response = self.user1_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_url_name(self):
        self.assertEqual(reverse('home'), '/')

    def test_guest_client_home_page(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)
        memories = response.context['memories']
        self.assertIsNone(memories)
        self.assertContains(response, 'Войти с помощью VK')

    def test_authorized_user_memories_list(self):
        with self.subTest(user=self.user1):
            response = self.user1_client.get('/')
            self.assertEqual(response.status_code, 200)
            memories = response.context['memories']
            self.assertEqual(len(memories), self.user1_memories_count)

        with self.subTest(user=self.user2):
            response = self.user2_client.get('/')
            self.assertEqual(response.status_code, 200)
            memories = response.context['memories']
            self.assertEqual(len(memories), self.user2_memories_count)

    def test_authorized_user_memories_empty_list(self):
        self.user3_client = Client()
        self.user3_client.force_login(self.user3)
        response = self.user3_client.get('/')
        self.assertEqual(response.status_code, 200)
        memories = response.context['memories']
        self.assertEqual(len(memories), 0)
        self.assertContains(response, 'У вас нет ни одного воспоминания')

    def test_authorized_user_memories_append_list(self):
        self.user3_client = Client()
        self.user3_client.force_login(self.user3)
        for i in range(2):
            Memory.objects.create(user=self.user3,
                                  name=f'Метсо {i}',
                                  comment='Comment',
                                  latitude=95.99,
                                  longitude=88.34)
        response = self.user3_client.get('/')
        self.assertEqual(response.status_code, 200)
        memories = response.context['memories']
        self.assertEqual(len(memories), 2)

    def test_user_logout(self):
        self.user1_client.logout()
        response = self.user1_client.get('/')
        self.assertEqual(response.status_code, 200)
        memories = response.context['memories']
        self.assertIsNone(memories)

    def test_urls_uses_correct_template(self):
        response = self.user1_client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class MemoryCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = VkUser.objects.create(vk_id=1)

    def setUp(self):
        self.user_client = Client()
        self.user_client.force_login(self.user)

        self.guest_client = Client()

    def test_memory_create_view_url_name(self):
        self.assertEqual(reverse('memory-create'), '/memory/create')

    def test_authorized_user_memory_create_view_request(self):
        response = self.user_client.get(reverse('memory-create'))
        self.assertEqual(response.status_code, 200)

    def test_memory_create_view_uses_correct_template(self):
        response = self.user_client.get(reverse('memory-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'memories/memory_create_or_update.html')

    def test_guest_create_view_request(self):
        response = self.guest_client.get(reverse('memory-create'))
        self.assertRedirects(response, reverse(
            'vk-auth') + '?next=' + reverse('memory-create'), 302, 302)

    def test_create_memory(self):
        memories_count = len(Memory.objects.all())
        response = self.user_client.post(
            reverse('memory-create'),
            {
                'name': 'Метсо',
                'comment': 'Comment',
                'latitude': 98.123,
                'longitude': 108.99
            }
        )
        self.assertRedirects(response, '/', 302, 200)
        self.assertEqual(len(Memory.objects.all()), memories_count + 1)


class MemoryUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = VkUser.objects.create(vk_id=1)
        cls.user2 = VkUser.objects.create(vk_id=2)

        cls.memory = Memory.objects.create(
            user=cls.user1,
            name='Метсо',
            comment='Comment',
            latitude=95.99,
            longitude=88.34)

    def setUp(self):
        self.user1_client = Client()
        self.user1_client.force_login(self.user1)

        self.user2_client = Client()
        self.user2_client.force_login(self.user2)

        self.guest_client = Client()

    def test_memory_update_view_url_name(self):
        self.assertEqual(
            reverse('memory-edit', kwargs={'slug': 'slug'}), '/memory/edit/slug')

    def test_authorized_user_memory_edit_view_request(self):
        response = self.user1_client.get(
            reverse('memory-edit', kwargs={'slug': self.memory.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_another_user_memory_edit_view(self):
        response = self.user2_client.get(
            reverse('memory-edit', kwargs={'slug': self.memory.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_memory_guest_memory_edit_request(self):
        url = reverse('memory-edit', kwargs={'slug': self.memory.slug})
        response = self.guest_client.get(url)
        self.assertRedirects(response, reverse(
            'vk-auth') + '?next=' + url, 302, 302)

    def test_user_memory_edit_memory_does_not_exist(self):
        url = reverse('memory-edit', kwargs={'slug': 'some_palace'})
        response = self.user1_client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_guest_memory_edit_memory_does_not_exist(self):
        url = reverse('memory-edit', kwargs={'slug': 'some_palace'})
        response = self.guest_client.get(url)
        self.assertRedirects(response, reverse(
            'vk-auth') + '?next=' + url, 302, 302)

    def test_memory_update_view_uses_correct_template(self):
        response = self.user1_client.get(
            reverse('memory-edit', kwargs={'slug': self.memory.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'memories/memory_create_or_update.html')

    def test_update_memory(self):
        memories_count = len(Memory.objects.all())
        response = self.user1_client.post(
            reverse('memory-edit', kwargs={'slug': self.memory.slug}),
            {
                'name': 'Метсо',
                'comment': 'Comment',
                'latitude': 98.123,
                'longitude': 108.99
            }
        )
        self.assertRedirects(response, '/', 302, 200)
        self.assertEqual(len(Memory.objects.all()), memories_count)
