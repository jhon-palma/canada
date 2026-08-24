"""Decoradores de control de acceso compartidos.

`login_required` no alcanza para las vistas internas destructivas: el blog
tiene registro publico (`blog:signup_blog` crea CustomUser con userBlog=True),
asi que cualquier comentarista quedaria autenticado. Estas vistas exigen
ademas `is_staff`.
"""

from django.contrib.auth.decorators import user_passes_test


def is_staff_user(user):
    return user.is_active and user.is_staff


#: Restringe la vista a usuarios internos activos con is_staff.
staff_required = user_passes_test(is_staff_user, login_url='accounts:login')


def is_internal_user(user):
    """Del equipo, por oposicion a quien se registro desde el blog.

    userBlog es la marca que ya usa el proyecto para separar unos de otros:
    users/views.py lista las cuentas internas con userBlog=False y las del
    blog con userBlog=True, y accounts/views.py mira el campo al entrar.

    Se prefiere a is_staff para las vistas de gestion del blog porque
    publicar no deberia exigir acceso al admin de Django: cualquiera del
    equipo escribe articulos, y solo unas pocas cuentas necesitan is_staff.
    """
    return (user.is_authenticated and user.is_active
            and not getattr(user, 'userBlog', False))


#: Restringe la vista a cuentas del equipo, sin exigirles is_staff.
interno_required = user_passes_test(is_internal_user, login_url='accounts:login')
