# Copyright (C)
# date: 13-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Food Dictionary."""

import re
import unicodedata

from FoodCaloEstimate.estimator.constants.image_constants import (
    UNKNOWN,
    UNKNOWN_CALO,
    UNKNOWN_INDEX,
)


class FoodDictionaryService:
    """Food Dictionary Class."""

    def __init__(self):
        """Init."""
        # FIXME: Adjust food data if needed
        self.__foods = (
            ("bánh cuốn", 2.0),
            ("mì quảng", 3.0),
            ("bánh tráng nướng", 2.5),
            ("bánh trung thu", 5.0),
            ("bánh tai heo", 2.0),
            ("gỏi cuốn", 2.0),
            ("bánh giò", 2.0),
            ("bún mắm", 2.5),
            ("canh chua", 2.5),
            ("nem chua", 1.5),
            ("bún riêu", 2.8),
            ("bánh da lợn", 2.5),
            ("bánh đúc", 2.5),
            ("bánh pía", 3.7),
            ("bánh canh", 2.6),
            ("bánh khọt", 2.0),
            ("bánh bột lọc", 2.3),
            ("bánh căn", 1.4),
            ("cơm chiên", 2.2),
            ("bánh tiêu", 2.0),
            ("bún thịt nướng", 2.3),
            ("bánh chưng", 3.5),
            ("bánh bò", 2.0),
            ("chả giò", 2.0),
            ("bún đậu mắm tôm", 2.7),
            ("bánh bèo", 1.2),
            ("bánh tét", 3.6),
            ("cao lầu", 2.0),
            ("cháo lòng", 1.0),
            ("cá kho tộ", 2.1),
            ("bún bò huế", 2.8),
            ("phở", 3.5),
            ("xôi xéo", 2.0),
            ("bánh mì", 2.1),
            ("bánh xèo", 2.5),
            ("cơm tấm", 3.2),
            ("hủ tiếu", 2.5),
        )

        self.food_data = {
            UNKNOWN: {
                "id": UNKNOWN_INDEX,
                "calories": UNKNOWN_CALO,
                "name_accent": UNKNOWN,
            }
        }
        self.id_to_food = {
            UNKNOWN_INDEX: {
                "calories": UNKNOWN_CALO,
                "name_accent": UNKNOWN,
                "name_no_accent": UNKNOWN,
            }
        }

        for food_id, (name_accent, calories) in enumerate(self.__foods):
            name_no_accent = self._remove_accents(name_accent)
            data_food_general = {"calories": calories}

            self.food_data[name_no_accent] = {
                **data_food_general,
                "id": food_id,
                "name_accent": name_accent,
            }
            self.id_to_food[food_id] = {
                **data_food_general,
                "name_accent": name_accent,
                "name_no_accent": name_no_accent,
            }

    def _remove_accents(self, text):
        """Remove accents from text."""
        text = unicodedata.normalize("NFD", text)
        text = re.sub(r"[\u0300-\u036f]", "", text)
        return text

    def _get_by_id(self, food_id):
        """Get food by ID."""
        return self.id_to_food.get(food_id)

    def _get_by_name(self, name):
        """Get food by name."""
        return self.food_data.get(name.lower())

    def get_calories(self, identifier):
        """Get calories by ID or name."""
        if isinstance(identifier, int):
            food = self._get_by_id(identifier)
        else:
            food = self._get_by_name(identifier)

        if food:
            return food["calories"]
        return None

    def get_name(self, identifier, remove_accents=False):
        """Get name by ID or name."""
        if isinstance(identifier, int):
            food = self._get_by_id(identifier)
        else:
            food = self._get_by_name(identifier)

        if food:
            return (
                food["name_accent"]
                if not remove_accents
                else food.get("name_no_accent")
            )
        return UNKNOWN


FoodDictionary = FoodDictionaryService()
