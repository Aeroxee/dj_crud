from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL")

# Create your models here.

def get_data_image_path(instance, filename):
    """Fungsi untuk mengembalikan image path.
    """
    import os.path
    return os.path.join("datas", instance.owner.username, filename)

class Data(models.Model):
    """Class ini mengimplementasikan field-field yang berada di tabel data.
    """
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_("judul"), max_length=255)
    description = models.TextField(_("deskripsi"), blank=True)
    image = models.ImageField(_("gambar"), upload_to=get_data_image_path, blank=True, null=True)
    
    def __str__(self):
        """Fungsi untuk mengembalikan nama data.
        """
        return self.title