from django.test import TestCase
from case_study.models import *
from accounts.models import *
from case_admin.views.common import *
from case_admin.views import tag


# Create your tests here.
class AdminTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(pk=1, name="test_tag")
        CaseStudy.objects.create(pk=1, case_state=CaseStudy.STATE_REVIEW)
        User.objects.create(is_active=False)

    def tearDown(self):
        Tag.objects.all().delete()
        CaseStudy.objects.all().delete()
        User.objects.all().delete()

    def test_populate_data(self):
        data = populate_data(tag.schema_tag, Tag.objects.all())
        self.assertEqual(len(data["entities"]), 1)
        good_data = {
            'endpoint': '/caseadmin/tags/',
            'entities': [
                [
                    {
                        'entity': 1,
                        'key': 'name',
                        'title': 'Tag',
                        'value': 'test_tag',
                        'widget': {'maxlength': 60, 'template': 'w-text.html'},
                        'write': True
                    }
                ],
            ]
        }
        self.assertEqual(data, good_data)

    def test_patch_model(self):
        class TR:
            pass
        req = TR()
        setattr(req, "body", "{\"name\": \"new_tag\"}")
        patch_model(req, Tag, tag.schema_tag, 1)
        t = Tag.objects.all().first()
        self.assertEqual(t.name, "new_tag")

    def test_delete_model_hard(self):
        class TR:
            pass
        req = TR()
        setattr(req, "body", "{\"hard\": true}")
        self.assertEqual(CaseStudy.objects.all().count(), 1)
        delete_model(req, CaseStudy, 1)
        self.assertEqual(CaseStudy.objects.all().count(), 0)

    def test_get_badge_counts(self):
        bc = get_badge_counts()
        good_bc = {
            "total": 2,
            "users": 1,
            "cases": 1,
            "questions": 0,
            "comments": 0,
            "tags": 0
        }
        self.assertEqual(bc, good_bc)
