from django.conf import settings
from django.contrib import admin, messages
from django.db.models import TextField
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from revm_site.utils.models import CommonRequestModel, CommonOfferModel


class CommonPaginatedAdmin(admin.ModelAdmin):
    list_per_page = 20


class CommonResourceInline(admin.TabularInline):
    extra = 1
    show_change_link = True
    view_on_site = True

    formfield_overrides = {TextField: {"widget": Textarea(attrs={"rows": 2, "cols": 20})}}

    def has_delete_permission(self, request, obj=None):
        if request.user.is_cjcci_user() or request.user.is_cncci_user():
            return False
        return super().has_delete_permission(request, obj)


class CommonOfferInline(CommonResourceInline):
    verbose_name_plural = _("Allocate this resource to a request")

    def get_formset(self, request, obj=None, **kwargs):
        self.offer_obj = obj
        formset = super().get_formset(request, obj, **kwargs)
        return formset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "request":
            RequestModel = self.model._meta.get_field('request').related_model
            if self.offer_obj:
                kwargs["queryset"] = RequestModel.objects.filter(status='V', category=self.offer_obj.category)
            else:
                kwargs["queryset"] = RequestModel.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CommonRequestInline(CommonResourceInline):
    verbose_name_plural = _("Allocate from the available offers")

    def get_formset(self, request, obj=None, **kwargs):
        self.request_obj = obj
        formset = super().get_formset(request, obj, **kwargs)
        return formset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "resource":
            OfferModel = self.model._meta.get_field('resource').related_model
            if self.request_obj:
                try:
                    kwargs["queryset"] = OfferModel.objects.filter(status='V', category=self.request_obj.category)
                except:
                    kwargs["queryset"] = OfferModel.objects.filter(status='V', type=self.request_obj.type)
            else:
                kwargs["queryset"] = OfferModel.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CommonResourceAdmin(ImportExportModelAdmin):
    def get_filtered_by_county_queryset(self, queryset, county):
        raise NotImplementedError

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()

        if request.user.is_cjcci_user():
            if request.user.county is None:
                message_str = _("You are not assigned to any county. Please contact your administrator.")
                self.message_user(request, message_str, messages.ERROR)
                return queryset.none()

            return self.get_filtered_by_county_queryset(queryset, request.user.county)

        if request.user.is_superuser or request.user.is_cncci_user():
            return queryset

        if request.user.is_regular_user():
            if isinstance(self.model, CommonOfferModel):
                return queryset.filter(donor=request.user)
            if isinstance(self.model, CommonRequestModel):
                return queryset.filter(made_by=request.user)

        return queryset

    class Meta:
        abstract = True


class CommonResourceSingleCountyAdmin(CommonResourceAdmin):
    def get_filtered_by_county_queryset(self, queryset, county):
        return queryset.filter(county_coverage=county)

    class Meta:
        abstract = True


class CommonResourceMultipleCountyAdmin(CommonResourceAdmin):
    def get_filtered_by_county_queryset(self, queryset, county):
        return queryset.filter(county_coverage__contains=county)

    class Meta:
        abstract = True


class CommonResourceToFromCountyAdmin(CommonResourceAdmin):
    def get_filtered_by_county_queryset(self, queryset, county):
        return queryset.filter(from_county=county)

    class Meta:
        abstract = True


class CountyFilter(admin.SimpleListFilter):
    title = _("County")

    parameter_name = "county"

    def lookups(self, request, model_admin):
        return settings.COUNTY_CHOICES

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            return queryset.filter(
                county_coverage__contains=self.value(),
            )
        return queryset
