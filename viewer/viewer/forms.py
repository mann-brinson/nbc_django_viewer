from django import forms
import datetime

class SearchForm(forms.Form):
	start_date = forms.DateField(initial=datetime.date.today)
	end_date = forms.DateField(initial=datetime.date.today)