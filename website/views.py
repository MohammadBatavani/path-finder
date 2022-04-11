from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Map, Map_Thread, History, Algorithm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from core.A_Star import A_Star
from django.http import StreamingHttpResponse

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if request.POST.get('firstname'):
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            User.objects.create_user(username=username, email=email,
                                     password=password, first_name=firstname, last_name=lastname)
        login(request, authenticate(request, username=username, password=password))
        return redirect(switch)
    return render(request, 'signUp-signIn.html')

@login_required(login_url=login_view)
def switch(request):
    return render(request, 'switch.html')

@login_required(login_url=login_view)
def main_view(request):

    context = {
        'Map': Map.objects.all(),
        'History': History.objects.filter(creator=request.user),
        'Algorithm': Algorithm.objects.all()
    }
    return render(request, 'frames.html', context=context)


@login_required(login_url=login_view)
def calculate_view(request):
    if request.method == 'POST':
        map_id = request.POST.get('map')
        algorithm = request.POST.get('algorithm')
        start_point = (int(request.POST.get('start_x')),
                       int(request.POST.get('start_y')))
        destination_point = (int(request.POST.get('destination_x')), int(
            request.POST.get('destination_y')))
        map_query = Map.objects.get(id=map_id)
        
        if (algorithm == 'A_Star'):
            engine = A_Star(map_query, start_point, destination_point, request.user)

        Map_Thread(thread_address=str(engine).split(' ')[-1][:-1],
                   creator=request.user, working_map=map_query,
                   algorithm=algorithm).save()
        return StreamingHttpResponse(engine.start())


@login_required(login_url=login_view)
def signOut(request):
    logout(request)
    return redirect(login_view)


def write_history(user, map, start_point, destination_point, res_dir, res_dir_distance, res_2d_distance, res_time_of_arrival):
    temp = History(creator=user, map=map, start_point={'x': start_point[0], 'y': start_point[1]},
            destination_point={'x': destination_point[0], 'y': destination_point[1]}, res_dir={0: res_dir},
            res_dir_distance=res_dir_distance, res_2d_distance=res_2d_distance, res_time_of_arrival=res_time_of_arrival)
    temp.save()
    return temp.id


def delete_map_thread(thread_address):
    Map_Thread.objects.get(thread_address__contains=thread_address).delete()