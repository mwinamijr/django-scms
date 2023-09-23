from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.core import validators
import re
from datetime import date


def class_room_validator(value):
	from .models import ClassRoom
	if ClassRoom.objects.filter(name=value).exists():
		raise ValidationError(_('{} already exists...!!!'.format(value)))


def subject_validator(value):
	from .models import Subject

	if Subject.objects.filter(name=value).exists():
		raise ValidationError(_('{} subject already exist....!!!'.format(value)))


def stream_validator(value):
	from .models import Stream
	if Stream.objects.filter(name=value).exists():
		raise ValidationError(_('{} stream already exists...!!!'.format(value)))


def students_date_of_birth_validator(value):
	"""
	this function is responsible o validating the students date of birth
	if the students year of  birth is less than or equal to least_year_of_birth
	then we raise a validation error
	:imports Student from models
	:param value:
	:return:
	"""
	from .models import Student
	required_age = 12
	least_year_of_birth = date.today().year - required_age

	if value.year >= least_year_of_birth:
		raise ValidationError(_('not valid date, student should be at least 13 years of age..!!!'))


@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
	regex = r'^[a-zA-Z]+\/(...)\/(....)'
	message = _(
		'Ener a valid username. This valu may contain only English letters,'
		'numbers, and @/./+/-/_ characters.'
	)
	flags = re.ASCII
