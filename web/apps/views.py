from django.shortcuts import render
def app_entry(request):
	return render(request, '../templates/homepage.html' )

def login(request):
    return render(request, '../templates/login.html')
