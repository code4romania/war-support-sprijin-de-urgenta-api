from django.conf import settings
from django.contrib import admin, messages
from django.db.models import TextField, Q
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from revm_site.utils.models import CommonRequestModel, CommonOfferModel


class CommonPaginatedAdmin(admin.ModelAdmin):
    list_per_page = 20


class CommonResourceInline(admin.StackedInline):
    extra = 1
    show_change_link = True
    view_on_site = True

    formfield_overrides = {TextField: {"widget": Textarea(attrs={"rows": 2, "cols": 20})}}

    def __init__(self, parent_model, admin_site):
        super().__init__(parent_model, admin_site)
        self.resource_obj = None
        self.related_resource_name = None

    def _get_formfield_queryset(self, related_model):
        if self.related_resource_name == "request":
            is_allocated_here = Q(resourcerequest__resource=self.resource_obj)
        else:
            is_allocated_here = Q(resourcerequest__request=self.resource_obj)
        try:
            return related_model.objects.filter(
                is_allocated_here | Q(status=settings.ITEM_STATUS_VERIFIED, category=self.resource_obj.category)
            ).distinct("pk")
        except AttributeError:
            return related_model.objects.filter(
                is_allocated_here | Q(status=settings.ITEM_STATUS_VERIFIED, type=self.resource_obj.type)
            ).distinct("pk")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == self.related_resource_name:
            related_model = self.model._meta.get_field(self.related_resource_name).related_model
            if self.resource_obj:
                kwargs["queryset"] = self._get_formfield_queryset(related_model)
            else:
                kwargs["queryset"] = related_model.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_cjcci_user() or request.user.is_cncci_user():
            return False
        return super().has_delete_permission(request, obj)


class CommonOfferInline(CommonResourceInline):
    verbose_name_plural = _("Allocate this resource to a request")

    def __init__(self, parent_model, admin_site):
        super().__init__(parent_model, admin_site)
        self.related_resource_name = "request"
        self.is_allocated_q = Q(resourcerequest__resource=self.resource_obj)

    def get_formset(self, request, obj=None, **kwargs):
        self.resource_obj = obj
        formset = super().get_formset(request, obj, **kwargs)
        return formset


class CommonReadonlyOfferInline(CommonOfferInline):
    readonly_fields = ("request", "total_units", "description")


class CommonRequestInline(CommonResourceInline):
    verbose_name_plural = _("Allocate from the available offers")

    def __init__(self, parent_model, admin_site):
        super().__init__(parent_model, admin_site)
        self.related_resource_name = "resource"
        self.is_allocated_q = Q(resourcerequest__request=self.resource_obj)

    def get_formset(self, request, obj=None, **kwargs):
        self.resource_obj = obj
        formset = super().get_formset(request, obj, **kwargs)
        return formset


class CommonReadonlyRequestInline(CommonRequestInline):
    readonly_fields = ("resource", "total_units", "description")


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
