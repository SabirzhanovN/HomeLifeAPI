from django.contrib import admin

from .models import GradeDescription, Review, Reply

admin.site.register(GradeDescription)
admin.site.register(Review)
admin.site.register(Reply)