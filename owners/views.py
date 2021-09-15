import json

# Create your views here.
from django.http        import JsonResponse
from django.views       import View

from owners.models      import Owner, Dog

class OwnerView(View):
    def post(self, request):
        data  = json.loads(request.body)
        Owner.objects.create(
            name = data["name"],
            email = data["email"],
            age = data["age"]
        )
        return JsonResponse({"MESSAGE":"CREATED"}, status=201 )
    
    def get(self, request):
        owners  = Owner.objects.all()
        results = []
        for owner in owners:
            dogList = []
            dogs = owner.dog_set.all()
            for dog in dogs:
                dogList.append({
                    "dog_name" : dog.name,
                    "dog_age"  : dog.age,
                })
            results.append(
                {
                    "owner_name" : owner.name,
                    "owner_email": owner.email,
                    "owner_age"  : owner.age,
                    "dog_list"   : dogList
                }
            )
        return JsonResponse({'resutls':results}, status=200)

class DogView(View):
    def post(self, request):
        data = json.loads(request.body)
        Dog.objects.create(
            name = data["name"],
            age = data["age"],
            owner = Owner.objects.get(id=data["owner_id"])
        )
        return JsonResponse({"MESSAGE":"CREATED"}, status=201 )

    def get(self, request):
        dogs = Dog.objects.all()
        results = []
        for dog in dogs:
            results.append(
                {
                    "dog_name"  : dog.name,
                    "dog_age"   : dog.age,
                    "owner_name": dog.owner.name,
                }
            )
        return JsonResponse({'resutls':results}, status=200)
