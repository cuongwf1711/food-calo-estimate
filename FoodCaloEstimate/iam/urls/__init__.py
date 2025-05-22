# Copyright (C)
# date: 09-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Init."""


from FoodCaloEstimate.iam.urls.auth_urls import urlpatterns as auth_urls
from FoodCaloEstimate.iam.urls.user_profile_urls import (
    urlpatterns as user_profile_urls,
)


urlpatterns = (
    [
        # custom prefix
        # path("", include(auth_urls)),
    ]
    + auth_urls
    + user_profile_urls
)
