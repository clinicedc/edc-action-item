from django_collect_offline.site_offline_models import site_offline_models

site_offline_models.register_for_app(
    'edc_action_item',
    exclude_models=[
        'edc_action_item.subjectidentifiermodel',
        'edc_action_item.TestModelWithoutMixin',
        'edc_action_item.TestModelWithActionDoesNotCreateAction',
        'edc_action_item.formzero',
        'edc_action_item.formone',
        'edc_action_item.formtwo',
        'edc_action_item.formthree',
        'edc_action_item.initial',
        'edc_action_item.followup',
        'edc_action_item.appointment',
        'edc_action_item.subjectvisit',
        'edc_action_item.crfone',
        'edc_action_item.crftwo',
        'edc_action_item.testmodelwithaction'])