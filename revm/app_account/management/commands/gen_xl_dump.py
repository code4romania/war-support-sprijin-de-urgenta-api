import os
from io import BytesIO

import numpy as np
import pandas as pd
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.utils import timezone

from app_item.models import ItemOffer, ItemRequest
from app_other.models import OtherOffer, OtherRequest
from app_transport_service.models import TransportServiceOffer, TransportServiceRequest
from app_volunteering.models import VolunteeringOffer, VolunteeringRequest


class Command(BaseCommand):
    help = "Dumps Models into Excel and sends email with xlsx as attachment"

    def __init__(self):
        super().__init__()
        self.now = timezone.localtime()
        self.hours_ago_24 = self.now - timezone.timedelta(hours=24)

    def add_arguments(self, parser):
        parser.add_argument(
            "emails",
            nargs="+",
            help="email addresses to send email to. separate multiple emails with spaces",
        )
        parser.add_argument(
            "--save-to-file",
            default="n",
            choices=["y", "n"],
            help="save the generated excel file to the current directory",
        )
        parser.add_argument(
            "--send-email",
            default="y",
            choices=["y", "n"],
            help="send the generated excel file as email attachment",
        )

    def handle(self, *args, **kwargs):
        email_addresses = kwargs["emails"]
        save_to_file = kwargs["save_to_file"] == "y"
        send_email = kwargs["send_email"] == "y"

        data = self._extract_database_data()

        bio = BytesIO()

        writer = pd.ExcelWriter(bio, engine="xlsxwriter")

        for df, sheet in data:
            if df.size > 0:
                self._prettify_data(df)

            df.to_excel(writer, sheet_name=sheet, index=False)

        writer.save()

        if save_to_file or settings.ENABLE_DUMP_LOCAL_SAVE:
            bio.seek(0)
            folder_path = os.path.join(settings.BASE_DIR, "dump_data")
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            file_path = os.path.join(folder_path, f"data-dump-{self.now.strftime('%Y-%m-%d')}.xlsx")
            with open(file_path, "wb") as f:
                f.write(bio.read())

        if send_email:
            bio.seek(0)
            attachment = [
                "situatia_zilnica_sdu.xlsx",
                bio.read(),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ]
            body = (
                "Situatia centralizata a datelor din sistemul integrat de management de "
                "resurse si voluntari sprijindeurgenta.ro pentru intevalul "
                f"{self.hours_ago_24.strftime('%c')} - {self.now.strftime('%c')}"
            )
            email = EmailMessage(
                subject="Raport zilnic situatie management resurse",
                from_email=settings.FROM_EMAIL,
                to=email_addresses,
                body=body,
                attachments=[attachment],
            )
            email.send()

    def _extract_database_data(self):
        item_offer_data_mapping = {
            self._field_name(ItemOffer.county_coverage): "Judete Acoperite",
            self._field_name(ItemOffer.town): "Oras",
            self._field_name(ItemOffer.description): "Descriere",
            self._field_name(ItemOffer.added_on): "Adaugat in",
            self._field_name(ItemOffer.status): "Stare",
            self._field_property_name(ItemOffer.donor, "username"): "Donator",
            self._field_property_name(ItemOffer.category, "name"): "Categorie",
            self._field_name(ItemOffer.name): "Nume",
            self._field_name(ItemOffer.quantity): "Cantitate",
            self._field_name(ItemOffer.packaging_type): "Ambalaj",
            self._field_name(ItemOffer.unit_type): "UM",
            self._field_name(ItemOffer.expiration_date): "Data de Expirare",
            self._field_name(ItemOffer.stock): "Stoc",
            self._field_property_name(ItemOffer.textile_category, "name"): "Categorie Textile",
            self._field_name(ItemOffer.kids_age): "Varsta Copii",
            self._field_name(ItemOffer.other_textiles): "Alte Textile",
            self._field_name(ItemOffer.tent_capacity): "Capacitate Cort",
        }
        item_request_data_mapping = {
            self._field_name(ItemRequest.county_coverage): "Judete Acoperite",
            self._field_name(ItemRequest.town): "Oras",
            self._field_name(ItemRequest.description): "Descriere",
            self._field_name(ItemRequest.added_on): "Adaugat in",
            self._field_name(ItemRequest.status): "Stare",
            self._field_property_name(ItemRequest.made_by, "username"): "Oferit de",
            self._field_property_name(ItemRequest.category, "name"): "Categorie",
            self._field_name(ItemRequest.name): "Nume",
            self._field_name(ItemRequest.quantity): "Cantitate",
            self._field_name(ItemRequest.packaging_type): "Ambalaj",
            self._field_name(ItemRequest.unit_type): "UM",
            self._field_name(ItemRequest.stock): "Stoc",
            self._field_property_name(ItemRequest.textile_category, "name"): "Categorie Textile",
            self._field_name(ItemRequest.kids_age): "Varsta Copii",
            self._field_name(ItemRequest.other_textiles): "Alte Textile",
            self._field_name(ItemRequest.tent_capacity): "Capacitate Cort",
        }
        other_offer_data_mapping = {
            self._field_name(OtherOffer.available_until): "Disponibil pana la",
            self._field_name(OtherOffer.name): "Nume",
            self._field_property_name(OtherOffer.category, "name"): "Categorie",
            self._field_property_name(OtherOffer.donor, "username"): "Donator",
            self._field_name(OtherOffer.added_on): "Adaugat in",
            self._field_name(OtherOffer.description): "Descriere",
            self._field_name(OtherOffer.status): "Stare",
            self._field_name(OtherOffer.town): "Oras",
            self._field_name(OtherOffer.county_coverage): "Judete Acoperite",
            self._field_name(OtherOffer.has_transportation): "Poate asigura transport",
        }
        other_request_data_mapping = {
            self._field_name(OtherRequest.name): "Nume",
            self._field_property_name(OtherRequest.category, "name"): "Categorie",
            self._field_property_name(OtherRequest.made_by, "username"): "Oferit de",
            self._field_name(OtherRequest.added_on): "Adaugat in",
            self._field_name(OtherRequest.description): "Descriere",
            self._field_name(OtherRequest.status): "Stare",
            self._field_name(OtherRequest.town): "Oras",
            self._field_name(OtherRequest.county_coverage): "Judete Acoperite",
        }
        transport_offer_data_mapping = {
            self._field_name(TransportServiceOffer.availability): "Disponibilitate",
            self._field_name(TransportServiceOffer.availability_interval_from): "Interval disponibilitate de la",
            self._field_name(TransportServiceOffer.availability_interval_to): "Interval disponibilitate pana la",
            self._field_name(TransportServiceOffer.available_seats): "Locuri disponibile",
            self._field_name(TransportServiceOffer.car_registration_number): "Numar de inmatriculare",
            self._field_property_name(TransportServiceOffer.category, "name"): "Categorie",
            self._field_name(TransportServiceOffer.driver_contact): "Contact sofer",
            self._field_name(TransportServiceOffer.driver_id): "Act de identitate sofer",
            self._field_name(TransportServiceOffer.driver_name): "Nume",
            self._field_name(TransportServiceOffer.has_disabled_access): "Acces persoane cu dizabilități",
            self._field_name(TransportServiceOffer.has_refrigeration): "Are refrigerare",
            self._field_name(TransportServiceOffer.pets_allowed): "Animale de companie permise",
            self._field_name(TransportServiceOffer.weight_capacity): "Limită de greutate",
            self._field_name(TransportServiceOffer.weight_unit): "Unitate de măsură",
            self._field_name(TransportServiceOffer.type): "Tip de transport",
            self._field_name(TransportServiceOffer.county_coverage): "Judete Acoperite",
            self._field_property_name(TransportServiceOffer.donor, "username"): "Donator",
            self._field_name(TransportServiceOffer.added_on): "Adaugat in",
            self._field_name(TransportServiceOffer.description): "Descriere",
            self._field_name(TransportServiceOffer.status): "Stare",
        }
        transport_request_data_mapping = {
            self._field_name(TransportServiceRequest.available_seats): "Locuri disponibile",
            self._field_property_name(TransportServiceRequest.category, "name"): "Categorie",
            self._field_name(TransportServiceRequest.from_city): "Oraș plecare",
            self._field_name(TransportServiceRequest.from_county): "Județ plecare",
            self._field_name(TransportServiceRequest.has_disabled_access): "Acces persoane cu dizabilități",
            self._field_name(TransportServiceRequest.has_refrigeration): "Are refrigerare",
            self._field_name(TransportServiceRequest.pets_allowed): "Animale de companie permise",
            self._field_name(TransportServiceRequest.to_city): "Oraș de destinație",
            self._field_name(TransportServiceRequest.to_county): "Județ de destinație",
            self._field_name(TransportServiceRequest.weight_capacity): "Limită de greutate",
            self._field_name(TransportServiceRequest.weight_unit): "Unitate de măsură",
            self._field_property_name(TransportServiceRequest.made_by, "username"): "Oferit de",
            self._field_name(TransportServiceRequest.added_on): "Adaugat in",
            self._field_name(TransportServiceRequest.description): "Descriere",
            self._field_name(TransportServiceRequest.status): "Stare",
        }
        volunteering_offer_data_mapping = {
            self._field_name(VolunteeringOffer.available_until): "Disponibil pana la",
            self._field_property_name(VolunteeringOffer.type, "name"): "Categorie",
            self._field_property_name(VolunteeringOffer.donor, "username"): "Donator",
            self._field_name(VolunteeringOffer.added_on): "Adaugat in",
            self._field_name(VolunteeringOffer.description): "Descriere",
            self._field_name(VolunteeringOffer.status): "Stare",
            self._field_name(VolunteeringOffer.town): "Oras",
            self._field_name(VolunteeringOffer.county_coverage): "Judete Acoperite",
            self._field_name(VolunteeringOffer.has_transportation): "Poate asigura transport",
        }
        volunteering_request_data_mapping = {
            self._field_property_name(VolunteeringRequest.type, "name"): "Categorie",
            self._field_property_name(VolunteeringRequest.made_by, "username"): "Oferit de",
            self._field_name(VolunteeringRequest.added_on): "Adaugat in",
            self._field_name(VolunteeringRequest.description): "Descriere",
            self._field_name(VolunteeringRequest.status): "Stare",
            self._field_name(VolunteeringRequest.town): "Oras",
            self._field_name(VolunteeringRequest.county_coverage): "Judete Acoperite",
        }
        item_offers = self._get_dataframe_with_objects(ItemOffer, item_offer_data_mapping)
        item_requests = self._get_dataframe_with_objects(ItemRequest, item_request_data_mapping)
        other_offer = self._get_dataframe_with_objects(OtherOffer, other_offer_data_mapping)
        other_request = self._get_dataframe_with_objects(OtherRequest, other_request_data_mapping)
        transport_offer = self._get_dataframe_with_objects(TransportServiceOffer, transport_offer_data_mapping)
        transport_request = self._get_dataframe_with_objects(TransportServiceRequest, transport_request_data_mapping)
        volunteering_offer = self._get_dataframe_with_objects(VolunteeringOffer, volunteering_offer_data_mapping)
        volunteering_request = self._get_dataframe_with_objects(VolunteeringRequest, volunteering_request_data_mapping)
        data = [
            (item_offers, "Donatii Produse"),
            (item_requests, "Cereri Produse"),
            (other_offer, "Donatii Altele"),
            (other_request, "Cereri Altele"),
            (transport_offer, "Donatii Transport"),
            (transport_request, "Cereri Transport"),
            (volunteering_offer, "Donatii Voluntariat"),
            (volunteering_request, "Cereri Voluntariat"),
        ]
        return data

    def _get_dataframe_with_objects(self, object_model, data_mapping):
        item_data = object_model.objects.filter(added_on__gte=self.hours_ago_24).values(*data_mapping.keys())
        item_data = item_data if len(item_data) > 0 else np.empty((0, len(data_mapping.keys())))
        items = pd.DataFrame(item_data)
        items.columns = list(data_mapping.values())
        return items

    @staticmethod
    def _prettify_data(df):
        if "Judete Acoperite" in df:
            df["Judete Acoperite"] = df["Judete Acoperite"].agg(lambda x: ", ".join(map(str, x)))
        if "Adaugat in" in df:
            df["Adaugat in"] = df["Adaugat in"].dt.tz_localize(None).dt.strftime("%d-%m-%Y %H:%M")

    @staticmethod
    def _field_name(model_field):
        return model_field.field.attname

    @staticmethod
    def _field_property_name(model_field, field_property):
        field_obj = model_field.field
        property_name = getattr(field_obj.related_model, field_property).field.attname
        return f"{field_obj.attname}__{property_name}"
