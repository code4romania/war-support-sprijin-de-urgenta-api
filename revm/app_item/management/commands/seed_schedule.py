from django.core.management.base import BaseCommand
from django_q.models import Schedule
from django.utils import timezone


class Command(BaseCommand):
    help = "Seed Schedules for Django Q"

    def handle(self, *args, **kwargs):

        try:
            if not Schedule.objects.filter(name="Daily Status").exists():
                DAILY_AT_HOUR = 17
                DAILY_AT_MINUTE = 00
                next_run = timezone.localtime(timezone.now()).replace(
                    hour=DAILY_AT_HOUR, minute=DAILY_AT_MINUTE, second=0
                )
                if timezone.localtime(timezone.now()) > next_run:
                    next_run = timezone.localtime(timezone.now()).replace(
                        day=timezone.localtime(timezone.now()).day + 1,
                        hour=DAILY_AT_HOUR,
                        minute=DAILY_AT_MINUTE,
                        second=0,
                    )
                Schedule.objects.create(
                    id=1,
                    name="Daily Status",
                    func="django.core.management.call_command",
                    args="'gen_xl_dump','sprijindeurgenta@code4.ro'",
                    schedule_type=Schedule.DAILY,
                    next_run=next_run,
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error seeding schedules -> {e}"))

        self.stdout.write(self.style.SUCCESS("Seeded Schedules successfully"))
