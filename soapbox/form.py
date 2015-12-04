from django import forms

def	get_my_choices():


    my_choices = (('1', 'Option 1'),('2', 'Option 2'),('3', 'Option 3'),)

    return my_choices

class PostForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=1)
    last_name = forms.CharField(label='First Name', max_length=100)
    my_choice_field = forms.ChoiceField(choices=get_my_choices())
    myfield = forms.CharField(widget=forms.Textarea(attrs={'class' : 'myfieldclass'}))
   