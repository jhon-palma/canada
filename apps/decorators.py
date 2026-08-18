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
