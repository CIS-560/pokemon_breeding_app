from django.shortcuts import render
def app_entry(request):
	return render(request, '../templates/base.html' )


