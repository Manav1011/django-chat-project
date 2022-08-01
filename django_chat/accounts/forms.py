from allauth.account.forms import SignupForm,LoginForm

class login_form(LoginForm):
    def login(self,*args,**kwargs):
        return super().login(**args,**kwargs)
    
    