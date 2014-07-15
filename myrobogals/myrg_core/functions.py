"""
    myRobogals
    myrg_core/functions.py
    Custom APILog model definition

    2014
    Robogals Software Team
"""
from .models import APILog

from myrg_groups.models import Role
#from myrg_groups.serializers import RoleSerializer

from .models import APILog
from rest_framework import serializers, status

def log(request, note = None):
    log_dict = {
        "role": None,
        "api_url": request.get_full_path(),
        "api_body": "{'test':'test'}",
        "note": None,
    }
    
    new_log = APILog(**log_dict)
    
    try:
        new_log.save()
    except:
        return False
        
    return new_log

# http://stackoverflow.com/a/4581997
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



class APILogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APILog
        
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        
        
def login_record(request):
    
    #initialise variables 
    user_role = []
    ip_address = ""
    api_url = ""
    api_body = "" 
    
    if request.user.is_authenticated():
       # request.user
       user_id = request.user.pk
       request.session['user_id'] = user_id
       
       # user_role
       RoleSerializer.Meta.fields = ["id"]
       role_serializer_query = RoleSerializer(Role.objects.filter(user = user_id))
       json_user_role = role_serializer_query.data
       for field_object in json_user_role:
            user_role.append(field_object.get("id"))
       
       #ip_address
       ip_address = get_client_ip(request)
       
       #api_url
       api_url = request.get_full_path()
       
       #api_body
       api_body = request.body
       
       #session
       note = request.session['user_id']
                   
    content = {
        "user_role": user_role,
        "ip": ip_address,
        "api_url":api_url,
        "api_body":str(api_body),
        "note":str(note),
    }
    
    serializer = APILogSerializer(data=content)
    if serializer.is_valid():
       serializer.save()
       return (content, serializer.data)
    else:
       return (content, serializer.data, serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    #return content
    
   