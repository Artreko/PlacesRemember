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
        correct_slug = slugify(self.memory1.name)
        self.assertEqual(self.memory1.slug, correct_slug)

    def test_save_unique_slug(self):
        correct_slug = slugify(self.memory2.name) + '-2'
        self.assertEqual(self.memory2.slug, correct_slug)

    def test_update_slug(self):
        new_name = 'Место'
        self.memory2.name = new_name
        self.memory2.save()
        self.assertEqual(self.memory2.slug, slugify(new_name))

    def test_get_absolute_url(self):
        slug = slugify(self.memory1.name)
        url = '/memory/edit/' + slug
        self.assertEqual(self.memory1.get_absolute_url(), url)

    def test_name_with_coordinates(self):
        expected_name =\
            f'{self.memory1.name}({self.memory1.latitude}, ' \
            + f'{self.memory1.longitude})'
        self.assertEqual(str(self.memory1), expected_name)
