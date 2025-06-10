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
    activity_factor: float | None,
    calorie_limit: float | None,
) -> float | None:
    """Calculate Calorie Limit."""
    if None in {gender, age, height, weight, activity_factor}:
        return calorie_limit

    # Calculate the base BMR using weight, height, and age
    # This part is common for both genders
    base_bmr_calculation = 10 * weight + 6.25 * height - 5 * age  # type: ignore

    # Determine the gender-specific adjustment value
    # Add 5 for males, subtract 161 for females
    gender_specific_adjustment = 5 if gender else -161

    # Add the gender adjustment to the base BMR
    total_calculated_bmr = base_bmr_calculation + gender_specific_adjustment

    # Calculate the total daily energy expenditure (TDEE)
    total_daily_energy_expenditure = total_calculated_bmr * activity_factor  # type: ignore

    total_calculated_bmr = total_daily_energy_expenditure * TimePeriod.from_label(
        period_label
    )

    return round(total_daily_energy_expenditure, 2)
