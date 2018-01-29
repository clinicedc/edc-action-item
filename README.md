# edc-action-items

[![Build Status](https://travis-ci.org/botswana-harvard/edc-action-item.svg?branch=develop)](https://travis-ci.org/botswana-harvard/edc-action-item) [![Coverage Status](https://coveralls.io/repos/github/botswana-harvard/edc-action-item/badge.svg?branch=develop)](https://coveralls.io/github/botswana-harvard/edc-action-item?branch=develop)


Add subject related action items to the Edc.

Action items are reminders. Usually a form needs to be completed based on some clinical condition or event. Action items have a unique `action_identifier` and status (New, Open, Closed). Actions can be configured to create `next` actions. An action is most useful when linked to the completion of a form.

For example, with Adverse Events where the event must be reported at the time of the event and then more data follows in subsequent reports. See mosule `ambition-ae.action_items` for examples. 

Define an `action_item` module. In it define actions using the `Action` class.

    from edc_action_item import Action, site_action_items
    from ambition_ae.action_items import AeFollowupAction, AeTmgAction

    class AeInitialAction(Action):
    
        name = AE_INITIAL_ACTION
        display_name = 'Submit AE Initial Report'
        model = 'ambition_ae.aeinitial'
        show_on_dashboard = True
        instructions = 'Complete the initial report and forward to the TMG'
        priority = HIGH_PRIORITY
        next_actions = [AeFollowupAction, AeTmgAction]
        
`next_actions` may be conditional. If so just override `get_next_actions`:
    
    class AeInitialAction(Action):
    
        name = AE_INITIAL_ACTION
        display_name = 'Submit AE Initial Report'
        model = 'ambition_ae.aeinitial'
        show_on_dashboard = True
        instructions = 'Complete the initial report and forward to the TMG'
        priority = HIGH_PRIORITY

        def get_next_actions(self):
            next_actions = [
                AeFollowupAction, AeTmgAction, RecurrenceOfSymptomsAction]
            try:
                self.action_item_model_cls().objects.get(
                    subject_identifier=self.model_obj.subject_identifier,
                    parent_reference_identifier=self.model_obj.tracking_identifier,
                    reference_model=AeTmgAction.model)
            except ObjectDoesNotExist:
                pass
            else:
                index = next_actions.index(AeTmgAction)
                next_actions.pop(index)
            if self.model_obj.ae_cm_recurrence != YES:
                index = next_actions.index(RecurrenceOfSymptomsAction)
                next_actions.pop(index)
            return next_actions


Register the Action:
    
    site_action_items.register(AeInitialAction)
 