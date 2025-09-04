from django.db import models

class InfoTable(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=250, null=True, blank=True)
    def __str__(self):
        return f"{self.name} {self.amount}"

class UpdatedInfoTable(models.Model):
    name = models.CharField(max_length=100)
    updated_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.updated_amount}"