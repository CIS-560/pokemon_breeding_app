from django.shortcuts import render

# Create your views here.
def app_entry(request):
	return render(request, '../templates/base.html' )
