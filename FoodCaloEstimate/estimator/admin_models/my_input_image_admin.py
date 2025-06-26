# Copyright (C)
# date: 15-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""My Input Image Admin."""

from django.contrib.admin import EmptyFieldListFilter
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

from FoodCaloEstimate.estimator.admin_models.chart_admin_model import ChartAdminModel
from FoodCaloEstimate.estimator.admin_models.confidence_range_filter import (
    ConfidenceRangeFilter,
)
from FoodCaloEstimate.estimator.admin_models.int_choices_filter import (
    make_int_choice_filter,
)
from FoodCaloEstimate.estimator.admin_models.my_input_image_form import MyInputImageForm
from FoodCaloEstimate.estimator.constants.image_constants import (
    DEFAULT_URL,
    ORIGIN_IMAGE,
    SEGMENTATION_IMAGE,
)
from FoodCaloEstimate.estimator.services.food_dictionany_service import FoodDictionary
from FoodCaloEstimate.estimator.services.image_service import ImageService
from FoodCaloEstimate.queue_tasks import run_task_in_queue


class MyInputImageAdmin(ChartAdminModel):
    """My Input Image Admin."""

    form = MyInputImageForm

    def label_name(self, obj):
        """Get label name."""
        return FoodDictionary.get_name(obj.label)

    def predict_name(self, obj):
        """Get predict name."""
        return FoodDictionary.get_name(obj.predict)

    def render_image(self, obj, image_type):
        """Render image."""
        url = obj.url.get(image_type, {}).get(DEFAULT_URL, "")
        return format_html(
            '<img src="{}" style="width:100%; height:auto; object-fit:contain;"/>', url
        )

    def origin_and_segmentation_images(self, obj):
        """Render origin and segmentation images."""
        return format_html(
            '<div style="display:flex; gap:1rem; flex-wrap:wrap;">'
            '  <div style="flex:1 1 45%;">{}</div>'
            '  <div style="flex:1 1 45%;">{}</div>'
            "</div>",
            self.render_image(obj, ORIGIN_IMAGE),
            self.render_image(obj, SEGMENTATION_IMAGE),
        )

    # Admin configurations
    list_display = (
        "user",
        "label_name",
        "predict_name",
        "confidence_percentage",
        "created_at",
        "updated_at",
        "staff",
        # "comment",
        "calo",
        "is_deleted",
    )
    search_fields = ("user__username", "staff__username")
    readonly_fields = [
        "user",
        "confidence_percentage",
        "created_at",
        "updated_at",
        "comment",
        "staff",
        "calo",
        "predict_name",
        "origin_and_segmentation_images",
        "is_deleted",
    ]
    list_filter = (
        make_int_choice_filter("label", "Label"),
        make_int_choice_filter("predict", "Prediction"),
        ConfidenceRangeFilter,
        ("staff", EmptyFieldListFilter),
        "created_at",
        "updated_at",
        "is_deleted",
    )
    exclude = (
        "url",
        "confidence",
        "predict",
        "deleted_at",
    )

    def save_model(self, request, obj, form, change):
        """Save model."""
        run_task_in_queue(ImageService.move_image_and_update_instance, obj)
        obj.staff = request.user
        obj.save(update_fields=["label", "updated_at", "staff"])

    def delete_model(self, request, obj):
        """Delete model."""
        run_task_in_queue(ImageService.delete_image, obj.url)
        return super().delete_model(request, obj)

    def has_add_permission(self, request):
        """Check if user has permission to add."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Check if user has permission to delete."""
        if obj and not obj.is_deleted:
            return False
        return super().has_delete_permission(request, obj)

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet) -> None:
        """Delete queryset."""
        [run_task_in_queue(ImageService.delete_image, obj.url) for obj in queryset]
        return super().delete_queryset(request, queryset)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Get queryset."""
        return super().get_queryset(request).select_related("staff", "user")
