from django.core.management.base import BaseCommand
from accounts.models import Post


class Command(BaseCommand):
    help = 'Эта функция удаляет все новости из определённой категории'
    missing_args_message = 'Нужно ввести категорию, из которой удаляем новости'

    def add_arguments(self, parser):
        parser.add_argument('argument', nargs='+', type=int)

    def handle(self, *args, **options):
        self.stdout.write(f'Вы подтверждаете удаление всех новостей из категории {options["argument"]}? y/n')
        answer = input()

        if answer != 'y':
            self.stdout.write(self.style.ERROR('Отменено'))
        else:
            try:
                Post.objects.filter(post_category=options['argument'][0]).delete()
                self.stdout.write(self.style.SUCCESS('Новости успешно удалены!'))
            except Post.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category'))
