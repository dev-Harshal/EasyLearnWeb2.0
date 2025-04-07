from django.db import models
from Users.models import User
# Create your models here.

class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    category = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    created_by = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Courses Table'

class Curriculum(models.Model):
    id = models.BigAutoField(primary_key=True)
    course = models.OneToOneField(Course, related_name='curriculum', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Curriculums Table'

class Section(models.Model):
    id = models.BigAutoField(primary_key=True)
    curriculum = models.ForeignKey(Curriculum, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    order = models.PositiveIntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Sections Table'


ITEM_TYPE_CHOICES = (('lesson', 'lesson'), ('quiz', 'quiz'))
class CurriculumItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    section = models.ForeignKey(Section, related_name='curriculum_items', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES, null=False, blank=False)
    order = models.PositiveIntegerField(null=False, blank=False, default=1) 

    class Meta:
        db_table = 'Curriculum Items Table'

class Lesson(models.Model):
    id = models.BigAutoField(primary_key=True)
    curriculum_item = models.OneToOneField(CurriculumItem, related_name='lesson', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    video_file = models.FileField(upload_to='videos/', null=False, blank=False)
    note_file = models.FileField(upload_to='notes/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'Lessons Table'

class Quiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    curriculum_item = models.OneToOneField(CurriculumItem, related_name='quiz', on_delete=models.CASCADE)
    question = models.CharField(max_length=255, null=False, blank=False)
    
    class Meta:
        db_table = 'Quizzes Table'

class QuizOption(models.Model):
    id = models.BigAutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, related_name='quiz_options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=False, blank=False) 
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = 'Quiz Options Table'

class Exam(models.Model):
    id = models.BigAutoField(primary_key=True)
    course = models.OneToOneField(Course, related_name='exam', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Exams Table'

class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=False, blank=False)
    mark = models.PositiveIntegerField(null=False, blank=False, default=0)

    class Meta:
        db_table = 'Questions Table'

class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=100, null=False, blank=False)
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = 'Answers Table'