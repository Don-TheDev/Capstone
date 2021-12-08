from django import forms


class CompletionForm(forms.Form):
    message_input = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            'class': 'message-input w3-theme-light',
            'placeholder': 'Type here'
        }
    ))


class GPTModelForm(forms.Form):
    prompt = forms.CharField(label='Prompt:', widget=forms.Textarea(
        attrs={
            'class': 'edit-input w3-padding w3-margin w3-theme-light',
        }
    ))
    examples = forms.CharField(label='Examples:', widget=forms.Textarea(
        attrs={
            'class': 'edit-input w3-padding w3-margin w3-theme-light',
        }
    ))
