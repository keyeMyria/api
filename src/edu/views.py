import logging
from pashinin.views import Base
from .models import Task
# from django.core.urlresolvers import reverse
log = logging.getLogger(__name__)


class Tasks(Base):
    template_name = "edu_tasks.jinja"

    def get_context_data(self, **kwargs):
        c = super(Tasks, self).get_context_data(**kwargs)
        c['tasks'] = Task.objects.all()
        return c
