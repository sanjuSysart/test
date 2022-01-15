



import jwt
from rest_framework.exceptions import AuthenticationFailed
from.models import tbl_user
from.serializer import EmployeeSerializer


# Token Authentication 

def authentications(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithm = ['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    user = tbl_user.objects.filter(us_id= payload['id']).first()
    serializer = EmployeeSerializer(user).data['us_id'] 
    return serializer