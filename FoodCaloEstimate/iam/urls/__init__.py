# Copyright (C)
# date: 09-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Init."""


from FoodCaloEstimate.iam.urls.auth_urls import urlpatterns as auth_urls
from FoodCaloEstimate.iam.urls.reference_point_urls import (
    urlpatterns as reference_point_urls,
)


urlpatterns = (
    [
        # custom prefix
        # path("", include(auth_urls)),
    ]
    + auth_urls
    + reference_point_urls
)
