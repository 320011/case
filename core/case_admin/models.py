from django.db import models


"""class CaseStudy(models.Model):
    # Processing information and settings
    date_submitted = models.DateTimeField(null=True, blank=True)
    date_last_edited = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    last_edited_user = models.IntegerField(blank=True)
    is_deleted = models.BooleanField(default=False)
    height = models.IntegerField(blank=True)
    weight = models.FloatField(blank=True)
    scr = models.FloatField(blank=True)
    age = models.IntegerField()
    description = models.TextField(help_text='Description for case study scenario.')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_1 = models.TextField(help_text='Answer 1')
    answer_2 = models.TextField(help_text='Answer 2')
    answer_3 = models.TextField(help_text='Answer 3')
    answer_4 = models.TextField(help_text='Answer 4')
    feedback = models.TextField(help_text='Case study creator feedback')"""
