# Copyright (C)
# date: 16-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""My Input Image Form."""

from django import forms

from FoodCaloEstimate.estimator.models.my_input_image import MyInputImage
from FoodCaloEstimate.estimator.services.food_dictionany_service import FoodDictionary

class MyInputImageForm(forms.ModelForm):
    """My Input Image Form."""

    label = forms.ChoiceField(
        choices=[
            (str(id), name["name_accent"]) for id, name in FoodDictionary.id_to_food.items()
        ],
        label="Label",
    )

    class Meta:
        """Meta class."""
        model = MyInputImage
        fields = "__all__"
