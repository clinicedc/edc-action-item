from django.test import TestCase, tag
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import CLOSED, OPEN, NEW

from ..action import delete_action_item
from ..action import ActionItemDeleteError
from ..models import ActionItem, ActionType
from ..site_action_items import site_action_items
from .action_items import FormOneAction, FormTwoAction, FormThreeAction
from .action_items import SingletonAction, register_actions
from .models import FormOne, SubjectIdentifierModel


class TestAction(TestCase):

    def setUp(self):
        register_actions()
        self.subject_identifier_model = ActionItem.subject_identifier_model
        ActionItem.subject_identifier_model = 'edc_action_item.subjectidentifiermodel'
        self.subject_identifier = '12345'
        SubjectIdentifierModel.objects.create(
            subject_identifier=self.subject_identifier)
        self.assertEqual(0, ActionType.objects.all().count())
        self.assertIn(FormOneAction.name, site_action_items.registry)
        self.assertIn(FormTwoAction.name, site_action_items.registry)
        self.assertIn(FormThreeAction.name, site_action_items.registry)

    def test_reference_model_delete_resets_action_item(self):
        obj = FormOne.objects.create(
            subject_identifier=self.subject_identifier)
        action_item = ActionItem.objects.get(
            action_identifier=obj.action_identifier)
        self.assertEqual(action_item.status, CLOSED)
        obj.delete()
        action_item = ActionItem.objects.get(
            action_identifier=obj.action_identifier)
        self.assertEqual(action_item.status, NEW)
        self.assertFalse(action_item.linked_to_reference)

    def test_delete_singleton(self):
        SingletonAction(
            subject_identifier=self.subject_identifier)
        delete_action_item(
            action_cls=SingletonAction,
            subject_identifier=self.subject_identifier)
        self.assertRaises(
            ObjectDoesNotExist,
            ActionItem.objects.get,
            subject_identifier=self.subject_identifier)

    def test_cannot_delete_if_not_new(self):
        action = SingletonAction(
            subject_identifier=self.subject_identifier)

        action_item = action.action_item_obj

        action_item.status = CLOSED
        action_item.save()
        self.assertRaises(
            ActionItemDeleteError,
            delete_action_item,
            action_cls=SingletonAction,
            subject_identifier=self.subject_identifier)
        action_item.status = OPEN
        action_item.save()
        self.assertRaises(
            ActionItemDeleteError,
            delete_action_item,
            action_cls=SingletonAction,
            subject_identifier=self.subject_identifier)