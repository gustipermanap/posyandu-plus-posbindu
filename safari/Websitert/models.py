from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField

class RW(models.Model):
    text = models.CharField(max_length=12,verbose_name='Nama Database')
    slide = models.ImageField(upload_to='images/', verbose_name='Carousel', blank=True, null=True)

    class Meta:
        verbose_name_plural = "  RW"
        ordering = ['text']

    def __str__(self):
        return self.text

class Organisasi(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    text = HTMLField()
    slug = models.SlugField(null=True,  unique=True)

    class Meta:    
        verbose_name_plural = "Organisasi"
        ordering = ['-title']
    
    def __str__(self):
        return self.title

class About(models.Model):   
    about = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True, default=False)
    text = HTMLField(blank=True, null=True)
    
    def __str__(self):
        return self.title

class Fasilitas(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    slug = models.SlugField(null=True,  unique=True)
    
    class Meta:
        verbose_name_plural = "Fasilitas"
        ordering = ['-name']
    
    def __str__(self):
        return self.name

class Acara(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True,  unique=True)
    # overview = HTMLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    thumbnail = models.ImageField(upload_to='images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Acara"
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

class Struktur(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "  Struktur Organisasi"

    def __str__(self):
        return self.title

class Tentang(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    judul = models.CharField(max_length=50, blank=True, default='')
    contentkanan = HTMLField(verbose_name='Content Kiri', blank=True, null=True)
    contentkiri = HTMLField(verbose_name='Content Kanan', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = " Tentang Kami"

    def __str__(self):
        return self.title
    
class rt1(models.Model):
    about = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    text = HTMLField(blank=True, null=True)

    title = models.CharField(max_length=50, blank=True, null=True)
    judul = models.CharField(max_length=50, blank=True, null=True, default='')
    contentkanan = HTMLField(verbose_name='Content Kiri', blank=True, null=True)
    contentkiri = HTMLField(verbose_name='Content Kanan', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')

        

    class Meta:
        verbose_name_plural = "RT  1"
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
        
class rt2(models.Model):
    about = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    text = HTMLField(blank=True, null=True)

    title = models.CharField(max_length=50, blank=True, null=True)
    judul = models.CharField(max_length=50, blank=True, null=True, default='')
    contentkanan = HTMLField(verbose_name='Content Kiri', blank=True, null=True)
    contentkiri = HTMLField(verbose_name='Content Kanan', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')

    class Meta:
        verbose_name_plural = "RT  2"
        ordering = ['title']

    def __str__(self):
        return self.title

class rt3(models.Model):
    about = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    text = HTMLField(blank=True, null=True)

    title = models.CharField(max_length=50, blank=True, null=True)
    judul = models.CharField(max_length=50, blank=True, null=True, default='')
    contentkanan = HTMLField(verbose_name='Content Kiri', blank=True, null=True)
    contentkiri = HTMLField(verbose_name='Content Kanan', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')

    class Meta:
        verbose_name_plural = "RT  3"
        ordering = ['title']

    def __str__(self):
        return self.title

class rt4(models.Model):
    about = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    text = HTMLField(blank=True, null=True)

    title = models.CharField(max_length=50, blank=True, null=True)
    judul = models.CharField(max_length=50, blank=True, null=True, default='')
    contentkanan = HTMLField(verbose_name='Content Kiri', blank=True, null=True)
    contentkiri = HTMLField(verbose_name='Content Kanan', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')

    class Meta:
        verbose_name_plural = "RT  4"
        ordering = ['title']

    def __str__(self):
        return self.title

class rt5(models.Model):
    about = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    text = HTMLField(blank=True, null=True)

    title = models.CharField(max_length=50, blank=True, null=True)
    judul = models.CharField(max_length=50, blank=True, null=True, default='')
    contentkanan = HTMLField(verbose_name='Content Kiri', blank=True, null=True)
    contentkiri = HTMLField(verbose_name='Content Kanan', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')

    class Meta:
        verbose_name_plural = "RT  5"
        ordering = ['title']

    def __str__(self):
        return self.title

class rt6(models.Model):
    about = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    text = HTMLField(blank=True, null=True)

    title = models.CharField(max_length=50, blank=True, null=True)
    judul = models.CharField(max_length=50, blank=True, null=True, default='')
    contentkanan = HTMLField(verbose_name='Content Kiri', blank=True, null=True)
    contentkiri = HTMLField(verbose_name='Content Kanan', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')

    class Meta:
        verbose_name_plural = "RT  6"
        ordering = ['title']

    def __str__(self):
        return self.title

class rt7(models.Model):
    about = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    text = HTMLField(blank=True, null=True)

    title = models.CharField(max_length=50, blank=True, null=True)
    judul = models.CharField(max_length=50, blank=True, null=True, default='')
    contentkanan = HTMLField(verbose_name='Content Kiri', blank=True, null=True)
    contentkiri = HTMLField(verbose_name='Content Kanan', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')

    class Meta:
        verbose_name_plural = "RT  7"
        ordering = ['title']

    def __str__(self):
        return self.title

class rt8(models.Model):
    about = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    text = HTMLField(blank=True, null=True)

    title = models.CharField(max_length=50, blank=True, null=True)
    judul = models.CharField(max_length=50, blank=True, null=True, default='')
    contentkanan = HTMLField(verbose_name='Content Kiri', blank=True, null=True)
    contentkiri = HTMLField(verbose_name='Content Kanan', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')

    class Meta:
        verbose_name_plural = "RT  8"
        ordering = ['title']

    def __str__(self):
        return self.title

class rt9(models.Model):
    about = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    text = HTMLField(blank=True, null=True)

    title = models.CharField(max_length=50, blank=True, null=True)
    judul = models.CharField(max_length=50, blank=True, null=True, default='')
    contentkanan = HTMLField(verbose_name='Content Kiri', blank=True, null=True)
    contentkiri = HTMLField(verbose_name='Content Kanan', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')

    class Meta:
        verbose_name_plural = "RT  9"
        ordering = ['title']

    def __str__(self):
        return self.title

class rt10(models.Model):
    about = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    text = HTMLField(blank=True, null=True)

    title = models.CharField(max_length=50, blank=True, null=True)
    judul = models.CharField(max_length=50, blank=True, null=True, default='')
    contentkanan = HTMLField(verbose_name='Content Kiri', blank=True, null=True)
    contentkiri = HTMLField(verbose_name='Content Kanan', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')

    class Meta:
        verbose_name_plural = "RT 10"
        ordering = ['title']

    def __str__(self):
        return self.title

class rt11(models.Model):
    about = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    text = HTMLField(blank=True, null=True)

    title = models.CharField(max_length=50, blank=True, null=True)
    judul = models.CharField(max_length=50, blank=True, null=True, default='')
    contentkanan = HTMLField(verbose_name='Content Kiri', blank=True, null=True)
    contentkiri = HTMLField(verbose_name='Content Kanan', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')

    class Meta:
        verbose_name_plural = "RT 11"
        ordering = ['title']

    def __str__(self):
        return self.title
