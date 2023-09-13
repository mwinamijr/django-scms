from django.db import models
from django.conf import settings
from datetime import date

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

class ClassLevel(models.Model):
    name = models.CharField(max_length=15, blank=True, null=True, verbose_name="Class Name")
    id = models.IntegerField(unique=True, primary_key=True, verbose_name="Grade Number")
    shortname = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

    @property
    def grade(self):
        return self.id

class Student(models.Model):
    addmission_number = models.IntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=150, null=True, verbose_name="First Name")
    middle_name = models.CharField(max_length=150, null=True, verbose_name="Middle Name")
    last_name = models.CharField(max_length=150,  null=True, verbose_name="Last Name")
    image = models.ImageField(upload_to="student_pics", blank=True, null=True)
    alert = models.CharField(max_length=500, blank=True, help_text="Warn any user who accesses this record with this text")
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True, null=True)
    birthday = models.DateField(blank=True, null=True, verbose_name="Birth Date", validators=settings.DATE_VALIDATORS)
    class_level = models.ForeignKey(
        ClassLevel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Class level")
    class_of_year = models.ForeignKey(
        ClassYear, 
        on_delete=models.SET_NULL,
        verbose_name="Graduating Class", 
        blank=True, null=True)
    std_vii_number = models.CharField(max_length=15,blank=True, null=True, unique=True, help_text="For integration with outside databases")
    prems_number = models.CharField(max_length=15,blank=True, null=True, unique=True, help_text="For integration with outside databases")

    parent_contact = models.CharField(max_length=13, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True)
    post_code = models.IntegerField(blank=True, null=True)
    parent_email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    siblings = models.ManyToManyField('Student', blank=True)
    #gpa = CachedDecimalField(editable=False, max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        permissions = (
            ("viewStudent", "View student"),
            ("reports", "View reports"),
        )
        ordering = ("addmission_number","first_name", "last_name")

    def __str__(self):
        return f"{self.addmission_number}-{self.first_name} {self.last_name}"

    def get_absolute_url():
        pass
    
class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to='api/sis/students/bulkupload')


class StudentHealthRecord(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    record = models.TextField()

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}"


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
