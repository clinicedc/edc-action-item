from django import forms


class ActionItemFormMixin(forms.ModelForm):

    action_identifier = forms.CharField(
        label='Action Identifier',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
