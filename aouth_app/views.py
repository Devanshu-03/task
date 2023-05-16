from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes,throttle_classes
from rest_framework.response import Response
from aouth_app.models import UserDetails
from oauthlib.common import generate_token
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from oauthlib.common import generate_token
from datetime import datetime, timedelta
from rest_framework.throttling import UserRateThrottle
from aouth_app.models import UserDetails
from rest_framework.exceptions import Throttled
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework_simplejwt.tokens import RefreshToken
from aouth_app.models import UserDetails
from rest_framework import status
from django.http import QueryDict
from django.core.paginator import Paginator
from aouth_app.serializers import UserDetailsSerializer
import requests



@api_view(['POST'])
@permission_classes([])
@throttle_classes([UserRateThrottle])
def insert_user_details(request):

    #check the rate limit for the user making the request
    rate_limit = UserRateThrottle()
    if rate_limit.allow_request(request=request,view=None):
        # Extract the user details from the request body
        f_name = request.data.get('f_name')
        l_name = request.data.get('l_name')
        email_id = request.data.get('email_id')
        phone_number = request.data.get('phone_number')
        address = request.data.get('address')


        # Perform validation on the input data
        if not all([f_name, l_name, email_id, phone_number, address]):
            return Response({'error': 'All fields are required'}, status=400)

        # Generate an access token
        access_token = generate_token()

        # Set the expiration time for the access token
        expires_at = datetime.now() + timedelta(minutes=3)
        max_age = int((expires_at - datetime.now()).total_seconds())


        # Create the user details object
        user_details = UserDetails(f_name=f_name, l_name=l_name, email_id=email_id,phone_number=phone_number, address=address)
        user_details.save()

        response = Response({'message':'Details inserted Successfully'})
        response.set_cookie('access_token',access_token,max_age)#expire after 3 min
        return response
    


    else:
        # If the rate limit is exceeded, raise a Throttled exception
        raise Throttled(wait=rate_limit.wait())
    
#get all user details api
@api_view(['GET'])
@throttle_classes([UserRateThrottle])
@permission_classes([])
def listusers(request):
    # Apply pagination
    paginator = LimitOffsetPagination()
    paginator.default_limit = 10  # Number of items per page
    

    users = UserDetails.objects.all().order_by('created_date')
    result_page = paginator.paginate_queryset(users, request)
    serializer = UserDetailsSerializer(result_page, many=True)

    # Create pagination 
    current_page_number = (paginator.offset // paginator.limit) + 1 if paginator.limit else 1
    next_page_number = current_page_number + 1 if paginator.offset + paginator.limit < paginator.count else None
    prev_page_number = current_page_number - 1 if current_page_number > 1 else None

    


    response = {
        'count': paginator.count,
        'current': current_page_number,
        'next': next_page_number,
        'previous': prev_page_number,
        'results': serializer.data,
    }

    return Response(response)

def home(request):
    if request.method =='POST':
       f_name = request.POST.get('f_name')
       l_name = request.POST.get('l_name')
       email = request.POST.get('email_id')
       address = request.POST.get('address')
       phone_number = request.POST.get('phone_number')
       data = {'f_name':f_name,'l_name':l_name,'email_id':email,'address':address,'phone_number':phone_number}
       header = {'content-Type':'application/json'}
       read = requests.post('http://127.0.0.1:8000/api/userdetails/',json=data,headers=header)
       return render(request,'index.html')
    else:
        return render(request,'index.html')


def list_user(request):
    user_data = UserDetails.objects.all()
    paginator = Paginator(user_data, 10)  # Display 10 items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    response = requests.get('http://127.0.0.1:8000/api/listusers/').json()
    print(response)
    return render(request,'userlist.html',{'response':response})
   