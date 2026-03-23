from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, RecruiterProfile 
from django.db.models import Q
from django.core.paginator import Paginator


def index(request):
    return render(request, 'index.html')


def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_home")

        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, "admin_login.html")


def home(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == "POST":
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        company_name = request.POST.get('company_name')

        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        Profile.objects.create(user=user, role=role)

        if role == "recruiter":
            RecruiterProfile.objects.create(
                user=user,
                company_name=company_name
            )

        messages.success(request, "Signup successful, now Signin")
        return redirect('signin')

    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            try:
                profile = Profile.objects.get(user=user)

                if profile.role == role:
                    login(request, user)

                    if role == "user":
                        return redirect('user_home')
                    elif role == "recruiter":
                        return redirect('recruiter_home')
                else:
                    messages.error(request, "Role does not match")

            except Profile.DoesNotExist:
                messages.error(request, "Profile not found.")

        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "signin.html")


@login_required(login_url='signin')
def user_home(request):
    return render(request, "user_home.html")


@login_required(login_url='signin')
def recruiter_home(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role == "recruiter":
        return render(request, "recruiter_home.html")
    else:
        return redirect('user_home')


def Logout(request):
    logout(request)
    return redirect('index')
@login_required
def admin_home(request):
    return render(request, "admin_home.html")
def view_users(request):

    search = request.GET.get('search')

    users_list = User.objects.filter(is_staff=False)

    if search:
        users_list = users_list.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )

    paginator = Paginator(users_list, 5)   # 5 users per page
    page = request.GET.get('page')

    users = paginator.get_page(page)

    return render(request, 'view_users.html', {'users': users})
def delete_user(request, id):

    user = User.objects.get(id=id)

    user.delete()

    return redirect('view_users')
def recruiters_pending(request):
    recruiters = RecruiterProfile.objects.filter(status='pending')
    return render(request,'recruiters_pending.html',{'recruiters':recruiters})

def accepted_recruiters(request):
    recruiters = RecruiterProfile.objects.filter(status='accepted')
    return render(request,'accepted_recruiters.html',{'recruiters':recruiters})

def rejected_recruiters(request):
    recruiters = RecruiterProfile.objects.filter(status='rejected')
    return render(request,'rejected_recruiters.html',{'recruiters':recruiters})

def all_recruiters(request):
    recruiters = RecruiterProfile.objects.all()
    return render(request,'all_recruiters.html',{'recruiters':recruiters})
def accept_recruiter(request, id):
    recruiter = get_object_or_404(RecruiterProfile, id=id)
    recruiter.status = "Accepted"
    recruiter.save()
    return redirect('accepted_recruiter')  # change if different name


def reject_recruiter(request, id):
    recruiter = get_object_or_404(RecruiterProfile, id=id)
    recruiter.status = "Rejected"
    recruiter.save()
    return redirect('rejected_recruiters.html')
def accepted_recruiters(request):
    recruiters = RecruiterProfile.objects.filter(status="Accepted")
    return render(request, 'accepted_recruiters.html', {'recruiters': recruiters})
def reject_recruiter(request, id):
    recruiter = get_object_or_404(RecruiterProfile, id=id)
    recruiter.status = "Rejected"
    recruiter.save()
    return redirect('rejected_recruiters') 
def all_recruiters(request):
    recruiters = RecruiterProfile.objects.all()
    return render(request, 'all_recruiters.html', {'recruiters': recruiters})
def changepassword_admin(request):
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Check old password
        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect")
            return redirect('changepassword_admin')

        # Check new password match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match")
            return redirect('changepassword_admin')

        # Set new password
        user.set_password(new_password)
        user.save()

        # Keep user logged in
        update_session_auth_hash(request, user)

        messages.success(request, "Password changed successfully")
        return redirect('admin_home')

    return render(request, 'changepassword_admin.html')