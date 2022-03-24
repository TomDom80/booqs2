from django.db import models


class PublicationLanguage(models.Model):
    lang = models.CharField(max_length=15, unique=True, blank=True, null=True)

    class Meta:
        ordering = ("lang",)

    def __str__(self):
        return self.lang


class Author(models.Model):
    name = models.CharField(max_length=64, unique=False)
    surname = models.CharField(max_length=64, unique=False)

    class Meta:
        ordering = ("name",)
        # ordering = ('id',)
        unique_together = (
            "name",
            "surname",
        )

    def __str__(self):
        return self.name + " " + self.surname


class Book(models.Model):
    title = models.TextField(unique=True, blank=False, null=False)
    authors = models.ManyToManyField("Author")
    pub_date = models.DateField(blank=False, null=False)
    isbn_nr = models.CharField(max_length=64, unique=True)
    pages_qty = models.PositiveSmallIntegerField(blank=False, null=False)
    cover_link = models.URLField(blank=False, null=False)
    pub_lang = models.ForeignKey(
        "PublicationLanguage", on_delete=models.PROTECT, blank=False, null=False
    )

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.title
