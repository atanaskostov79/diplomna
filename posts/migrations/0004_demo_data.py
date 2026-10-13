from django.db import migrations


DEMO_SLUGS = ['svyat', 'patuvania', 'sport', 'biznes', 'tehnologii']


def seed_demo(apps, schema_editor):
    Category = apps.get_model('posts', 'Category')
    Posts = apps.get_model('posts', 'Posts')
    Comment = apps.get_model('posts', 'Comment')

    categories = [
        ('Свят', 'svyat'),
        ('Пътувания', 'patuvania'),
        ('Спорт', 'sport'),
        ('Бизнес', 'biznes'),
        ('Технологии', 'tehnologii'),
    ]
    by_slug = {}
    for name, slug in categories:
        category, _created = Category.objects.get_or_create(slug=slug, defaults={'name': name})
        by_slug[slug] = category

    refreshed = {
        'Post 1': {
            'title': 'Репортаж',
            'entry_title': 'Нови правила за туристите в Гранд Каньон',
            'content': (
                'Парковата служба обсъжда по-строги квоти за нощувки в отдалечените пътеки. '
                'Идеята е да се ограничи ерозията и да остане място за по-малки групи.'
            ),
            'category': by_slug['svyat'],
        },
        'Post 2': {
            'title': 'Мач',
            'entry_title': 'Сезонът в Шампионска лига тръгва с пълни трибуни',
            'content': (
                'Първият кръг събра рекордна публика. Отборите залагат на висок пресинг, '
                'а феновете вече пълнят гостуващите сектори.'
            ),
            'category': by_slug['sport'],
        },
        'Post 3': {
            'title': 'Пазар',
            'entry_title': 'Mercedes показа новия AMG седан',
            'content': (
                'Новият модел залага на по-тих салон и по-бързо ускорение. '
                'Дилърите вече приемат предварителни заявки за пролетта.'
            ),
            'category': by_slug['biznes'],
        },
    }
    for title, data in refreshed.items():
        Posts.objects.filter(title=title).update(**data)

    demos = [
        (
            'patuvania',
            'Маршрут',
            'Нов план за пътеките в националните паркове',
            'Рейнджъри и доброволци ще обновят маркировката по дългите маршрути. '
            'Летният сезон обещава по-ясни карти и по-малко затворени участъци.',
        ),
        (
            'tehnologii',
            'Устройства',
            'Най-честите проблеми с Android и как се оправят',
            'Батерията пада след няколко големи обновления, а известията се дублират. '
            'Кратко рестартиране и проверка на фоновите приложения решават повечето случаи.',
        ),
        (
            'sport',
            'Анализ',
            'Флорида предлага мерки срещу мечките край игрищата',
            'Местните клубове слагат затворени контейнери и предупредителни табели. '
            'Целта е мачовете да не се местят заради животни в района.',
        ),
        (
            'tehnologii',
            'Редакции',
            'Как малките редакции използват изкуствен интелект',
            'Журналистите ползват инструментите за разчитане на записи и първи вариант на заглавия. '
            'Крайният текст минава през редактор, преди да бъде публикуван.',
        ),
    ]
    for slug, title, entry_title, content in demos:
        Posts.objects.get_or_create(
            entry_title=entry_title,
            defaults={
                'title': title,
                'content': content,
                'category': by_slug[slug],
            },
        )

    comment_sets = {
        'Нови правила за туристите в Гранд Каньон': [
            ('Мария Иванова', 'maria@example.com', 'Хубав текст. Квотите наистина са нужни, ако пътеките се тъпчат всеки уикенд.'),
            ('Георги Петров', 'georgi@example.com', 'Бих искал и карта на затворените участъци, не само общите правила.'),
        ],
        'Сезонът в Шампионска лига тръгва с пълни трибуни': [
            ('Иван Димитров', '', 'Атмосферата в първия кръг беше страхотна. Дано гостуващите фенове пак имат места.'),
            ('Никол Стоянова', 'nikol@example.com', 'Пресингът се вижда, но защитата още допуска лесни грешки.'),
        ],
        'Mercedes показа новия AMG седан': [
            ('Петър Колев', 'petar@example.com', 'Интересно ми е каква е реалната консумация, не само ускорението.'),
        ],
        'Нов план за пътеките в националните паркове': [
            ('Елена Василева', '', 'Маркировката миналото лято беше объркваща. Ако я оправят, ще тръгна пак по дългия маршрут.'),
        ],
        'Най-честите проблеми с Android и как се оправят': [
            ('Калин Тодоров', 'kalin@example.com', 'При мен дублираните известия спряха, след като махнах две стари приложения.'),
            ('Десислава Илиева', '', 'Полезно. Батерията ми пада най-много след нощни обновления.'),
        ],
    }
    for entry_title, comments in comment_sets.items():
        post = Posts.objects.filter(entry_title=entry_title).first()
        if post is None:
            continue
        for author, email, body in comments:
            Comment.objects.get_or_create(
                post=post,
                author=author,
                body=body,
                defaults={'email': email},
            )


def unseed_demo(apps, schema_editor):
    Category = apps.get_model('posts', 'Category')
    Category.objects.filter(slug__in=DEMO_SLUGS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_category_comment'),
    ]

    operations = [
        migrations.RunPython(seed_demo, unseed_demo),
    ]
