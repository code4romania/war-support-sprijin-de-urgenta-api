# from captcha.fields import ReCaptchaField
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Fieldset, Layout, Submit
from django import forms
from django.utils.translation import gettext_lazy as _

from app_food_request.models import FoodRequest


class FoodRequestForm(forms.ModelForm):
    # captcha = ReCaptchaField(
    #     label="",
    # )
    terms_and_conditions = forms.BooleanField(
        label=_(
            '<div class="toc">I have read and agree to the '
            '<a class="toc" href="/en/terms-and-conditions/">Terms and Conditions</a>'
            "</div>"
        ),
        required=True,
    )

    class Meta:
        model = FoodRequest
        fields = [
            "ngo_name",
            "county_coverage",
            "town",
            "address",
            "contact_person",
            "phone_number",
            "email",
            "backup_phone_number",
            "offered_services",
            "other_offered_services",
            "adult_vegetarian_portions",
            "child_vegetarian_portions",
            "adult_meat_portions",
            "child_meat_portions",
            "adult_restricted_portions",
            "adult_restriction_notes",
            "child_restricted_portions",
            "child_restriction_notes",
            "delivery_hours",
            "delivery_daily_frequency",
            "preferred_packaging",
            "notes",
            "terms_and_conditions",
        ]

        labels = {
            "adult_restriction_notes": _("Adult restriction notes (please fill in)"),
            "child_restriction_notes": _("Child restriction notes (please fill in)"),
            "notes": _("Notes (please fill in)"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                _("NGO Details"),
                "ngo_name",
                "county_coverage",
                "town",
                "address",
                "contact_person",
                "phone_number",
                "email",
                "backup_phone_number",
                "offered_services",
                "other_offered_services",
                css_class="fieldset",
            ),
            Fieldset(
                _("Food details"),
                Fieldset(
                    _("Vegetarian"),
                    "adult_vegetarian_portions",
                    "child_vegetarian_portions",
                    css_class="subfieldset",
                ),
                Fieldset(
                    _("Meat"),
                    "adult_meat_portions",
                    "child_meat_portions",
                    css_class="subfieldset",
                ),
                Fieldset(
                    _("Dietary restrictions"),
                    "adult_restriction_notes",
                    "adult_restricted_portions",
                    "child_restriction_notes",
                    "child_restricted_portions",
                    css_class="subfieldset",
                ),
                css_class="fieldset",
            ),
            Fieldset(
                _("Delivery details"),
                "delivery_hours",
                "delivery_daily_frequency",
                "preferred_packaging",
                "notes",
                css_class="fieldset",
            ),
            HTML('<hr class="pre-toc">'),
            Div(
                Div("terms_and_conditions", css_class="toc-input"),
                FormActions(
                    Submit("submit", f"{_('Send request')} &vrtri;", css_class="btn btn-primary btn-lg float-right "),
                ),
                css_class="final-input",
            ),
        )

        # # TODO: Add captcha support
        # if not settings.RECAPTCHA_PUBLIC_KEY:
        #     del self.fields["captcha"]
