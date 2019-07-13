import logging

from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.management.color import color_style
from django.db.models import Q
from django.utils.formats import localize
from edc_model.constants import DEFAULT_BASE_FIELDS
from edc_constants.constants import CLOSED, NEW, OPEN

from .create_action_item import SingletonActionItemError
from .create_action_item import create_action_item
from .get_action_type import get_action_type
from .site_action_items import site_action_items

logger = logging.getLogger(__name__)
style = color_style()

REFERENCE_MODEL_ERROR_CODE = "reference_model"


class ActionError(ValidationError):
    pass


class RelatedReferenceObjectDoesNotExist(ObjectDoesNotExist):
    pass


class Action:

    admin_site_name = None
    color_style = "danger"
    create_by_action = None
    create_by_user = None
    display_name = None
    help_text = None
    instructions = None
    name = None
    parent_action_names = None
    enforce_parent_action_names = True
    priority = None
    reference_model = None
    related_reference_fk_attr = None
    related_reference_model = None
    show_link_to_add = False
    show_link_to_changelist = False
    show_on_dashboard = None
    singleton = False
    delete_with_reference_object = False

    action_item_model = "edc_action_item.actionitem"
    action_type_model = "edc_action_item.actiontype"
    next_actions = None  # a list of Action classes which may include 'self'

    def __init__(
        self,
        action_item=None,
        reference_obj=None,
        subject_identifier=None,
        action_identifier=None,
        parent_action_item=None,
        related_action_item=None,
        using=None,
        readonly=None,
    ):

        self._action_item = action_item
        self._reference_obj = reference_obj

        self.parent_action_names = self.parent_action_names or []

        self.messages = {}

        self.action_identifier = action_identifier
        self.parent_action_item = parent_action_item
        self.related_action_item = related_action_item
        self.readonly = readonly
        self.subject_identifier = subject_identifier
        self.using = using

        if self.action_item.action_cls != self.__class__:
            raise ActionError(
                f"Action class mismatch for given ActionItem. "
                f"{self.action_item.action_cls} incorrectly passed "
                f"to Action {self.__class__}",
                code="class type mismatch",
            )
        self.action_identifier = self.action_item.action_identifier
        self.linked_to_reference = self.action_item.linked_to_reference
        self.parent_action_item = self.action_item.parent_action_item
        self.related_action_item = self.action_item.related_action_item
        if not self.subject_identifier:
            self.subject_identifier = self.action_item.subject_identifier

        if (
            self.enforce_parent_action_names
            and self.parent_action_item
            and self.parent_action_item.action_cls.name not in self.parent_action_names
        ):
            raise ActionError(
                f"Action class received an unlisted parent_action_item. "
                f"Expected one of {self.parent_action_names}. "
                f"Got '{self.parent_action_item.action_cls.name}'. "
                f"See Action {self.__class__}."
            )
        if not self.related_action_item and self.related_reference_fk_attr:
            raise ActionError(
                "Action class expects a related_action_item. "
                f"related_reference_fk_attr={self.related_reference_fk_attr}. "
                f"Got None for action based on action_item {self.action_item}. "
                f"See {repr(self)}"
            )

        if self.reference_obj and not self.readonly:
            self.close_and_create_next()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def __str__(self):
        return self.name

    def get_color_style(self):
        return self.color_style

    def get_display_name(self):
        return self.action_item.action_type.display_name

    @property
    def reference_obj(self):
        """Returns the reference model instance or None.

        If the reference model instance "should" exist,
        raise an exception. That is; action_identifier already
        allocated, action item exists and is CLOSED.
        """
        if not self._reference_obj:
            try:
                self._reference_obj = (
                    self.reference_model_cls()
                    .objects.using(self.using)
                    .get(action_identifier=self.action_identifier)
                )
            except ObjectDoesNotExist:
                if (
                    self.action_identifier
                    and self.action_item
                    and self.action_item.status == CLOSED
                ):
                    raise ActionError(
                        "Reference model instance not found. "
                        f"Got action_identifier='{self.action_identifier}' "
                        f"for reference_model "
                        f"'{self.reference_model}'. See {repr(self)}",
                        code=REFERENCE_MODEL_ERROR_CODE,
                    )
        return self._reference_obj

    @property
    def action_item(self):
        """Returns an action_item model instance.

        If necessary, create.
        """
        if not self._action_item:
            if self.action_identifier:
                self._action_item = (
                    self.action_item_model_cls()
                    .objects.using(self.using)
                    .get(action_identifier=self.action_identifier)
                )
            elif self.reference_obj:
                self._action_item = self.reference_obj.action_item
            else:
                opts = dict(
                    subject_identifier=self.subject_identifier,
                    action_type=get_action_type(self.__class__),
                    related_action_item=self.related_action_item,
                    status=NEW,
                )
                try:
                    self._action_item = (
                        self.action_item_model_cls()
                        .objects.using(self.using)
                        .get(**opts)
                    )
                except ObjectDoesNotExist:
                    try:
                        self._action_item = create_action_item(
                            self.__class__,
                            parent_action_item=self.parent_action_item,
                            using=self.using,
                            **opts,
                        )
                    except SingletonActionItemError:
                        self._action_item = (
                            self.action_item_model_cls()
                            .objects.using(self.using)
                            .get(
                                subject_identifier=self.subject_identifier,
                                action_type=get_action_type(self.__class__),
                            )
                        )
                except MultipleObjectsReturned:
                    self._action_item = (
                        self.action_item_model_cls()
                        .objects.using(self.using)
                        .filter(**opts)
                        .order_by("created")[0]
                    )
            if not self._action_item:
                opts = dict(
                    reference_obj=self.reference_obj,
                    subject_identifier=self.subject_identifier,
                    action_identifier=self.action_identifier,
                    parent_action_item=self.parent_action_item,
                    related_action_item=self.related_action_item,
                )
                raise ActionError(f"Unable to get or create ActionItem. Got {opts}.")
        return self._action_item

    @classmethod
    def action_item_model_cls(cls):
        """Returns the ActionItem model class.
        """
        return django_apps.get_model(cls.action_item_model)

    @classmethod
    def action_type_model_cls(cls):
        """Returns the ActionType model class.
        """
        return django_apps.get_model(cls.action_type_model)

    @classmethod
    def reference_model_cls(cls):
        """Returns the reference model class.
        """
        return django_apps.get_model(cls.reference_model)

    @classmethod
    def related_reference_model_cls(cls):
        """Returns the related reference model class
        """
        return django_apps.get_model(cls.related_reference_model)

    @classmethod
    def as_dict(cls):
        """Returns select class attrs as a dictionary.
        """
        dct = {k: v for k, v in cls.__dict__.items() if not k.startswith("_")}
        try:
            dct.update(reference_model=cls.reference_model.lower())
        except AttributeError:
            pass
        try:
            dct.update(related_reference_model=cls.related_reference_model.lower())
        except AttributeError:
            pass
        dct.update(
            name=cls.name,
            display_name=cls.display_name,
            show_on_dashboard=(
                True if cls.show_on_dashboard is None else cls.show_on_dashboard
            ),
            show_link_to_changelist=(
                True
                if cls.show_link_to_changelist is None
                else cls.show_link_to_changelist
            ),
            create_by_user=(True if cls.create_by_user is None else cls.create_by_user),
            create_by_action=(
                True if cls.create_by_action is None else cls.create_by_action
            ),
            instructions=cls.instructions,
        )
        return dct

    def get_next_actions(self):
        """Returns a list of action classes to be created
        again by this model if the first has been closed on post_save.
        """
        return self.next_actions or []

    def close_action_item_on_save(self):
        """Returns True if action item for \'action_identifier\'
        is to be closed on post_save.

        Note: post_save watches the reference model instance.
        """
        return True

    def close_and_create_next(self):
        """Attempt to close the action item and
        create new ones, if required.
        """
        if self.reference_obj_has_changed:
            self.reopen_action_items()
        status = CLOSED if self.close_action_item_on_save() else OPEN
        if self.action_item.status != status:
            self.action_item.status = status
            self.action_item.save(using=self.using)
            self.action_item.refresh_from_db(using=self.using)
        if status == CLOSED:
            self.create_next_action_items()

    def create_next_action_items(self):
        """Creates any next action items if they do not
        already exist.
        """
        next_actions = list(set(self.get_next_actions()))
        for action_name in next_actions:
            action_cls = (
                self.__class__
                if action_name == "self"
                else site_action_items.get(action_name)
            )
            action_type = get_action_type(action_cls)
            if action_type.related_reference_model:
                related_action_item = (
                    self.action_item.related_action_item or self.action_item
                )
            else:
                related_action_item = None
            action_cls(
                subject_identifier=self.subject_identifier,
                parent_action_item=self.action_item,
                related_action_item=related_action_item,
                using=self.using,
            )

    def reopen_on_change(self):
        """May be overriden."""
        return not self.close_action_item_on_save()

    def reopen_action_items(self):
        """Reopens the action_item and child action items for this
        reference object if reference object was changed since
        the last save.
        """
        for action_item in (
            self.action_item_model_cls()
            .objects.using(self.using)
            .filter(
                (
                    Q(action_identifier=self.reference_obj.action_identifier)
                    | Q(
                        parent_action_item__action_identifier=(
                            self.reference_obj.action_identifier
                        )
                    )
                    | Q(related_action_item=self.reference_obj.action_item)  # noqa
                ),
                status=CLOSED,
            )
        ):
            if self.reopen_on_change():
                action_item.status = OPEN
                action_item.save(using=self.using)
                self.messages.update(
                    {
                        action_item: (
                            f"{self.reference_obj._meta.verbose_name.title()} "
                            f"{self.reference_obj} was changed on "
                            f"{localize(self.reference_obj.modified)} "
                            f"({settings.TIME_ZONE})"
                        )
                    }
                )

    @property
    def reference_obj_has_changed(self):
        """Returns True if the reference object has changed
        since the last save.

        Reviews the objects "history" (historical) instances.
        """
        changed_message = {}
        try:
            history = (
                self.reference_obj.history.using(self.using)
                .all()
                .order_by("-history_date")[1]
            )
        except IndexError:
            pass
        except AttributeError:
            # suppressed here but is reviewed in system checks
            pass
        else:
            # TODO: use historical record's diff??
            field_names = [
                field.name
                for field in self.reference_obj._meta.get_fields()
                if field.name not in DEFAULT_BASE_FIELDS
            ]
            for field_name in field_names:
                try:
                    if getattr(history, field_name) != getattr(
                        self.reference_obj, field_name
                    ):
                        changed_message.update(
                            {field_name: getattr(self.reference_obj, field_name)}
                        )
                except AttributeError:
                    pass
        return changed_message

    def append_to_next_if_required(
        self, next_actions=None, action_cls=None, action_name=None, required=None
    ):
        """Returns next actions where the given action_cls.name is
        appended if required.

        `required` can be anything that evaluates to a boolean.

        Will not append if the ActionItem for the next action
        already exists.
        """
        try:
            action_name = action_cls.name
        except AttributeError:
            pass
        next_actions = next_actions or []
        required = True if required is None else required
        opts = dict(
            subject_identifier=self.subject_identifier,
            parent_action_item__action_identifier=self.action_identifier,
            action_type__name=action_name,
        )
        try:
            next_action_item = (
                self.action_item_model_cls().objects.using(self.using).get(**opts)
            )
        except ObjectDoesNotExist:
            next_action_item = None
        except MultipleObjectsReturned:
            # suggests the action item sequence is broken
            logger.warning(
                style.ERROR(
                    f"skipping 'append_to_next_if_required' for "
                    f"{self.action_identifier} next actions. "
                    f"You may wish to review this action item.\n"
                )
            )
            next_action_item = None
        if not next_action_item and required:
            next_actions.append(action_name)
        return next_actions

    def delete_children_if_new(self, parent_action_item=None):
        """Deletes the action item instance where status
        is NEW, use with caution.

        Since some actions are created by an event, this method
        could mess up the state.
        """
        index = 0
        opts = dict(
            subject_identifier=self.subject_identifier,
            parent_action_item=parent_action_item,
            status=NEW,
        )
        for index, obj in enumerate(
            self.action_item_model_cls().objects.using(self.using).filter(**opts)
        ):
            obj.delete(using=self.using)
        return index
