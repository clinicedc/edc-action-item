from edc_identifier.simple_identifier import SimpleUniqueIdentifier


class ActionIdentifier(SimpleUniqueIdentifier):
    random_string_length = 12
    identifier_type = "action_identifier"
    identifier_prefix = "AC"
    make_human_readable = True
