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
            ("bánh cuốn", 3.5),
            ("mì quảng", 7.0),
            ("bánh tráng nướng", 4.8),
            ("bánh trung thu", 9.0),
            ("bánh tai heo", 2.0),
            ("gỏi cuốn", 3.0),
            ("bánh giò", 6.0),
            ("bún mắm", 6.5),
            ("canh chua", 4.0),
            ("nem chua", 1.8),
            ("bún riêu", 7.0),
            ("bánh da lợn", 4.0),
            ("bánh đúc", 3.9),
            ("bánh pía", 10.0),
            ("bánh canh", 5.0),
            ("bánh khọt", 8.0),
            ("bánh bột lọc", 6.0),
            ("bánh căn", 8.0),
            ("cơm chiên", 4.8),
            ("bánh tiêu", 3.8),
            ("bún thịt nướng", 6.5),
            ("bánh chưng", 18.0),
            ("bánh bò", 5.0),
            ("chả giò", 5.5),
            ("bún đậu mắm tôm", 7.7),
            ("bánh bèo", 4.5),
            ("bánh tét", 10.0),
            ("cao lầu", 5.5),
            ("cháo lòng", 3.7),
            ("cá kho tộ", 3.1),
            ("bún bò huế", 8.0),
            ("phở", 6),
            ("xôi xéo", 8.0),
            ("bánh mì", 5.1),
            ("bánh xèo", 5.0),
            ("cơm tấm", 9.0),
            ("hủ tiếu", 8.5),
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
