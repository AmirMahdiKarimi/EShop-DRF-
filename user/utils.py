from .models import UserAgent

def get_user_agent(request):
    try:
        print()
        user_agent = str(request.user_agent).split(' / ')
        
        # print(user_agent)
        user_agent = UserAgent.objects.create(family=user_agent[0], brand=user_agent[1], model=user_agent[2])
        return user_agent
    except:
        raise("There isn't user agent!")