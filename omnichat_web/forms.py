from django import forms


class CompletionForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            'class': 'message-input',
            'placeholder': 'Type here'
        }
    ))


class GPTModelForm(forms.Form):
    prompt = forms.CharField(label='Prompt:', widget=forms.Textarea(
        attrs={
            'class': 'edit-input',
        }
    ))
    examples = forms.CharField(label='Examples:', widget=forms.Textarea(
        attrs={
            'class': 'edit-input',
        }
    ))
