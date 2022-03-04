from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.utils import timezone
import pandas as pd
from io import BytesIO

from app_item.models import ItemOffer, ItemRequest


class Command(BaseCommand):
    help = "Dumps Models into Excel and sends email with xlsx as attachement"

    def add_arguments(self, parser):
        parser.add_argument(
            "emails",
            nargs="+",
            help="email addresses to send email to. space separated",
        )

    def handle(self, *args, **kwargs):

        email_addresses = kwargs["emails"]
        now = timezone.now()
        hours_ago_24 = now - timezone.timedelta(hours=24)

        item_offers = pd.DataFrame(
            ItemOffer.objects.filter(
                added_on__gte=hours_ago_24
            ).values(
                "county_coverage",
                "town",
                "description",
                "added_on",
                "status",
                "donor__username",
                "category__name",
                "name",
                "quantity",
                "packaging_type",
                "unit_type",
                "expiration_date",
                "stock",
                "textile_category__name",
                "kids_age",
                "other_textiles",
                "tent_capacity",
            )
        )
        item_offers.columns = [
            "Judete Acoperite",
            "Oras",
            "Descriere",
            "Adaugat in",
            "Stare",
            "Donator",
            "Categorie",
            "Nume",
            "Cantitate",
            "Ambalaj",
            "UM",
            "Data de Expirare",
            "Stoc",
            "Categorie Textile",
            "Varsta Copii",
            "Alte Textile",
            "Capacitate Cort",
        ]
        item_requests = pd.DataFrame(
            ItemRequest.objects.filter(
                added_on__gte=hours_ago_24
            ).values(
                "county_coverage",
                "town",
                "description",
                "added_on",
                "status",
                "made_by__username",
                "category__name",
                "name",
                "quantity",
                "packaging_type",
                "unit_type",
                "stock",
                "textile_category__name",
                "kids_age",
                "other_textiles",
                "tent_capacity",
            )
        )

        item_requests.columns = [
            "Judete Acoperite",
            "Oras",
            "Descriere",
            "Adaugat in",
            "Stare",
            "Oferit de",
            "Categorie",
            "Nume",
            "Cantitate",
            "Ambalaj",
            "UM",
            "Stoc",
            "Categorie Textile",
            "Varsta Copii",
            "Alte Textile",
            "Capacitate Cort",
        ]

        data = [
            (item_offers, "Donatii Produse"),
            (item_requests, "Cereri Produse"),
        ]

        bio = BytesIO()

        writer = pd.ExcelWriter(bio, engine="xlsxwriter")

        for df, sheet in data:
            df["Judete Acoperite"] = df["Judete Acoperite"].agg(
                lambda x: ", ".join(map(str, x))
            )
            df["Adaugat in"] = df["Adaugat in"].dt.tz_localize(None)

            df.to_excel(writer, sheet_name=sheet, index=False)

        writer.save()
        bio.seek(0)

        email = EmailMessage(
            subject="Raport zilnic situatie management resurse",
            from_email="no-reply@code4.ro",
            body=(
                "Situatia centralizata a datelor din sistemul integrat de management de "
                f"resurse si voluntari sprijindeurgenta.ro pentru intevalul {hours_ago_24.strftime('%c')} - {now.strftime('%c')}"
            ),
            to=email_addresses,
        )
        email.attach(
            "situatia_zilnica_sdu.xlsx",
            bio.getvalue(),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        email.send()
