from datetime import datetime
from django.db import models

from django.contrib.auth.models import Group
from django.utils import timezone

from .validators import *

from administration.common_objs import *
from administration.models import AcademicYear
from users.models import CustomUser


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    order_rank = models.IntegerField(
        blank=True, null=True, help_text="Rank that courses will show up in reports"
    )

    class Meta:
        ordering = ("order_rank", "name")

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subject_code = models.CharField(max_length=10, blank=True, null=True, unique=True)
    is_selectable = models.BooleanField(
        default=False, help_text="select if subject is optional"
    )
    graded = models.BooleanField(
        default=True, help_text="Teachers can submit grades for this course"
    )
    description = models.CharField(max_length=255, blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="the department associated with this subject",
    )

    def __str__(self):
        return self.name


class Teacher(models.Model):
    username = models.CharField(unique=True, max_length=250, blank=True)
    first_name = models.CharField(max_length=300, verbose_name="First Name", blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=300, verbose_name="Last Name", blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, blank=True)
    email = models.EmailField(blank=True, null=True)
    empId = models.CharField(max_length=8, null=True, blank=True, unique=True)
    tin_number = models.CharField(max_length=9, null=True, blank=True)
    nssf_number = models.CharField(max_length=9, null=True, blank=True)
    short_name = models.CharField(max_length=3, null=True, blank=True, unique=True)
    isTeacher = models.BooleanField(default=True)
    salary = models.IntegerField(blank=True, null=True)
    subject_specialization = models.ManyToManyField(Subject, blank=True)
    national_id = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=150, blank=True)
    alt_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Personal Email apart from the one given by the school",
    )
    date_of_birth = models.DateField(blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="employee_images", blank=True, null=True)
    inactive = models.BooleanField(default=False)

    class Meta:
        ordering = ("first_name", "last_name")

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def deleted(self):
        # for backward compatibility
        return self.inactive

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        #  check if the person is already a student
        # if Student.objects.filter(id=self.id).count():
        #    raise ValidationError("cannot have a someone be a student and a Teacher")
        # create username
        username = self.first_name + self.last_name
        self.username = username
        # save model
        super(Teacher, self).save()

        # create a user with default password as firstname and lastname
        user, created = CustomUser.objects.get_or_create(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            is_teacher=self.isTeacher,
        )
        if created:
            password = "Complex." + str(self.empId[4:])
            user.set_password(password)
            user.save()
            # send the username and password to email
            msg = (
                "\nHey {} Welcome to {}, your username is {} and the default one time password is {}"
                "Please login to your portal and change the password.."
                "This password is valid for 24 hours only".format(
                    (str(self.first_name) + str(self.last_name)),
                    "this school ",
                    self.email,
                    user.password,
                )
            )
            # mail_agent(self.alt_email, "Default user Name and password", msg)

        # add the user to a Group
        group, gcreated = Group.objects.get_or_create(name="teacher")
        if gcreated:
            group.save()
        user.groups.add(group)
        user.save()


class ClassLevel(models.Model):
    id = models.IntegerField(unique=True, primary_key=True, verbose_name="Class Level")
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name


class GradeLevel(models.Model):
    id = models.IntegerField(unique=True, primary_key=True, verbose_name="Grade Level")
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name


class ClassYear(models.Model):
    """Class year such as class of 2019"""

    year = models.CharField(max_length=100, unique=True, help_text="Example 2020")
    full_name = models.CharField(
        max_length=255, help_text="Example Class of 2020", blank=True
    )

    def __str__(self):
        return self.full_name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.full_name:
            self.full_name = "Class of %s" % (self.year,)
        super(ClassYear, self).save()


class ReasonLeft(models.Model):
    reason = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.reason


class Stream(models.Model):
    name = models.CharField(max_length=50, validators=[stream_validator])

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    name = models.ForeignKey(
        ClassLevel, on_delete=models.CASCADE, blank=True, related_name="class_level"
    )
    stream = models.ForeignKey(
        Stream, on_delete=models.CASCADE, blank=True, related_name="class_stream"
    )
    class_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True)
    grade_level = models.ForeignKey(
        GradeLevel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="the grade level of the class ie: 'form one is in Grade one' ",
    )
    capacity = models.IntegerField(
        help_text="Enter total number of sits default is set to 25",
        default=40,
        blank=True,
    )
    occupied_sits = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        unique_together = ["name", "stream"]

    def __str__(self):
        if self.stream:
            return "{} {}".format(self.name, str(self.stream))
        else:
            return self.name

    def available_sits(self):
        open_sits = self.capacity - self.occupied_sits
        return open_sits

    def class_status(self):
        # get the percentage of occupied sits
        percentage = (self.occupied_sits / self.capacity) * 100
        return "{}%".format(float(percentage))

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Before we Save any data in the class room lets check to see if there are open sits

        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        if (self.capacity - self.occupied_sits) < 0:
            raise ValueError(
                "all sits in this classroom are occupied try other classes"
            )
        else:
            super(ClassRoom, self).save()


class SubjectAllocation(models.Model):
    """
    A model to allocate subjects to respective teacher t the school
    """

    teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="allocated_subjects"
    )
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term = models.CharField(max_length=10, choices=ACADEMIC_TERM, blank=True, null=True)
    class_room = models.ForeignKey(
        ClassRoom, on_delete=models.CASCADE, related_name="subjects"
    )

    def __str__(self):
        return str(self.teacher_name)

    def subjects_data(self):
        for data in self.subjects.all():
            return data


class Parent(models.Model):
    first_name = models.CharField(
        max_length=300, verbose_name="First Name", blank=True, null=True
    )
    middle_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Middle Name"
    )
    last_name = models.CharField(
        max_length=300, verbose_name="Last Name", blank=True, null=True
    )
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICE, blank=True, null=True
    )
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    parent_type = models.CharField(
        choices=PARENT_CHOICE, max_length=10, blank=True, null=True
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(
        max_length=150, unique=True, help_text="personal phone number"
    )
    national_id = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(
        max_length=255, blank=True, null=True, help_text="current occupation"
    )
    monthly_income = models.FloatField(
        help_text="parents average monthly income", blank=True, null=True
    )
    single_parent = models.BooleanField(
        default=False, blank=True, help_text="is he/she a single parent"
    )
    alt_email = models.EmailField(blank=True, null=True, help_text="personal Email ")
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="Parent_images", blank=True)
    inactive = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super(Parent, self).save()

        # create a user and password
        user, created = CustomUser.objects.get_or_create(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            is_parent=True,
        )
        if created:
            password = str(self.first_name) + str(self.last_name)
            user.set_password(password)
            user.save()

        # lets create a student group or add to an existing one
        group, gcreated = Group.objects.get_or_create(name="parent")
        if gcreated:
            group.save()
        user.groups.add(group)
        user.save()


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150, null=True, verbose_name="First Name")
    middle_name = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Middle Name"
    )
    last_name = models.CharField(max_length=150, null=True, verbose_name="Last Name")
    graduation_date = models.DateField(blank=True, null=True)
    grade_level = models.ForeignKey(
        GradeLevel, blank=True, null=True, on_delete=models.SET_NULL
    )
    class_of_year = models.ForeignKey(
        ClassYear, blank=True, null=True, on_delete=models.SET_NULL
    )
    date_dismissed = models.DateField(blank=True, null=True)
    reason_left = models.ForeignKey(
        ReasonLeft, blank=True, null=True, on_delete=models.SET_NULL
    )
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICE, blank=True, null=True
    )
    religion = models.CharField(
        max_length=50, choices=RELIGION_CHOICE, blank=True, null=True
    )
    region = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    parent_guardian = models.ForeignKey(
        Parent, on_delete=models.CASCADE, blank=True, null=True, related_name="child"
    )
    parent_contact = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True)
    admission_date = models.DateTimeField(auto_now_add=True)
    admission_number = models.CharField(max_length=50, blank=True, unique=True)
    prem_number = models.CharField(max_length=50, blank=True)
    siblings = models.ManyToManyField("Student", blank=True)
    image = models.ImageField(upload_to="StudentsImages", blank=True)

    cache_gpa = models.DecimalField(
        editable=False, max_digits=5, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_year(self, active_year):
        """get the year (fresh, etc) from the class of XX year"""

        if self.class_of_year:
            try:
                this_year = active_year.end_date.year
                school_last_year = GradeLevel.objects.oder_by("-id")[0].id
                class_of_year = self.class_of_year.unique_for_year

                target_year = school_last_year - (class_of_year - this_year)
                return GradeLevel.objects.get(id=target_year)
            except:
                return None

    def determine_year(self):
        """Set the year (fresh, etc) from class XX year"""

        if self.class_of_year:
            try:
                active_year = AcademicYear.objects.filter(active_year=True)[0]
                self.year = self.get_year(active_year)
            except:
                return None

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        # create prent from student data
        parent, created = Parent.objects.get_or_create(
            phone_number=self.parent_contact,
            email="mzaziwa" + str(self.first_name) + str(self.last_name) + "@hic.com",
            first_name=self.middle_name,
            last_name=self.last_name,
        )
        if created:
            parent.save()

        self.parent_guardian = parent
        super(Student, self).save()

    """
	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

		# 1. Check if there is a staff with the same id as student
		if Teacher.objects.filter(id=self.id).count():
			raise ValidationError('Cannot have someone be a student and a Staff')

		#self.admission_number = assign_admission_numbers()
		self.determine_year()

		super(Student, self).save()
		user, created = User.objects.get_or_create(username=self.username)
		if created:
			# if a user is created give the user a default password
			user.password = (str(self.first_name) + str(self.middle_name))
			user.save()

		# lets create a student group or add to an existing one
		group, gcreated = Group.objects.get_or_create(name="students")
		if gcreated:
			group.save()
		user.groups.add(group)
		user.save() 
		

    def clean(self):
        
        # Check if a Faculty exists, cant have someone be a student and faculty
        if Teacher.objects.filter(id=self.id).count():
            raise ValidationError("Cannot have someone be a student AND faculty!")
        super(Student, self).clean()
    """

    def graduate_and_create_alumni(self):
        self.inactive = True

        self.reason_left = ReasonLeft.objects.get_or_create(reason="Graduated")[0]
        if not self.graduation_date:
            self.graduation_date = date.today()

        # register student as Alumni
        # noinspection PyUnresolvedReferences
        # from alumni.models import Alumni
        # Alumni.objects.get_or_create(student=self)
        self.save()


class StudentClass(models.Model):
    """
    This is a bridge table to link a student to a class
    when you add a student to a class we update the selected class capacity

    """

    classroom = models.ForeignKey(
        ClassRoom, on_delete=models.CASCADE, related_name="class_student"
    )
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    student_id = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="student_class"
    )

    @property
    def is_current_class(self):
        if self.academic_year.is_current_session:
            return True
        return False

    def __str__(self):
        return str(self.student_id)

    def update_class_table(self):
        selected_class = ClassRoom.objects.get(pk=self.classroom.pk)
        new_value = selected_class.occupied_sits + 1
        selected_class.occupied_sits = new_value
        selected_class.save()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        # lets update the class sits

        self.update_class_table()
        super(StudentClass, self).save()


class StudentsMedicalHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    history = models.TextField()
    file = models.FileField(upload_to="students_medical_files", blank=True, null=True)

    def __str__(self):
        return str(self.student)


class StudentsPreviousAcademicHistory(models.Model):
    students_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    former_school = models.CharField(max_length=255, help_text="Former school name")
    last_gpa = models.FloatField()
    notes = models.CharField(
        max_length=255,
        blank=True,
        help_text="Indicate students academic performance according to your observation",
    )
    academic_record = models.FileField(
        upload_to="students_former_academic_files", blank=True
    )

    def __str__(self):
        return str(self.students_name)


class GradeScale(models.Model):
    """Translate a numeric grade to some other scale.
    Example: Letter grade or 4.0 scale."""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "{}".format(self.name)

    def get_rule(self, grade):
        if grade is not None:
            return self.gradescalerule_set.filter(
                min_grade__lte=grade, max_grade__gte=grade
            ).first()

    def to_letter(self, grade):
        rule = self.get_rule(grade)
        if rule:
            return rule.letter_grade

    def to_numeric(self, grade):
        rule = self.get_rule(grade)
        if rule:
            return rule.numeric_scale


class GradeScaleRule(models.Model):
    """One rule for a grade scale."""

    min_grade = models.DecimalField(max_digits=5, decimal_places=2)
    max_grade = models.DecimalField(max_digits=5, decimal_places=2)
    letter_grade = models.CharField(max_length=50, blank=True, null=True)
    numeric_scale = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    grade_scale = models.ForeignKey(GradeScale, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("min_grade", "max_grade", "grade_scale")

    def __str__(self):
        return f"{self.min_grade}-{self.max_grade} {self.letter_grade} {self.numeric_scale}"


# def get_default_benchmark_grade():
#    return str(Configuration.get_or_default("Benchmark-based grading", "False").value).lower() == "true"
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    gpa = models.FloatField(null=True)
    cat_gpa = models.FloatField(null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term = models.CharField(max_length=10, choices=ACADEMIC_TERM, blank=True, null=True)

    def __str__(self):
        return str(self.student)


class Dormitory(models.Model):
    name = models.CharField(max_length=150)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    occupied_beds = models.IntegerField(blank=True, null=True)
    captain = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name

    def available_beds(self):
        total = self.capacity - self.occupied_beds
        if total <= 0:
            return "all beds in {} are occupied".format(self.name)

        else:
            return total

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if (self.capacity - self.occupied_beds) <= 0:
            raise ValueError(
                "all beds in {} are occupied:\n please add more beds or save to another dormitory".format(
                    self.name
                )
            )
        else:
            super(Dormitory, self).save()


class DormitoryAllocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE)
    date_from = models.DateField(auto_now_add=True)
    date_till = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.student.admission_number)

    def update_dormitory(self):
        """
        update the capacity of each dorm
        :return:
        """
        selected_dorm = Dormitory.objects.get(pk=self.dormitory.pk)
        new_capacity = selected_dorm.occupied_beds + 1
        selected_dorm.occupied_beds = new_capacity
        selected_dorm.save()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.update_dormitory()
        super(DormitoryAllocation, self).save()


class ExaminationListHandler(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    ends_date = models.DateField()
    out_of = models.IntegerField()
    # academic_term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='academic_term_exam')
    classrooms = models.ManyToManyField(ClassRoom, related_name="class_exams")
    comments = models.CharField(
        max_length=200, blank=True, null=True, help_text="Comments Regarding Exam"
    )
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def status(self):
        if datetime.now().date() > self.start_date:
            return "Done"
        elif self.start_date >= datetime.now().date() >= self.ends_date:
            return "on going"
        return "Coming up"

    def __str__(self):
        return self.name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super(ExaminationListHandler, self).save()


class MarksManagement(models.Model):
    exam_name = models.ForeignKey(
        ExaminationListHandler, on_delete=models.CASCADE, related_name="exam_marks"
    )
    points_scored = models.FloatField()
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="subject_marks"
    )
    student = models.ForeignKey(
        StudentClass, on_delete=models.CASCADE, related_name="student_marks"
    )
    created_by = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="marks_entered"
    )
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.points_scored


'''
class TranscriptNoteChoice(models.Model):
	"""
	Returns a predefined transcript note.
	when displayed from 'TranscriptNote':
	replaces $student with student name
	Replaces $he_she with students appropriate gender word
	"""

	note = models.TextField()

	def __str__(self):
		return self.note

class TranscriptNote(models.Model):
	""" These are notes intended to be shown on a transcript. They may be either free
		text or a predefined choice. If both are entered they will be concatenated.
		"""

	note = models.TextField(blank=True)
	predefined_note = models.ForeignKey(TranscriptNoteChoice, blank=True, null=True, on_delete=models.SET_NULL)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.student)
'''


class StudentFile(models.Model):
    file = models.FileField(upload_to="student_files")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student)


class StudentHealthRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    record = models.TextField()

    def __str__(self):
        return str(self.student)


class MessageToParent(models.Model):
    """Store a message to be shown to parents for a specific amount of time"""

    message = models.TextField(
        help_text="this message will be shown to Parents when they log in"
    )
    start_date = models.DateField(
        default=timezone.now,
        help_text="If blank the message will be posted starting today",
    )
    end_date = models.DateField(
        default=timezone.now, help_text="if blank the message will end today"
    )

    def __str__(self):
        return self.message


class MessageToTeacher(models.Model):
    """Stores a message to be shown to Teachers for a specific amount of time"""

    message = models.TextField(
        help_text="This message will be shown to teachers when they log in."
    )
    start_date = models.DateField(
        default=timezone.now,
        help_text="If blank the message will be posted starting today",
    )
    end_date = models.DateField(
        default=timezone.now, help_text="if blank the message will end today"
    )

    def __str__(self):
        return self.message


class FamilyAccessUser(CustomUser):
    """A person who can log into the non-admin side and see the same view as a student,
    except that he/she cannot submit timecards.
    This proxy model allows non-superuser registrars to update family user accounts.
    """

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        super(FamilyAccessUser, self).save()
        self.groups.add(Group.objects.get_or_create(name="family")[0])
