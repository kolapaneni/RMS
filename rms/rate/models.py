from django.db import models


class CommonStampModel(models.Model):
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DiscountTypeChoices(models.TextChoices):
    FIXED = 'FIXED'
    PERCENTAGE = 'PERCENTAGE'


class RoomRate(CommonStampModel):
    """
    Model to store the room room
    """
    room_id = models.IntegerField()
    room_name = models.CharField(max_length=255)
    default_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.room_name


class OverriddenRoomRate(CommonStampModel):
    room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE)
    overridden_rate = models.DecimalField(max_digits=10, decimal_places=2)
    stay_date = models.DateField()

    class Meta:
        unique_together = ['room_rate', 'stay_date']


class Discount(CommonStampModel):
    discount_id = models.IntegerField()
    discount_name = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=10, choices=DiscountTypeChoices.choices)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2)


class DiscountRoomRate(models.Model):
    room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
