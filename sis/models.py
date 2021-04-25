from django.db import models
from django.conf import settings
from datetime import date

class PhoneNumber(models.Model):
    number = models.CharField(max_length=15, blank=True, null=True)
    _type = models.CharField(max_length=2, choices=(('H', 'Home'), ('C', 'Cell'), ('W', 'Work'), ('O', 'Other')), blank=True)
    def __str__(self):
        return self.number


class EmergencyContact(models.Model):
    fname = models.CharField(max_length=255, verbose_name="First Name")
    mname = models.CharField(max_length=255, blank=True, null=True, verbose_name="Middle Name")
    lname = models.CharField(max_length=255, verbose_name="Last Name")
    relationship_to_student = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True)
    primary_contact = models.BooleanField(default=True, help_text="This contact is where mailings should be sent to. In the event of an emergency, this is the person that will be contacted first.")
    emergency_only = models.BooleanField(default=False, help_text="Only contact in case of emergency")
    sync_schoolreach = models.BooleanField(help_text="Sync this contact with schoolreach",default=True)

    class Meta:
        ordering = ('primary_contact', 'lname')
        verbose_name = "Student Contact"

    def __str__(self):
        txt = self.fname + " " + self.lname
        for number in self.emergencycontactnumber_set.all():
            txt += " " + str(number)
        return txt

    def save(self, *args, **kwargs):
        super(EmergencyContact, self).save(*args, **kwargs)
        self.cache_student_addresses()

    def cache_student_addresses(self):
        """cache these for the student for primary contact only
        There is another check on Student in case all contacts where deleted"""
        if self.primary_contact:
            for student in self.student_set.all():
                student.parent_guardian = self.fname + " " + self.lname
                student.city = self.city
                student.state = self.state
                student.post_code = self.post_code
                student.parent_email = self.email
                student.save()
                for contact in student.emergency_contacts.exclude(id=self.id):
                    # There should only be one primary contact!
                    if contact.primary_contact:
                        contact.primary_contact = False
                        contact.save()

class EmergencyContactNumber(PhoneNumber):
    contact = models.ForeignKey(EmergencyContact, on_delete=models.CASCADE)
    primary = models.BooleanField(default=False, )

    class Meta:
        verbose_name = "Student Contact Number"

    def save(self, *args, **kwargs):
        if self.primary:
            for contact in self.contact.emergencycontactnumber_set.exclude(id=self.id).filter(primary=True):
                contact.primary = False
                contact.save()
        super(EmergencyContactNumber, self).save(*args, **kwargs)

    def __str__(self):
        return self.get__type_display() + ":" + self.number

class GradeLevel(models.Model):
    id = models.IntegerField(unique=True, primary_key=True, verbose_name="Grade Number")
    name = models.CharField(max_length=150, unique=True, verbose_name="Grade Name")

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

    @property
    def grade(self):
        return self.id

class ClassYear(models.Model):
    """ Class year such as class of 2010.
    """
    year = models.IntegerField(unique=True, help_text="Example 2014")
    full_name = models.CharField(max_length=255, help_text="Example Class of 2014", blank=True)

    class Meta:
        verbose_name = "Graduating Class"
        verbose_name_plural = "Graduating Classes"

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = "Class of %s" % (self.year,)
        super(ClassYear, self).save(*args, **kwargs)

class Student(models.Model):
    fname = models.CharField(max_length=150, blank=True, null=True, verbose_name="First Name")
    mname = models.CharField(max_length=150, blank=True, null=True, verbose_name="Middle Name")
    lname = models.CharField(max_length=150, blank=True, null=True, verbose_name="Last Name")
    grad_date = models.DateField(blank=True, null=True, validators=settings.DATE_VALIDATORS)
    pic = models.ImageField(upload_to="student_pics", blank=True, null=True)
    alert = models.CharField(max_length=500, blank=True, help_text="Warn any user who accesses this record with this text")
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True, null=True)
    bday = models.DateField(blank=True, null=True, verbose_name="Birth Date", validators=settings.DATE_VALIDATORS)
    year = models.ForeignKey(
        GradeLevel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Grade level")
    class_of_year = models.ForeignKey(
        ClassYear, 
        on_delete=models.SET_NULL,
        verbose_name="Graduating Class", 
        blank=True, null=True)
    #date_dismissed = models.DateField(blank=True, null=True, validators=settings.DATE_VALIDATORS)
    prems_number = models.CharField(max_length=15,blank=True, null=True, unique=True, help_text="For integration with outside databases")

    # These fields are cached from emergency contacts
    parent_guardian = models.CharField(max_length=150, blank=True, editable=False)
    street = models.CharField(max_length=150, blank=True, editable=False)
    state = models.CharField(max_length=255, blank=True, editable=True, null=True)
    city = models.CharField(max_length=255, blank=True)
    post_code = models.IntegerField(blank=True, editable=False, null=True)
    parent_email = models.EmailField(blank=True, editable=False)
    notes = models.TextField(blank=True)
    emergency_contacts = models.ManyToManyField(EmergencyContact, verbose_name="Student Contact", blank=True)
    siblings = models.ManyToManyField('Student', blank=True)
    #gpa = CachedDecimalField(editable=False, max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        permissions = (
            ("viewStudent", "View student"),
            ("reports", "View reports"),
        )
        ordering = ("fname", "lname")

    def __str__(self):
        return f"{self.fname} {self.lname}"

    def get_absolute_url():
        pass
class StudentHealthRecord(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    record = models.TextField()

    def __str__(self):
        return f"{self.student.fname} {self.student.lname}"

class GradeScale(models.Model):
    """ Translate a numeric grade to some other scale.
    Example: Letter grade or 4.0 scale. """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    def get_rule(self, grade):
        if grade is not None:
            return self.gradescalerule_set.filter(min_grade__lte=grade, max_grade__gte=grade).first()

    def to_letter(self, grade):
        rule = self.get_rule(grade)
        if rule:
            return rule.letter_grade

    def to_numeric(self, grade):
        rule = self.get_rule(grade)
        if rule:
            return rule.numeric_scale


class GradeScaleRule(models.Model):
    """ One rule for a grade scale.  """
    min_grade = models.DecimalField(max_digits=5, decimal_places=2)
    max_grade = models.DecimalField(max_digits=5, decimal_places=2)
    letter_grade = models.CharField(max_length=50, blank=True, null=True)
    numeric_scale = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    grade_scale = models.ForeignKey(GradeScale, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('min_grade', 'max_grade', 'grade_scale')

    def __str__(self):
        return f"{self.min_grade}-{self.max_grade} {self.letter_grade} {self.numeric_scale}"


#def get_default_benchmark_grade():
#    return str(Configuration.get_or_default("Benchmark-based grading", "False").value).lower() == "true"

class SchoolYear(models.Model):
    name = models.CharField(max_length=255, unique=True)
    start_date = models.DateField(validators=settings.DATE_VALIDATORS)
    end_date = models.DateField(validators=settings.DATE_VALIDATORS)
    grad_date = models.DateField(blank=True, null=True, validators=settings.DATE_VALIDATORS)
    #grade_scale = models.ForeignKey(GradeScale, blank=True, null=True, help_text="Alternative grade scale such as letter grades or a 4.0 scale")
    active_year = models.BooleanField(default=False,
        help_text="DANGER!! This is the current school year. There can only be one and setting this will remove it from other years. " \
                  "If you want to change the active year you almost certainly want to click Management, Change School Year.")
#    benchmark_grade = models.BooleanField(default=get_default_benchmark_grade,
#                                          help_text="Causes additional information to appear on transcripts. The configuration option \"Benchmark-based grading\" sets the default for this field.")

    class Meta:
        ordering = ('-start_date',)

    def __str__(self):
        return self.name

    def get_number_days(self, date=date.today()):
        """ Returns number of active school days in this year, based on
        each marking period of the year.
        date: Defaults to today, date to count towards. Used to get days up to a certain date"""
        mps = self.markingperiod_set.filter(show_reports=True).order_by('start_date')
        day = 0
        for mp in mps:
            day += mp.get_number_days(date)
        return day

    def save(self, *args, **kwargs):
        super(SchoolYear, self).save(*args, **kwargs)
        if self.active_year:
            _all = SchoolYear.objects.exclude(id=self.id).update(active_year=False)


class MessageToStudent(models.Model):
    """ Stores a message to be shown to students for a specific amount of time
    """
    message = models.TextField(help_text="This message will be shown to students when they log in.")
    start_date = models.DateField(auto_now_add=False, validators=settings.DATE_VALIDATORS)
    end_date = models.DateField(auto_now_add=False, validators=settings.DATE_VALIDATORS)
    def __str__(self):
        return self.message

