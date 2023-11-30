from django.views import View
from django.http import HttpRequest,JsonResponse
from django.contrib.auth.models import User
from .models import Profile
from django.forms import model_to_dict
import json

class UserProfilView(View):

    def get(self, request:HttpRequest,user_id:int):
        try:    
            user=User.objects.filter(is_staff=False, superuser=False)
        except:
            return JsonResponse({})
        profils=Profile.objects.get(user=user)
        result=[]
        for profil in profils:
            result.append(model_to_dict(profil))
        return JsonResponse(result,safe=False)
    def post(self,request:HttpRequest, user_id:int):
        try:
            user=User.objects.get(id=user_id)
        except:
            return JsonResponse({})
        data=json.loads(request.body.decode()) 
        Profile.objects.create(
            phone_number=data.get("phone"),
            age=data.get("age"),
            picture=data.get("picture"),
            user=user
        )
        return JsonResponse({"message":"created"})
    def put(self,request:HttpRequest,user_id:int)->JsonResponse:
        try:
            user=User.objects.get(id=user_id)
        except:
            return JsonResponse({"message":"user does not exist"})
        profil=Profile.objects.get(user=user)
        data=json.loads(request.body.decode())
        Profile.objects.update(
            phone=data.get("phone",profil.phone),
            date_of_birth=data.get("age",profil.date_of_birth),
            pricture=data.get("picture",profil.pricture)
        )
        profil.save()
        return JsonResponse({"message":"updated"})
        return JsonResponse({"message":"updated"})
    def delete(self,request:HttpRequest,user_id:int)->JsonResponse:
        try:
            user=User.objects.get(id=user_id)
        except:
            return JsonResponse({"message":"user not found"})
        user.delete()
        return JsonResponse({"message":"deleted"})