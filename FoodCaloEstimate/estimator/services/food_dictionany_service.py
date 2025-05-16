# Copyright (C)
# date: 13-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Food Dictionary."""

import re
import unicodedata

from FoodCaloEstimate.estimator.constants.image_constants import UNKNOWN, UNKNOWN_CALO, UNKNOWN_INDEX


class FoodDictionaryService:
    """Food Dictionary Class."""

    def __init__(self):
        """Init."""
        self.__foods = (
            ("bánh cuốn", 140),
            ("mì quảng", 450),
            ("bánh tráng nướng", 250),
            ("bánh trung thu", 350),
            ("bánh tai heo", 320),
            ("gỏi cuốn", 120),
            ("bánh giò", 200),
            ("bún mắm", 380),
            ("canh chua", 150),
            ("nem chua", 220),
            ("bún riêu", 320),
            ("bánh da lợn", 270),
            ("bánh đúc", 170),
            ("bánh pía", 400),
            ("bánh canh", 340),
            ("bánh khọt", 280),
            ("bánh bột lọc", 190),
            ("bánh căn", 240),
            ("cơm chiên", 380),
            ("bánh tiêu", 350),
            ("bún thịt nướng", 420),
            ("bánh chưng", 290),
            ("bánh bò", 250),
            ("chả giò", 300),
            ("bún đậu mắm tôm", 450),
            ("bánh bèo", 150),
            ("bánh tét", 290),
            ("cao lầu", 380),
            ("cháo lòng", 290),
            ("cá kho tộ", 250),
            ("bún bò huế", 400),
            ("phở", 350),
            ("xôi xéo", 420),
            ("bánh mì", 380),
            ("bánh xèo", 330),
            ("cơm tấm", 450),
            ("hủ tiếu", 320),
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
            return food["name_accent"] if not remove_accents else food.get("name_no_accent")
        return UNKNOWN


FoodDictionary = FoodDictionaryService()
