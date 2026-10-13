from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from posts.forms import CommentForm
from posts.models import Category, Comment, Posts


class CategoryModelTests(TestCase):
    def test_str_returns_name(self):
        category = Category.objects.create(name='Наука', slug='nauka')
        self.assertEqual(str(category), 'Наука')

    def test_categories_are_ordered_by_name(self):
        Category.objects.create(name='Ябълка', slug='test-yabalka')
        Category.objects.create(name='Авокадо', slug='test-avokado')
        names = list(
            Category.objects.filter(slug__in=['test-yabalka', 'test-avokado']).values_list('name', flat=True)
        )
        self.assertEqual(names, ['Авокадо', 'Ябълка'])


class PostModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Тест Свят', slug='test-svyat')
        self.post = Posts.objects.create(
            title='Репортаж',
            entry_title='Заглавие на поста',
            content='Текст на поста',
            category=self.category,
        )

    def test_str_returns_entry_title(self):
        self.assertEqual(str(self.post), 'Заглавие на поста')

    def test_entry_title_defaults_to_na(self):
        post = Posts.objects.create(title='Кратко', content='Съдържание')
        self.assertEqual(post.entry_title, 'N/A')

    def test_deleting_category_keeps_the_post(self):
        self.category.delete()
        self.post.refresh_from_db()
        self.assertIsNone(self.post.category)

    def test_newest_posts_come_first(self):
        older = Posts.objects.create(title='Стар', entry_title='Стар пост', content='Стар')
        newer = Posts.objects.create(title='Нов', entry_title='Нов пост', content='Нов')
        older.created_at = timezone.now() - timedelta(days=2)
        older.save(update_fields=['created_at'])
        titles = list(
            Posts.objects.filter(entry_title__in=['Стар пост', 'Нов пост']).values_list('entry_title', flat=True)
        )
        self.assertEqual(titles, ['Нов пост', 'Стар пост'])


class CommentModelTests(TestCase):
    def setUp(self):
        self.post = Posts.objects.create(title='Пост', entry_title='Пост', content='Текст')

    def test_str_includes_author_and_post(self):
        comment = Comment.objects.create(post=self.post, author='Мария', body='Браво')
        self.assertEqual(str(comment), 'Мария on Пост')

    def test_comments_are_ordered_oldest_first(self):
        first = Comment.objects.create(post=self.post, author='Първи', body='Едно')
        second = Comment.objects.create(post=self.post, author='Втори', body='Две')
        first.created_at = timezone.now() - timedelta(hours=1)
        first.save(update_fields=['created_at'])
        authors = list(self.post.comments.values_list('author', flat=True))
        self.assertEqual(authors, ['Първи', 'Втори'])

    def test_deleting_post_deletes_its_comments(self):
        Comment.objects.create(post=self.post, author='Мария', body='Браво')
        post_id = self.post.pk
        self.post.delete()
        self.assertFalse(Comment.objects.filter(post_id=post_id).exists())


class CommentFormTests(TestCase):
    def test_accepts_name_and_comment_without_email(self):
        form = CommentForm(data={'author': 'Иван', 'email': '', 'body': 'Хубав текст'})
        self.assertTrue(form.is_valid())

    def test_rejects_missing_name(self):
        form = CommentForm(data={'author': '', 'email': '', 'body': 'Хубав текст'})
        self.assertFalse(form.is_valid())
        self.assertIn('author', form.errors)

    def test_rejects_missing_comment(self):
        form = CommentForm(data={'author': 'Иван', 'email': '', 'body': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)

    def test_rejects_invalid_email(self):
        form = CommentForm(data={'author': 'Иван', 'email': 'не-е-имейл', 'body': 'Текст'})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class PostViewTests(TestCase):
    def setUp(self):
        self.sport = Category.objects.create(name='Тест Спорт', slug='test-sport')
        self.news = Category.objects.create(name='Тест Свят', slug='test-svyat')
        self.sport_post = Posts.objects.create(
            title='Мач',
            entry_title='Уникален спортен пост',
            content='Спортен текст',
            category=self.sport,
        )
        self.news_post = Posts.objects.create(
            title='Новина',
            entry_title='Уникална световна новина',
            content='Новинарски текст',
            category=self.news,
        )
        Comment.objects.create(post=self.sport_post, author='Иван Димитров', body='Силен мач')

    def test_home_lists_posts_and_categories(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Уникален спортен пост')
        self.assertContains(response, 'Тест Спорт')
        self.assertContains(response, reverse('category', args=['test-sport']))

    def test_category_page_lists_only_its_posts(self):
        response = self.client.get(reverse('category', args=['test-sport']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Уникален спортен пост')
        self.assertNotContains(response, 'Уникална световна новина')
        self.assertEqual(response.context['category'], self.sport)
        self.assertEqual(response.context['section_title'], 'Тест Спорт')

    def test_unknown_category_returns_404(self):
        response = self.client.get(reverse('category', args=['nqma-takava']))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_shows_content_and_comments(self):
        response = self.client.get(reverse('post-detail', args=[self.sport_post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Уникален спортен пост')
        self.assertContains(response, 'Спортен текст')
        self.assertContains(response, 'Иван Димитров')
        self.assertContains(response, 'Силен мач')

    def test_unknown_post_returns_404(self):
        response = self.client.get(reverse('post-detail', args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_valid_comment_is_saved_and_shown(self):
        url = reverse('post-detail', args=[self.sport_post.pk])
        response = self.client.post(url, {
            'author': 'Ана Георгиева',
            'email': 'ana@example.com',
            'body': 'Добър матч',
        })
        self.assertRedirects(response, url)
        self.assertTrue(
            Comment.objects.filter(post=self.sport_post, author='Ана Георгиева', body='Добър матч').exists()
        )
        follow = self.client.get(url)
        self.assertContains(follow, 'Ана Георгиева')
        self.assertContains(follow, 'Добър матч')

    def test_invalid_comment_is_not_saved(self):
        url = reverse('post-detail', args=[self.sport_post.pk])
        before = Comment.objects.count()
        response = self.client.post(url, {'author': '', 'email': '', 'body': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), before)
        self.assertContains(response, 'Провери името и коментара.')

    def test_comment_is_not_attached_to_another_post(self):
        self.client.post(reverse('post-detail', args=[self.sport_post.pk]), {
            'author': 'Ана Георгиева',
            'email': '',
            'body': 'Само за спорта',
        })
        other = self.client.get(reverse('post-detail', args=[self.news_post.pk]))
        self.assertNotContains(other, 'Само за спорта')
