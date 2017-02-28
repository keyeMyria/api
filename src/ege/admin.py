from django.contrib import admin
from .models import Subject, Exam, Task
from django.utils.translation import ugettext_lazy as _
# from adminfilters.models import Species, Breed


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
    make_published.short_description = _("Published")


def unpublish(modeladmin, request, queryset):
    queryset.update(published=False)
    make_published.short_description = _("Hide")+" (published=False)"


# admin.site.register(Task)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'published')
    list_filter = ('published', )
    ordering = ['-published', 'name']
    actions = [unpublish, make_published]


class MembershipInline(admin.TabularInline):
    model = Task
    # show_change_link = True
    extra = 0
    # model = Exam.tasks.through


# class SubjectsListFilter(admin.SimpleListFilter):

#     """
#     This filter will always return a subset of the instances in a Model, either filtering by the
#     user choice or by a default value.
#     """
#     # Human-readable title which will be displayed in the
#     # right admin sidebar just above the filter options.
#     title = 'Предмет'

#     # Parameter for the filter that will be used in the URL query.
#     parameter_name = 'subjects'

#     default_value = None

#     def lookups(self, request, model_admin):
#         """
#         Returns a list of tuples. The first element in each
#         tuple is the coded value for the option that will
#         appear in the URL query. The second element is the
#         human-readable name for the option that will appear
#         in the right sidebar.
#         """
#         list_of_species = []
#         queryset = Subject.objects.filter(published=True)
#         for species in queryset:
#             list_of_species.append(
#                 (str(species.id), species.name)
#             )
#         return sorted(list_of_species, key=lambda tp: tp[1])

#     def queryset(self, request, queryset):
#         """
#         Returns the filtered queryset based on the value
#         provided in the query string and retrievable via
#         `self.value()`.
#         """
#         # Compare the requested value to decide how to filter the queryset.
#         if self.value():
#             return queryset.filter(subject=self.value())
#         return queryset

#     def value(self):
#         """
#         Overriding this method will allow us to always have a default value.
#         """
#         value = super(SubjectsListFilter, self).value()
#         if value is None:
#             if self.default_value is None:
#                 # If there is at least one Species, return the first by name. Otherwise, None.
#                 first_species = Species.objects.order_by('name').first()
#                 value = None if first_species is None else first_species.id
#                 self.default_value = value
#             else:
#                 value = self.default_value
#         return str(value)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    # inlines = [
    #     TagInline,
    # ]
    list_filter = ('exam__subject', 'exam__year', )


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
    exclude = ('tasks',)

    list_filter = ('type', )

    fieldsets = (
        (None, {
           'fields': ('published', 'type', 'subject', 'year')
        }),
        (_('Description'), {
            'fields': ('info', ),
        }),
        # ('Задачи экзамена', {
        #     'fields': ('exam_tasks', ),
        # }),
    )
    # filter_horizontal = ('exam_tasks',)
