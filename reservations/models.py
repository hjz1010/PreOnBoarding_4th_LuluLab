from django.db import models

from core.models import TimeStampModel

class Time(models.Model): 
	time = models.TimeField()
	
	class Meta: 
		db_table = 'time'


class HospitalType(models.Model): 
	type = models.CharField(max_length = 50)

	class Meta: 
		db_table = 'hospital_type'


class Province(models.Model): 
	name = models.CharField(max_length = 50)

	class Meta: 
		db_table = 'province'


class ReservationType(models.Model): 
	type = models.CharField(max_length = 50)

	class Meta: 
		db_table = 'reservation_type'


class ReservationStatus(models.Model): 
	status = models.CharField(max_length = 50)

	class Meta: 
		db_table = 'reservation_status'


class Hospital(models.Model): 
	name          = models.CharField(max_length= 50)
	address       = models.CharField(max_length=100)
	contact       = models.CharField(max_length=50)
	hospital_type = models.ForeignKey('HospitalType', on_delete=models.CASCADE)
	province      = models.ForeignKey('Province', on_delete=models.CASCADE)

	class Meta: 
		db_table = 'hospital'


class Reservation(TimeStampModel): 
	reservation_number = models.CharField(max_length = 100)
	patient_name       = models.CharField(max_length = 10)
	patient_birth      = models.DateField()
	date               = models.DateField()
	customer           = models.ForeignKey('users.User', on_delete=models.CASCADE)
	time               = models.ForeignKey('Time', on_delete=models.CASCADE)
	hospital           = models.ForeignKey('Hospital', on_delete=models.CASCADE)
	reservation_type   = models.ForeignKey('ReservationType', on_delete=models.CASCADE)
	reservation_status = models.ForeignKey('ReservationStatus', on_delete=models.CASCADE)

	class Meta: 
		db_table = 'reservation'

