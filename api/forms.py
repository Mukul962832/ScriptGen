from django import forms

class ScriptForm(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter script prompt...'}), required=True)
    file = forms.FileField(required=False)
    language = forms.ChoiceField(choices=[('English', 'English'), ('Spanish', 'Spanish')], required=False)
