from django.shortcuts import render
from django.contrib.auth.models import Group, User

def add_user_to_group(user_id, group_name):
    try:
        user = User.objects.get(id=user_id)
        group = Group.objects.get(name=group_name)
        group.user_set.add(user)
        return f"Korisnik {user.username} dodan u grupu {group_name}."
    except User.DoesNotExist:
        return "Korisnik ne postoji."
    except Group.DoesNotExist:
        return "Grupa ne postoji."
