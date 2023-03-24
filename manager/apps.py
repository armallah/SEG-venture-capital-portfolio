from django.apps import AppConfig



class ManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manager'    

    def ready(self):

        from manager.models import User
        try:
            User.objects.create_superuser(
                    username="admin@wayra.co"
                    ,password="password"
                    ,first_name = "Wayra"
                    ,last_name = "Admin"
                    ,user_type = 2
                    )
        except:
            print("hi")

        pass # startup code here
