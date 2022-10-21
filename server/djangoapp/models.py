from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=250)
    # logo = models.ImageField()

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    Sedan = 'Sedan'
    SUV = 'SUV'
    Wagon = 'Wagon'
    Hatch_Back = 'Hatch_Back'
    Convertible = 'Convertible'
    Pickup = 'Pickup'
    Van = 'Van'
    TYPE_CHOICES = [
        (Sedan, 'Sedan'),
        (SUV, 'SUV'),
        (Wagon, 'Wagon'),
        (Hatch_Back, 'Hatch Back'),
        (Pickup, 'Pickup'),
        (Van, 'Van')
    ]
    name = models.CharField(max_length=20)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    dealer_id = models.IntegerField()
    year = models.DateField()

    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
