from django import forms


class NameForm(forms.Form):
    #   your_name = forms.CharField(label='Your name', max_length=100)
    #   title = forms.CharField(label='Your name',max_length=50)
    file = forms.FileField()


