from django.urls import path # type: ignore
from . import views

urlpatterns = [
path('', views.home, name='home'),
path('explore', views.explore, name='explore'),
path('register', views.register, name='register'),
path('login', views.login, name='login'),
path('perfil', views.perfil, name='perfil'),
path('logout', views.logout, name='logout'),
path('adminBook', views.adminBook, name='adminBook'),
path('addBook', views.addBook, name='addBook'),
path('editBook/<int:id>/', views.editBook, name='editBook'),
path('deleteBook/<int:id>/', views.deleteBook, name='deleteBook'),
path('viewBook/<int:id>/', views.viewBook, name='viewBook'),
path('getBook/<int:id>/', views.getBook, name='getBook'),
path('contri/<int:user_id>', views.contri, name='contri'),
path('adminUsers', views.adminUsers, name='adminUsers'),
path('addUsers/', views.addUsers, name='addUsers'),
path('editUser', views.editUser, name='editUser'),
path('prestamos/', views.prestamos, name='prestamos'),
path('addPrestamo/', views.addPrestamo, name='addPrestamo'),
path('editPrestamo/', views.editPrestamo, name='editPrestamo'),
path('test', views.test, name='test'),
path('tour_virtual', views.tour_virtual, name='tour_virtual'),
path('prestamo_salas', views.prestamo_salas, name='prestamo_salas'),
]
