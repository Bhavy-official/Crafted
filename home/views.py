from django.shortcuts import render , redirect

def home(request):
    return render(request , 'home/home.html')


def write(request):
    return render(request , 'home/write.html')

def ai_generate(request):
    return render(request , 'home/ai-generate.html')


def signup(request):
  
    return render(request, "home/signup.html")


def login(request):
   
    return render(request, "home/login.html")

def post_detail(request, post_id):
 
    return render(request, 'home/post_detail.html', {'post_id': post_id})