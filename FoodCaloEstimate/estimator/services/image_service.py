"""Image Service."""

from FoodCaloEstimate.estimator.constants.image_constants import CLOUDINARY_PUBLIC_ID, LOCAL_IMAGE_PATH, ORIGIN_IMAGE, SEGMENTATION_IMAGE
from FoodCaloEstimate.estimator.services.cloudinary_service import CloudinaryService
from FoodCaloEstimate.estimator.services.food_dictionany_service import FoodDictionary
from FoodCaloEstimate.estimator.services.local_storage_service import LocalStorageService


class ImageService:
    """Image Service."""

    @staticmethod
    def upload_image(image_byteio, *folder):
        """Upload image."""
        cloudinary_storage_image = CloudinaryService().upload_image(
            image_byteio,
            *folder,
        )
        local_storage_image = LocalStorageService().upload_image(
            image_byteio,
            *folder,
        )

        return cloudinary_storage_image, local_storage_image

    @staticmethod
    def move_image(image_url, image_type, label_name):
        """Move image."""
        image_url.update(LocalStorageService().move_image(
            image_url[LOCAL_IMAGE_PATH], image_type, label_name
        ))
        CloudinaryService().move_image(
            image_url[CLOUDINARY_PUBLIC_ID], image_type, label_name
        )

    @staticmethod
    def move_image_and_update_instance(instance):
        """Move image and update instance."""
        label_name = FoodDictionary.get_name(instance.label, remove_accents=True)
        ImageService.move_image(instance.url[ORIGIN_IMAGE], ORIGIN_IMAGE, label_name)
        ImageService.move_image(instance.url[SEGMENTATION_IMAGE], SEGMENTATION_IMAGE, label_name)

        instance.save(update_fields=["url"])

    @staticmethod
    def delete_image(image_url_dict):
        """Delete image."""
        CloudinaryService().delete_image(image_url_dict)
        LocalStorageService().delete_image(image_url_dict)
