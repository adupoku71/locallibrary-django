from django.contrib import admin
from .models import Author, Book, Genre, BookInstance, Language

# Register your models here.
# inline display of associated models
class BooksInline(admin.TabularInline):
    # vertical layout
    model = Book
class BooksInstanceInline(admin.TabularInline):
    # horizontal layout
    model = BookInstance

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    
    # The fields attribute lists just those fields that are to be displayed on the form, in order. Fields are displayed vertically by default, but will display horizontally if you further group them in a tuple  
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    
    inlines = [BooksInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    
    # You can add "sections" to group related model information within the detail form, using the fieldsets attribute.
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

# admin.site.register(Author)
# admin.site.register(Book)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)
