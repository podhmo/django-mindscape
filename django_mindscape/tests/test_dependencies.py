# -*- coding:utf-8 -*-
import unittest
from evilunit import test_target


@test_target("django_mindscape:Walker")
class _ForeignKeyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from django.db import models

        class _Group(models.Model):
            name = models.CharField(max_length=255, null=False, default="")

            class Meta:
                app_label = "myapp"

        class _Member(models.Model):
            group = models.ForeignKey(_Group, related_name="member_set")
            name = models.CharField(max_length=255, null=False, default="")

            class Meta:
                app_label = "myapp"

        cls._Group = _Group
        cls._Member = _Member

    def _get_models(self):
        return [self._Group, self._Member]

    def test_dependecies__member(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        member_dependencies = [node.to.model for node in walker[self._Member].dependencies]
        self.assertEqual(member_dependencies, [self._Group])

    def test_dependecies__group(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        self.assertEqual(walker[self._Group].dependencies, [])

    def test_relation_type(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        reltype = walker[self._Member].dependencies[0].type
        self.assertEqual(reltype, "M1")

    def test_relation_name(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        name = walker[self._Member].dependencies[0].name
        self.assertEqual(name, "group")

    def test_relation_backref(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        backref = walker[self._Member].dependencies[0].backref
        self.assertEqual(backref, "member_set")

    def test_relation_fkname(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        fkname = walker[self._Member].dependencies[0].fkname
        self.assertEqual(fkname, "group_id")


@test_target("django_mindscape:Walker")
class _RelatedNameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from django.db import models

        class _Group(models.Model):
            name = models.CharField(max_length=255, null=False, default="")

            class Meta:
                app_label = "myappp"

        class _Member(models.Model):
            group = models.ForeignKey(_Group, related_name="+")
            name = models.CharField(max_length=255, null=False, default="")

            class Meta:
                app_label = "myappp"

        cls._Group = _Group
        cls._Member = _Member

    def _get_models(self):
        return [self._Group, self._Member]

    def test_relation_name(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        name = walker[self._Member].dependencies[0].name
        self.assertEqual(name, "group")

    def test_relation_backref(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        backref = walker[self._Member].dependencies[0].backref
        self.assertEqual(backref, None)


@test_target("django_mindscape:Walker")
class _ManyToManyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from django.db import models

        class _Group(models.Model):
            name = models.CharField(max_length=255, null=False, default="")

        class Meta:
            app_label = "myapp2"

        class _Member(models.Model):
            group_set = models.ManyToManyField(_Group, through="_GroupTo_Member", related_name="member_set")
            name = models.CharField(max_length=255, null=False, default="")

            class Meta:
                app_label = "myapp2"

        class _GroupTo_Member(models.Model):
            member = models.ForeignKey(_Member)
            group = models.ForeignKey(_Group)

            class Meta:
                app_label = "myapp2"

        cls._Group = _Group
        cls._Member = _Member
        cls._GroupTo_Member = _GroupTo_Member

    def _get_models(self):
        return [self._Group, self._Member]

    def test_get_relation(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()
        relations = walker[self._Member].dependencies
        self.assertNotEqual(len(relations), 0)

    @unittest.skip("hmm")
    def test_get_relation__reverse(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()
        relations = walker[self._Group].dependencies
        self.assertNotEqual(len(relations), 0)

    def test_relation_type(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()
        reltype = walker[self._Member].dependencies[0].type
        self.assertEqual(reltype, "MM")

    def test_relation_name(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        name = walker[self._Member].dependencies[0].name
        self.assertEqual(name, "group_set")

    def test_relation_backref(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        backref = walker[self._Member].dependencies[0].backref
        self.assertEqual(backref, "member_set")

    def test_relation_through(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        through = walker[self._Member].dependencies[0].through
        self.assertEqual(through.model, self._GroupTo_Member)

    def test_relation_fkname(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        fkname = walker[self._Member].dependencies[0].fkname
        self.assertEqual(fkname, "group_set_id")


@test_target("django_mindscape:Walker")
class _OneToOneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from django.db import models

        class _Group(models.Model):
            name = models.CharField(max_length=255, null=False, default="")

            class Meta:
                app_label = "myapp3"

        class _Member(models.Model):
            group = models.OneToOneField(_Group, related_name="member")
            name = models.CharField(max_length=255, null=False, default="")

            class Meta:
                app_label = "myapp3"

        cls._Group = _Group
        cls._Member = _Member

    def _get_models(self):
        return [self._Group, self._Member]

    def test_relation_type(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()
        reltype = walker[self._Member].dependencies[0].type
        self.assertEqual(reltype, "11")

    def test_relation_name(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        name = walker[self._Member].dependencies[0].name
        self.assertEqual(name, "group")

    def test_relation_backref(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        backref = walker[self._Member].dependencies[0].backref
        self.assertEqual(backref, "member")

    def test_relation_fkname(self):
        walker = self._makeOne(self._get_models())
        walker.walkall()

        fkname = walker[self._Member].dependencies[0].fkname
        self.assertEqual(fkname, "group_id")
