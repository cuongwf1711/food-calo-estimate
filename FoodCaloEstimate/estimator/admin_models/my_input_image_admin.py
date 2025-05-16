# Copyright (C)
# date: 15-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""My Input Image Admin."""

from django.utils.html import format_html

from FoodCaloEstimate.estimator.admin_models.confidence_range_filter import ConfidenceRangeFilter
from FoodCaloEstimate.estimator.admin_models.int_choices_filter import make_int_choice_filter
from FoodCaloEstimate.estimator.admin_models.my_input_image_form import MyInputImageForm
from FoodCaloEstimate.estimator.constants.image_constants import LOCAL_IMAGE_URL, ORIGIN_IMAGE, SEGMENTATION_IMAGE
from FoodCaloEstimate.estimator.services.food_dictionany_service import FoodDictionary
from FoodCaloEstimate.estimator.services.image_service import ImageService
from FoodCaloEstimate.queue_tasks import run_task_in_queue
from FoodCaloEstimate.estimator.admin_models.chart_admin_model import ChartAdminModel

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
        url = obj.url.get(image_type, {}).get(LOCAL_IMAGE_URL, "")
        return format_html(
            '<img src="{}" style="width:100%; height:auto; object-fit:contain;"/>',
            url
        )

    def origin_and_segmentation_images(self, obj):
        """Render origin and segmentation images."""
        return format_html(
            '<div style="display:flex; gap:1rem; flex-wrap:wrap;">'
            '  <div style="flex:1 1 45%;">{}</div>'
            '  <div style="flex:1 1 45%;">{}</div>'
            '</div>',
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
        "comment",
        "calo",
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
    ]
    list_filter = (
        make_int_choice_filter("label",   "Label"),
        make_int_choice_filter("predict", "Prediction"),
        ConfidenceRangeFilter,
        "created_at",
        "updated_at",
    )
    exclude = (
        "url",
        "confidence",
        "predict",
    )

    def save_model(self, request, obj, form, change):
        """Save model."""
        run_task_in_queue(
            ImageService.move_image_and_update_instance,
            obj
        )
        obj.staff = request.user
        obj.save(update_fields=["label", "updated_at", "staff"])

    def delete_model(self, request, obj):
        """Delete model."""
        run_task_in_queue(ImageService().delete_image, obj.url)
        return super().delete_model(request, obj)

    def has_add_permission(self, request):
        """Check if user has permission to add."""
        return False
