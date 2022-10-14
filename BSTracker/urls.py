from unicodedata import name
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.displaydashboard, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('caneva/<int:id>', views.displayCaneva, name="caneva"),
    path('List-caneva/', views.displayListCaneva,name='List-caneva'),
    path('cartographie/', views.displaymap, name='cartographie'),
    path('dashboard/', views.displaydashboard, name='dashboard'),
    path('create-caneva/new/<int:id>', views.createnewcaneva, name='add-new'),
    path('create-caneva/new', views.addnewcaneva, name='create-caneva'),
    path('create-caneva/new/<int:id>/submitted', views.canevasubmitted, name='submitted'),
    # path('create-caneva/newblackspot', views.addnewbs, name='newblackspot'),
    path('delete/<int:id>', views.deletebs, name="delete"),
    path('edit/<int:id>', views.editbs, name="edit"),
    path('New-black-spot/<int:id>/<str:stateName>', views.addnewblackspot, name='New-black-spot'),
    path('reports/', views.displayReports, name="reports"),
    path('report/new/<int:id>', views.generateNewReport, name="newReport"),
    path('report/new', views.newReport, name="newReport"),
    path('profil/', views.Displayprofil, name="profil" ),
    # path('display-list-caneva', views.displaylistcaneva, name='display-list-caneva')

    # path('add-new-blackspot/', views.addnewbs, name='add-new-blackspot')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)