
from django import forms


class QuestionForm(forms.Form):
    #title = forms.CharField(label="title", max_length=100)
    #content = forms.CharField(label="pole_question", max_length=3000)
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "col-9 pole_for_question"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"col-9 pole_for_question"}))
    tags = forms.CharField(widget=forms.TextInput(attrs={"class": "col-9 pole_for_question"}))
    #tags = forms.CharField(label="tag", max_length=100)


    """
    title = forms.CharField(widget=forms.TextInput(attrs={"class":"col-9 pole_for_question"}))

    content = forms.Field(widget=forms.TextInput(attrs={"class":"col-9 pole_for_question text_pole"}))
    
    
    tags = forms.CharField(widget=forms.TextInput(attrs={"class":"col-9 pole_for_question"}))



    """


