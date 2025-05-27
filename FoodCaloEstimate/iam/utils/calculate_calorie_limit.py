# Copyright (C)
# date: 27-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Calculate Calorie Limit Utility."""

from FoodCaloEstimate.iam.constants.period_choices import TimePeriod


def calculate_calorie_limit(
    gender: bool | None,
    age: int | None,
    height: int | None,
    weight: int | None,
    period_label: str,
    calorie_limit: float | None,
) -> float | None:
    """Calculate Calorie Limit."""
    if None in {gender, age, height, weight}:
        return calorie_limit

    # Calculate the base BMR using weight, height, and age
    # This part is common for both genders
    base_bmr_calculation = 10 * weight + 6.25 * height - 5 * age

    # Determine the gender-specific adjustment value
    # Add 5 for males, subtract 161 for females
    gender_specific_adjustment = 5 if gender else -161

    # Add the gender adjustment to the base BMR
    total_calculated_bmr_per_day = base_bmr_calculation + gender_specific_adjustment

    total_calculated_bmr = total_calculated_bmr_per_day * TimePeriod.from_label(
        period_label
    )

    # Round the final BMR to two decimal places for accuracy
    final_bmr_value = round(total_calculated_bmr, 2)

    return final_bmr_value
