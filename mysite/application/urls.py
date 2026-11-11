from django.urls import path

from . import views

from .views import homePageView, addView, deleteView, downloadView, addNoteView, searchNoteView

urlpatterns = [
    path('', homePageView, name='home'),
    path('add/', addView, name='add'),
    path('addnote/', addNoteView, name='addNote'),
    path('searchnote/', searchNoteView, name='searchNote'),
    path('download/<int:fileid>', downloadView, name='add'),
    path('delete/', deleteView, name='delete'),
]
