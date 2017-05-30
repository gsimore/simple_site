'''
Models for Shop
'''
from django.db import models
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class Item(models.Model):
    '''
    class Item for modelling a buyable shop item.
    attributes:
        title, description, price, image, thumbnail(auto generated)
    '''
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='image_uploads')
    thumbnail = models.ImageField(
        upload_to='thumbnail_uploads',
        max_length=500,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    def create_thumbnail(self):
        if not self.image:
            return

        THUMBNAIL_SIZE = (300, 400)
        DJANGO_TYPE = self.image.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = '.jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = '.png'

        image = Image.open(BytesIO(self.image.read()))
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                temp_handle.read(), content_type=DJANGO_TYPE)

        self.thumbnail.save(
            '{}thumbnail{}'.format(os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
            save=False
        )

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        force_update = False
        if self.id:
            force_update = True

        super(Item, self).save(force_update=force_update)
