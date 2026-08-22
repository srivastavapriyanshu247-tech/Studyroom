from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import Room,topic,message,User
from .forms import RoomForm,Userform,myUserCreationForm

def loginpage(request):
    page='login'
    if request.method=='POST':
        Email=request.POST.get('email','')
        pasword=request.POST.get('password','')
        try:
            user=User.objects.get(email=Email)
        except:
            messages.error(request,"User does not exist")
        user=authenticate(request,email=Email,password=pasword)
        if user is not None:
            login(request,user)
            next_url=request.GET.get('next')
            return redirect(next_url if next_url else 'home')
        else: messages.error(request,"username or password is wrong")
    context={'page':page}
    return render(request,'login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form=myUserCreationForm()
    if request.method=='POST':
        form=myUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            form.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occurred while registration!")
    context={'form':form}
    return render(request,'login_register.html',context)

def home(request):
    q=request.GET.get('q','')
    try:
        user=User.objects.get(username=q)
    except User.DoesNotExist:
            user=None
    if user:
        return redirect('userProfile',pk=user.id)
    rooms=Room.objects.filter(Q(topic__name__icontains=q)| Q(name__icontains=q)) 
    topics=topic.objects.all()[:4]
    room_count=rooms.count()
    topic_count=topics.count()
    mussage=message.objects.filter(room__in=rooms).order_by('-created')[:7]
    return render(request,'home.html',{'rooms':rooms,
                                       'topics':topics,
                                       'mussages':mussage,
                                       'room_count':room_count,
                                       'topic_count':topic_count})

def room(request,pk):
    edit=False
    rooom=Room.objects.get(id=pk)
    q=request.GET.get('q','')
    if q == 'join':
        rooom.members.add(request.user)
    if request.method=='POST':
        if 'comment' in request.POST:
            message.objects.create(
                user=request.user,
                room=rooom,
                body=request.POST.get('comment')
            )
            rooom.members.add(request.user)
            return redirect('room',pk=rooom.id)
        
        elif 'comment_delete' in request.POST:
            message.objects.get(id=request.POST.get('message_id')).delete()
            return redirect('room',pk=rooom.id)
        
        elif 'button' in request.POST:
            mussage=message.objects.get(id=request.POST.get('message_id'))
            mussage.edit=True
            mussage.save()
            return redirect('room',pk=rooom.id)
        
        elif 'comment_edited' in request.POST:
            mussage=message.objects.get(id=request.POST.get('message_id'))
            mussage.body=request.POST.get('edited_message')
            mussage.edit=False
            mussage.save()
            return redirect('room',pk=rooom.id)
        
    Messages=message.objects.filter(room=rooom).order_by('-created')
    message_count=Messages.count()
    members=rooom.members.all()
    context={'room':rooom,
             'messagus':Messages,
             'message_count':message_count,
             'members':members}
    return render(request,'room.html',context)

def room2(request,pk):
    return render(request,'room2.html')

def user_profile(request,pk):
    host=User.objects.get(id=pk)
    mussage=host.message_set.all().order_by('-created')[:5]
    rooms=host.room_set.all()
    topics=topic.objects.all()[:4]
    content={'user':host, 'mussages':mussage, 'rooms':rooms,'topics':topics}
    return render(request,'user_profile.html',content)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    topics=topic.objects.all()
    
    if request.method == 'POST':
        topicc,created =topic.objects.get_or_create(name=request.POST.get('topic'))
        room=Room.objects.create(
            name=request.POST.get('name'),
            host=request.user,
            description=request.POST.get('description'),
            topic=topicc
        )
        return redirect('home')
    
    context={'form': form,'topics':topics}
    return render(request,'room_form.html',context)

def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=topic.objects.all()
    if request.method == 'POST':
        topicc,created =topic.objects.get_or_create(name=request.POST.get('topic'))
        room.topic=topicc
        room.name=request.POST.get('name')
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')
    content={'topics':topics,'room':room,'form':form}
    return render(request,'room_form.html',content)

def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    topicc=topic.objects.get(name=room.topic.name)
    if request.method=='POST':
        room.delete()
        if topicc.room_set.all().count() == 0:
                topicc.delete()
        return redirect('home')
    content={'obj':room}
    return render(request,'delete.html',content)

def deleteMessage(request,pk):
    msg=message.objects.get(id=pk)
    room=msg.room
    if request.method == 'POST':
        msg.delete()
        return redirect('room',pk=room.id)
    content={'obj':msg}
    return render(request,'delete.html',content)
# def get_search(request):
#     search_name=request.POST.get('tp','')
#     rooms=Room.objects.filter(topic__name__icontains=search_name)
#     content={'rooms':rooms}
#     return render(request,'search.html',content)

# def browse_topics(request,pk):
#     rooms=Room.objects.all()
#     objs=[]
#     for room in rooms:
#         if pk==room.topic.name:
#             objs.append(room)
#     content={'rooms':objs}
#     return render(request,'search.html',content)
@login_required(login_url='login')
def edit_user(request):
    user=request.user
    form=Userform(instance=user)
    if request.method == 'POST':
        form=Userform(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('userProfile',pk=user.id)
    content={'user':user,'form':form}
    return render(request,'edit-user.html',content)


def topicpage(request):
    topics=topic.objects.all()
    return render(request,'topics.html',{'topics':topics})

    