from django.test import TestCase
from pytils.translit import slugify
from memories.models import Memory
from vk_auth.models import VkUser


class MemoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = VkUser.objects.create(vk_id=1)
        cls.memory1 = Memory.objects.create(
            user_id=1, name='Place', comment='Comment text', latitude=88.93, longitude=99.45)
        cls.memory2 = Memory.objects.create(
            user_id=1, name='Place', comment='Comment text 2', latitude=99.93, longitude=22.45)

    def test_verbose_names(self):
        memory = self.memory1
        fields_with_verboses = {
            'user': 'Пользователь',
            'name': 'Название',
            'comment': 'Комментарий',
            'latitude': 'Широта',
            'longitude': 'Долгота',
            'slug': 'URL',
        }
        for field, expected_field_label in fields_with_verboses.items():
            with self.subTest(field=field):
                field_label = memory._meta.get_field(field).verbose_name
                self.assertEqual(field_label, expected_field_label)

    def test_save_slug(self):
        memory = Memory.objects.get(id=1)
        correct_slug = slugify(memory.name)
        self.assertEqual(memory.slug, correct_slug)

    def test_save_unique_slug(self):
        memory = Memory.objects.get(id=2)
        correct_slug = slugify(memory.name) + '-2'
        self.assertEqual(memory.slug, correct_slug)

    def test_get_absolute_url(self):
        memory = Memory.objects.get(id=1)
        slug = slugify(memory.name)
        url = '/memory/edit/' + slug
        self.assertEqual(memory.get_absolute_url(), url)

    def test_name_with_coordinates(self):
        memory = Memory.objects.get(id=1)
        expected_name =\
            f'{memory.name}({memory.latitude}, {memory.longitude})'
        self.assertEqual(str(memory), expected_name)
