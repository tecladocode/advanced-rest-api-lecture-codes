from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity


from libs import image_helper
from libs.strings import gettext
from schemas.image import ImageSchema

image_schema = ImageSchema()


class ImageUpload(Resource):
    @jwt_required()
    def post(self):
        """
        This endpoint is used to upload an image file. It uses the
        JWT to retrieve user information and save the image in the user's folder.
        If a file with the same name exists in the user's folder, name conflicts
        will be automatically resolved by appending a underscore and a smallest
        unused integer. (eg. filename.png to filename_1.png).
        """
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        try:
            # save(self, storage, folder=None, name=None)
            image_path = image_helper.save_image(data["image"], folder=folder)
            # here we only return the basename of the image and hide the internal folder structure from our user
            basename = image_helper.get_basename(image_path)
            return {"message": gettext("image_uploaded").format(basename)}, 201
        except UploadNotAllowed:  # forbidden file type
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400
