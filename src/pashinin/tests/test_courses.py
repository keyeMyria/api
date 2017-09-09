import pytest


@pytest.mark.urls('pashinin.urls')
def test_CourseView_some_courses(admin_client, db):
    from pashinin.models import Course
    # from core import now
    assert Course.objects.filter().count() == 0
    Course.objects.create(
        slug='python-base',
        # start=now(),
        # end=now()
    )
    assert Course.objects.filter().count() > 0
    r = admin_client.get('/courses/python-base')
    assert r.status_code == 200

    # no such course
    r = admin_client.get('/courses/00000000')
    assert r.status_code == 404
