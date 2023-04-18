from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from .models import Post
from django.contrib.auth.models import User, Group

from django.template import loader 


#forget password
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages 


#home page
@login_required(login_url="/login")#if not login, redirect to /login
def home(request): 
	posts = Post.objects.all()

	if request.method == "POST":
		post_id = request.POST.get("post-id")
		user_id = request.POST.get("user-id")

		if post_id:
			post = Post.objects.filter(id=post_id).first()
			if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
				post.delete()
		elif user_id:
			user = User.objects.filter(id=user_id).first()
			if user and request.user.is_staff:
				try: 
					group = Group.objects.get(name='default')
					group.user_set.remove(user)
				except: 
					pass 

				try: 
					group = Group.objects.get(name='mod')
					group.user_set.remove(user)
				except: 
					pass
				
	return render(request, 'main/home.html', {"posts": posts})

#create a post form
@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request): 
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect("/home")
	else:
		form = PostForm()
	return render(request, 'main/create_post.html', {"form": form})

#register form
def sign_up(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('/home') 
	else: 
		form = RegisterForm()

	return render(request, 'registration/sign_up.html', {"form": form}) 


#forget password
#We need to add a view function that sends an email to the user if their email connects to an existing user account.
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "main/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
				
					return redirect ("login")
				
				messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
				messages.error(request, 'An invalid email has been entered.')
				
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})

#display the account owner's profile
@login_required
def my_profile(request):
	pf = User.objects.all().values()
	template = loader.get_template('main/my_profile.html')
	context = {
		'pf': pf, 
	}
	return HttpResponse(template.render(context, request))

#the account owner can edit/update their profile information
def edit_my_profile(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		form = RegisterForm(request.POST or None, instance=current_user)
		if form.is_valid():
			form.save()
			login(request, current_user)
			messages.success(request, ("Your Profile has been updated"))
			return redirect('my_profile')
		
		return render(request, "main/edit_my_profile.html", {'form':form})
	else:
		messages.success(request, ("You must logged in to edit profile"))
		return redirect('/login')
	

#display all of the user 
@login_required
def members(request):
  mymembers = User.objects.all().values()
  template = loader.get_template('main/all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))

#display all of the user in details
@login_required
def details(request, id):
  memberdetails = User.objects.get(id=id)
  template = loader.get_template('main/members_details.html')
  context = {
    'memberdetails': memberdetails,
  }
  return HttpResponse(template.render(context, request))

