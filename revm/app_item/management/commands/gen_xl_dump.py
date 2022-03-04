from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
import pandas as pd
from io import BytesIO

from app_item.models import ItemOffer, ItemRequest


class Command(BaseCommand):
    help = "Dumps Models into Excel and sends email with xlsx as attachement"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email_addresses",
            nargs="*",
            help="email addresses to send email to. space separated",
        )

    def handle(self, *args, **kwargs):

        email_addresses = kwargs["email_addresses"]

        item_offers = pd.DataFrame(ItemOffer.objects.values())
        item_requests = pd.DataFrame(ItemRequest.objects.values())

        return print(item_offers)

        data = [
            (item_offers, "Donatii Produse"),
            (item_requests, "Cereri Produse"),
        ]

        bio = BytesIO()

        writer = pd.ExcelWriter(bio, engine="xlsxwriter")

        for df, sheet in data:
            df.to_excel(writer, sheet_name=sheet, index=False)

        writer.save()
        bio.seek(0)

        email = EmailMessage(
            subject="Raport zilnic situatie management resurse",
            body=(
                "Situatia centralizata a datelor din sistemul integrat de management de "
                "resurse si voluntari sprijindeurgenta.ro pentru intevalul [date][hour] - [date][hour]"
            ),
            to=[email_addresses],
        )
        email.attach(
            "situatia_zilnica_sdu.xlsx",
            bio.getvalue(),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        email.send()
