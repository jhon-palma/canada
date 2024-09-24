import pdb
from django.contrib import auth
from .models import CustomUser

class Validator(object):
    _post = None
    required = []
    _message = ''

    def __init__(self, post):
        self._post = post

    def is_empty(self, field):
        if field == '' or field is None:
            return True
        return False

    def is_valid(self):
        for field in self.required:
            if self.is_empty(self._post[field]):
                self._message = 'El campo %s no puede ser vacio' %  field
                return False
        return True

    def getMessage(self):
        return self._message
    
class FormLoginValidator(Validator):
    access = None

    def is_valid(self):
        if not super(FormLoginValidator, self).is_valid():
            return False

        email = self._post['email']
        password = self._post['password']

        try:
            access = auth.authenticate(request=self._post, username=email, password=password)
            self.access = access

            if access is None:
                self._message = 'Usuario o contraseña Incorrectos'
                return False
            
            return True
            
        except CustomUser.DoesNotExist:
            self._message = 'Acceso Incorrecto'
            return False


