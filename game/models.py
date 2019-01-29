from django.db import models

# Create your models here.
class QuantumCat(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class QuantumCats(models.Model):
    cat_choices = models.CharField(max_length=14)

    def __str__(self):
        return self.cat_choices
