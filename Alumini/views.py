from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt



def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Username: {username}")
        print(f"Password: {password}")
        print(request.user.id)

        # Check if the username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect('/') 

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, "Logged in successfully!")
            return redirect('/alumini-page')
        else:
            messages.error(request, "Invalid Password")
            return redirect('/')  

    return render(request, 'login.html')


def Registraion_page(request):
    if request.method =='POST':
        firstName = request.POST.get('firstname')
        lastName = request.POST.get('lastname')
        userName = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = userName)
        if user.exists():
            messages.info(request,'Username Already taken')
            return redirect('/registration-page')
        

        user = User.objects.create(
            first_name = firstName,
            last_name = lastName,
            username = userName
        )

        user.set_password(password)
        user.save()
        messages.info(request,'Account Created Successfully')
        return redirect('/')
    return render(request,'registration.html')



def logout_page(request):
    logout(request)
    return redirect('/')


@login_required
def alumini_profile(request):
    if request.method == 'POST':
        current_role = request.POST.get('current_role')
        industry = request.POST.get('industry_name')
        skills = request.POST.get('skills')
        location = request.POST.get('location')
    
        
        if Alumni.objects.filter(user=request.user).exists():
            messages.error(request, "You already have an alumni profile.")
            return redirect('/alumini-profile')

        alumini = Alumni.objects.create(
            user = request.user,
            current_role = current_role,
            industry = industry,
            skills = skills,
            location = location
        )
        alumini.save()
        return redirect('alumini-profile-show', user_id=request.user.id)

    return render(request,'alumini_profile.html')
def edit_alumni_profile(request):
    alumni = get_object_or_404(Alumni, user=request.user)

    if request.method == 'POST':
        alumni.current_role = request.POST.get('current_role')
        alumni.industry = request.POST.get('industry')
        alumni.skills = request.POST.get('skills')
        alumni.location = request.POST.get('location')

        alumni.save()
        print(reverse('alumini-profile-show', kwargs={'user_id': request.user.id}))


        messages.success(request, "Profile updated successfully!")
        return redirect('alumini-profile-show', user_id=request.user.id)
    
    return render(request, 'alumini_edit_profile.html', {'alumni': alumni})


def alumini_profile_show(request, user_id):
    alumni = get_object_or_404(Alumni, user__id=user_id)
    return render(request, 'alumini_profile_show.html', {'alumni': alumni})


def delete_profile(request,user_id):
    alumini = Alumni.objects.get(id = user_id)
    alumini.delete()
    return redirect('/alumini-page')



def post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        des = request.POST.get('textarea')

        print(image)
        print(des)

        Post.objects.create(
            alumni = request.user,
            image = image,
            description = des
        )

        return redirect('/alumini-page')
    return render(request,'Alumnipost.html')




def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Ensure the request is a POST request for CSRF protection
    if request.method == 'POST':
        if request.user in post.like.all():
            post.like.remove(request.user)  # Unlike the post
            liked = False
        else:
            post.like.add(request.user)  # Like the post
            liked = True

        # Get the updated like count
        likes_count = post.like.count()
        return JsonResponse({'likes_count': likes_count, 'liked': liked})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)



def alumini_page(request):
    allpost = Post.objects.all().order_by('-created_at')
    if request.method == 'POST':
        queryset = request.POST.get('search')

        if queryset:
            aluminis = Alumni.objects.filter(user__username__icontains=queryset)

        return render(request,'alumini_list.html',{'aluminis':aluminis})
    else:
       return render(request,'alumini.html',{'allpost':allpost})
       

def alumini_list(request):
    if request.method == 'POST':
        queryset = request.POST.get('search')
        
        if queryset:
            # Searching alumni based on multiple fields
            aluminis = Alumni.objects.filter(
                Q(user__username__icontains=queryset) |
                Q(location__icontains=queryset) |
                Q(skills__icontains=queryset) |
                Q(industry__icontains=queryset)
            ).order_by('user__username')
        else:
            aluminis = Alumni.objects.all().order_by('user__username')
        
        return render(request, 'alumini_list.html', {'aluminis': aluminis, 'user_id': request.user.id})
    else:
        aluminis = Alumni.objects.all().order_by('user__username')
        return render(request, 'alumini_list.html', {'aluminis': aluminis, 'user_id': request.user.id})



# views.py
def connection_requests_view(request):
    # Get the pending requests for the logged-in user (receiver)
    pending_requests = Connection.objects.filter(receiver=request.user, status="Pending")

    # Pass the current user (receiver) ID to the template
    return render(request, "connection_requests.html", {
        "pending_requests": pending_requests,  # List of pending requests
        "receiver_id": request.user.id  # Receiver's user ID
    })


@csrf_exempt
def accept_connection(request, request_id):
    if request.method == "POST":
        try:
            connection = Connection.objects.get(id=request_id, receiver=request.user, status="Pending")
            connection.status = "Accepted"
            connection.save()
            return JsonResponse({"success": True, "message": "Connection accepted!"})
        except Connection.DoesNotExist:
            return JsonResponse({"success": False, "message": "Connection request not found!"}, status=404)

    return JsonResponse({"success": False, "message": "Invalid request method!"}, status=400)

def get_connection_request_count(request):
    count = Connection.objects.filter(receiver=request.user, status="Pending").count()
    return JsonResponse({"count": count})





# for updated connected button, when request accepted
def send_connection_request(request, user_id):
    if request.method == 'POST':
        receiver = get_object_or_404(User, id=user_id)
        connection, created = Connection.objects.get_or_create(sender=request.user, receiver=receiver)
        if created:
            # WebSocket notification logic here
            return JsonResponse({'message': 'Connection request sent!', 'status': 'success'})
        return JsonResponse({'message': 'Connection request already exists!', 'status': 'exists'})



@csrf_exempt
def accept_connection(request, request_id):
    if request.method == "POST":
        try:
            connection = Connection.objects.get(id=request_id, receiver=request.user, status="Pending")
            connection.status = "Accepted"
            connection.save()
            return JsonResponse({"success": True, "message": "Connection accepted!"})
        except Connection.DoesNotExist:
            return JsonResponse({"success": False, "message": "Connection request not found!"}, status=404)

    return JsonResponse({"success": False, "message": "Invalid request method!"}, status=400)


def get_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')

    comments_data = [
        {"user": comment.user.username, "text": comment.text, "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M")}
        for comment in comments
    ]
    
    return JsonResponse({"comments": comments_data})

def add_comment(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        comment_text = request.POST.get("comment_text")
        post = get_object_or_404(Post, id=post_id)

        new_comment = Comment.objects.create(post=post, user=request.user, text=comment_text)

        return JsonResponse({
            "user": new_comment.user.username,
            "text": new_comment.text,
            "created_at": new_comment.created_at.strftime("%Y-%m-%d %H:%M"),
            "comment_count": post.comments.count(),
        })

    return JsonResponse({"error": "Invalid request"}, status=400)
