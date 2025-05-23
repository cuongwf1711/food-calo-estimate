# Copyright (C)
# date: 16-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Chart Admin Model."""

from django.contrib.admin import ModelAdmin
from django.db.models import Count, F, Q, Sum
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.urls import path

from FoodCaloEstimate.estimator.models.my_input_image import MyInputImage
from FoodCaloEstimate.estimator.services.food_dictionany_service import FoodDictionary


# use: add method, add method to extra_urls, change file change_list.html
class ChartAdminModel(ModelAdmin):
    """Chart Admin Model."""

    all_labels = {
        id: name["name_accent"] for id, name in FoodDictionary.id_to_food.items()
    }
    model = MyInputImage
    MAX_X = 30

    def get_urls(self):
        extra_urls = [
            path(f"chart_data_{key}", self.admin_site.admin_view(func))
            for key, func in {
                "date": self.chart_data_date_endpoint,
                "label_type": self.chart_data_label_type_endpoint,
                "predict_type": self.chart_data_predict_type_endpoint,
                "user": self.chart_data_user_endpoint,
                "staff": self.chart_data_staff_endpoint,
                "calories": self.chart_data_calories_endpoint,
                "percentage": self.chart_data_percentage_endpoint,
            }.items()
        ]
        return extra_urls + super().get_urls()

    # Chart data endpoints
    def get_data_from_date(self, annotate_y):
        """Get data from date."""
        data = (
            self.model.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=annotate_y)
            .order_by("-date")[: self.MAX_X]
        )
        return JsonResponse(list(data), safe=False)

    def chart_data_date_endpoint(self, request):
        """Chart data grouped by date."""
        return self.get_data_from_date(Count("id"))

    def chart_data_calories_endpoint(self, request):
        """Sum calories per day."""
        return self.get_data_from_date(Sum("calo"))

    def get_data_all_labels(self, field):
        """Get data for all labels."""
        raw_data = self.model.objects.values(field).annotate(y=Count("id"))
        raw_data_dict = {item[field]: item["y"] for item in raw_data}
        data = [
            {"x": self.all_labels.get(key, key), "y": raw_data_dict.get(key, 0)}
            for key in self.all_labels
        ]
        return JsonResponse(data, safe=False)

    def chart_data_label_type_endpoint(self, request):
        """Chart data grouped by label."""
        return self.get_data_all_labels("label")

    def chart_data_predict_type_endpoint(self, request):
        """Chart data grouped by predict."""
        return self.get_data_all_labels("predict")

    def get_data_from_user(self, field):
        """Get data for all labels."""
        data = (
            self.model.objects.values(field)
            .annotate(y=Count("id"))
            .order_by("-y")[: self.MAX_X]
        )
        return JsonResponse(
            [{"x": item[field], "y": item["y"]} for item in data],
            safe=False,
        )

    def chart_data_user_endpoint(self, request):
        """Chart data grouped by user."""
        return self.get_data_from_user("user__username")

    def chart_data_staff_endpoint(self, request):
        """Chart data grouped by staff."""
        return self.get_data_from_user("staff__username")

    def chart_data_percentage_endpoint(self, request):
        """Chart data percentage."""
        stats = self.model.objects.aggregate(
            unprocessed_count=Count("id", filter=Q(staff__isnull=True)),
            processed_count=Count("id", filter=Q(staff__isnull=False)),
            correct_predictions=Count(
                "id", filter=Q(staff__isnull=False) & Q(label=F("predict"))
            ),
            deleted_count=Count("id", filter=Q(is_deleted=True)),
            not_deleted_count=Count("id", filter=Q(is_deleted=False)),
        )

        unprocessed = stats["unprocessed_count"] or 0
        processed = stats["processed_count"] or 0
        correct = stats["correct_predictions"] or 0
        deleted = stats["deleted_count"] or 0
        not_deleted = stats["not_deleted_count"] or 0

        accuracy_percentage = (correct / processed * 100) if processed else 0.0
        processed_ratio_pct = (processed / unprocessed * 100) if unprocessed else 0.0
        deleted_percentage = (
            (deleted / (deleted + not_deleted) * 100)
            if (deleted + not_deleted)
            else 0.0
        )
        not_deleted_percentage = (
            (not_deleted / (deleted + not_deleted) * 100)
            if (deleted + not_deleted)
            else 0.0
        )

        response_data = [
            {"x": "Accuracy", "y": float(f"{accuracy_percentage:.2f}")},
            {"x": "Processed/Unprocessed", "y": float(f"{processed_ratio_pct:.2f}")},
            {"x": "Deleted", "y": float(f"{deleted_percentage:.2f}")},
            {"x": "Not Deleted", "y": float(f"{not_deleted_percentage:.2f}")},
        ]
        return JsonResponse(response_data, safe=False)
