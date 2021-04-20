from django.db import models


class EmergencyContact(models.Model):
    fname = models.CharField(max_length=255, verbose_name="First Name")
    mname = models.CharField(max_length=255, blank=True, null=True, verbose_name="Middle Name")
    lname = models.CharField(max_length=255, verbose_name="Last Name")
    relationship_to_student = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True, default=get_city)
    state = USStateField(blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True)
    primary_contact = models.BooleanField(default=True, help_text="This contact is where mailings should be sent to. In the event of an emergency, this is the person that will be contacted first.")
    emergency_only = models.BooleanField(default=False, help_text="Only contact in case of emergency")
    sync_schoolreach = models.BooleanField(help_text="Sync this contact with schoolreach",default=True)

    class Meta:
        ordering = ('primary_contact', 'lname')
        verbose_name = "Student Contact"

    def __unicode__(self):
        txt = self.fname + " " + self.lname
        for number in self.emergencycontactnumber_set.all():
            txt += " " + unicode(number)
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
                student.street = self.street
                student.state = self.state
                student.parent_email = self.email
                student.save()
                for contact in student.emergency_contacts.exclude(id=self.id):
                    # There should only be one primary contact!
                    if contact.primary_contact:
                        contact.primary_contact = False
                        contact.save()
            # cache these for the applicant
            if hasattr(self, 'applicant_set'):
                for applicant in self.applicant_set.all():
                    applicant.set_cache(self)

    def show_student(self):
        students = ""
        for student in self.student_set.all():
            students += f"{student}, "
        return students[:-2]


class EmergencyContactNumber(PhoneNumber):
    contact = models.ForeignKey(EmergencyContact)
    primary = models.BooleanField(default=False, )

    class Meta:
        verbose_name = "Student Contact Number"

    def save(self, *args, **kwargs):
        if self.primary:
            for contact in self.contact.emergencycontactnumber_set.exclude(id=self.id).filter(primary=True):
                contact.primary = False
                contact.save()
        super(EmergencyContactNumber, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.ext:
            return self.get_type_display() + ":" + self.number + "x" + self.ext
        else:
            return self.get_type_display() + ":" + self.number

class GradeLevel(models.Model):
    id = models.IntegerField(unique=True, primary_key=True, verbose_name="Grade Number")
    name = models.CharField(max_length=150, unique=True, verbose_name="Grade Name")

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return unicode(self.name)

    @property
    def grade(self):
        return self.id

class ClassYear(models.Model):
    """ Class year such as class of 2010.
    """
    year = IntegerRangeField(unique=True, min_value=1900, max_value=2200, help_text="Example 2014")
    full_name = models.CharField(max_length=255, help_text="Example Class of 2014", blank=True)

    class Meta:
        verbose_name = "Graduating Class"
        verbose_name_plural = "Graduating Classes"

    def __unicode__(self):
        return unicode(self.full_name)

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = "Class of %s" % (self.year,)
        super(ClassYear, self).save(*args, **kwargs)

class Student(User, CustomFieldModel):
    mname = models.CharField(max_length=150, blank=True, null=True, verbose_name="Middle Name")
    grad_date = models.DateField(blank=True, null=True, validators=settings.DATE_VALIDATORS)
    pic = ImageWithThumbsField(upload_to="student_pics", blank=True, null=True, sizes=((70,65),(530, 400)))
    alert = models.CharField(max_length=500, blank=True, help_text="Warn any user who accesses this record with this text")
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True, null=True)
    bday = models.DateField(blank=True, null=True, verbose_name="Birth Date", validators=settings.DATE_VALIDATORS)
    year = models.ForeignKey(
        GradeLevel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Grade level")
    class_of_year = models.ForeignKey(ClassYear, verbose_name="Graduating Class", blank=True, null=True)
    date_dismissed = models.DateField(blank=True, null=True, validators=settings.DATE_VALIDATORS)
    reason_left = models.ForeignKey(ReasonLeft, blank=True, null=True)
    unique_id = models.IntegerField(blank=True, null=True, unique=True, help_text="For integration with outside databases")
    ssn = models.CharField(max_length=11, blank=True, null=True)  #Once 1.1 is out USSocialSecurityNumberField(blank=True)

    # These fields are cached from emergency contacts
    parent_guardian = models.CharField(max_length=150, blank=True, editable=False)
    street = models.CharField(max_length=150, blank=True, editable=False)
    state = USStateField(blank=True, editable=False, null=True)
    city = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=10, blank=True, editable=False)
    parent_email = models.EmailField(blank=True, editable=False)

    family_preferred_language = models.ForeignKey(LanguageChoice, blank=True, null=True, default=get_default_language)
    family_access_users = models.ManyToManyField(
        family_ref,
        blank=True,
        related_name="+",
    )
    alt_email = models.EmailField(blank=True, help_text="Alternative student email that is not their school email.")
    notes = models.TextField(blank=True)
    emergency_contacts = models.ManyToManyField(EmergencyContact, verbose_name="Student Contact", blank=True)
    siblings = models.ManyToManyField('Student', blank=True)
    cohorts = models.ManyToManyField(Cohort, through='StudentCohort', blank=True)
    cache_cohort = models.ForeignKey(Cohort, editable=False, blank=True, null=True, on_delete=models.SET_NULL, help_text="Cached primary cohort.", related_name="cache_cohorts")
    individual_education_program = models.BooleanField(default=False)
    gpa = CachedDecimalField(editable=False, max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        permissions = (
            ("view_student", "View student"),
            ("view_ssn_student", "View student ssn"),
            ("view_mentor_student", "View mentoring information student"),
            ("reports", "View reports"),
        )
        ordering = ("last_name", "first_name")

    def __unicode__(self):
        return u"{0}, {1}".format(self.last_name, self.first_name)

    def get_absolute_url():
        pass

class MessageToStudent(models.Model):
    """ Stores a message to be shown to students for a specific amount of time
    """
    message = RichTextField(help_text="This message will be shown to students when they log in.")
    start_date = models.DateField(default=date.today, validators=settings.DATE_VALIDATORS)
    end_date = models.DateField(default=date.today, validators=settings.DATE_VALIDATORS)
    def __unicode__(self):
        return self.message

