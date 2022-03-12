from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Описание команды'   # показывает подсказку при вводе "python manage.py <команда> --help"
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True  # напоминать ли о миграциях. Если тру — то будет напоминание о том,
                                       # что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # здесь пишутся аргументы для команды
        parser.add_argument('argument', nargs='+', type=int)

    def handle(self, *args, **options):
        # здесь можно писать любой код, который выполняется при вызове команды
        self.stdout.write(str(options['argument']))
