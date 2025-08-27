# your_app/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from catalog.models import Genre, Author, Language, Book, BookInstance
import random

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **options):
        self.stdout.write('Creating dummy data...')
        
        # Clear existing data (optional)
        # Genre.objects.all().delete()
        # Author.objects.all().delete()
        # Language.objects.all().delete()
        # Book.objects.all().delete()
        # BookInstance.objects.all().delete()

        # Create Genres
        genres = [
            'Science Fiction', 'Fantasy', 'Mystery', 'Romance', 
            'Thriller', 'Horror', 'Historical Fiction', 'Biography',
            'Young Adult', 'Children', 'Poetry', 'Drama', 'Fiction',
            'Crime'
        ]
        
        genre_objects = []
        for genre_name in genres:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            genre_objects.append(genre)
            self.stdout.write(f'Created genre: {genre_name}')

        # Create Languages
        languages = ['English', 'French', 'Spanish', 'German', 'Italian', 'Russian']
        language_objects = []
        for lang_name in languages:
            lang, created = Language.objects.get_or_create(name=lang_name)
            language_objects.append(lang)
            self.stdout.write(f'Created language: {lang_name}')

        # Create Authors
        authors_data = [
            {'first_name': 'George', 'last_name': 'Orwell', 'dob': date(1903, 6, 25), 'dod': date(1950, 1, 21)},
            {'first_name': 'Jane', 'last_name': 'Austen', 'dob': date(1775, 12, 16), 'dod': date(1817, 7, 18)},
            {'first_name': 'Stephen', 'last_name': 'King', 'dob': date(1947, 9, 21), 'dod': None},
            {'first_name': 'J.K.', 'last_name': 'Rowling', 'dob': date(1965, 7, 31), 'dod': None},
            {'first_name': 'Ernest', 'last_name': 'Hemingway', 'dob': date(1899, 7, 21), 'dod': date(1961, 7, 2)},
            {'first_name': 'Agatha', 'last_name': 'Christie', 'dob': date(1890, 9, 15), 'dod': date(1976, 1, 12)},
        ]
        
        author_objects = []
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                first_name=author_data['first_name'],
                last_name=author_data['last_name'],
                defaults={
                    'date_of_birth': author_data['dob'],
                    'date_of_death': author_data['dod']
                }
            )
            author_objects.append(author)
            self.stdout.write(f'Created author: {author}')

        # Create Books
        books_data = [
            {
                'title': '1984',
                'author': author_objects[0],
                'summary': 'A dystopian social science fiction novel about totalitarian control.',
                'isbn': '9780451524935',
                'genres': ['Science Fiction', 'Drama']
            },
            {
                'title': 'Pride and Prejudice',
                'author': author_objects[1],
                'summary': 'A romantic novel of manners that depicts the emotional development of protagonist Elizabeth Bennet.',
                'isbn': '9780141439518',
                'genres': ['Romance', 'Historical Fiction']
            },
            {
                'title': 'The Shining',
                'author': author_objects[2],
                'summary': 'A horror novel about a family serving as winter caretakers of a haunted hotel.',
                'isbn': '9780307743657',
                'genres': ['Horror', 'Thriller']
            },
            {
                'title': 'Harry Potter and the Philosopher\'s Stone',
                'author': author_objects[3],
                'summary': 'The first novel in the Harry Potter series and Rowling\'s debut novel.',
                'isbn': '9780747532743',
                'genres': ['Fantasy', 'Young Adult']
            },
            {
                'title': 'The Old Man and the Sea',
                'author': author_objects[4],
                'summary': 'A short novel about an aging Cuban fisherman who struggles with a giant marlin.',
                'isbn': '9780684801223',
                'genres': ['Fiction', 'Drama']
            },
            {
                'title': 'Murder on the Orient Express',
                'author': author_objects[5],
                'summary': 'A detective novel featuring the Belgian detective Hercule Poirot.',
                'isbn': '9780062693662',
                'genres': ['Mystery', 'Crime']
            },
        ]

        book_objects = []
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                author=book_data['author'],
                defaults={
                    'summary': book_data['summary'],
                    'isbn': book_data['isbn']
                }
            )
            
            # Add genres
            for genre_name in book_data['genres']:
                genre = Genre.objects.get(name=genre_name)
                book.genre.add(genre)
            
            book_objects.append(book)
            self.stdout.write(f'Created book: {book.title}')

        # Create Book Instances
        status_choices = ['m', 'o', 'a', 'r']
        for book in book_objects:
            # Create multiple instances for each book
            for i in range(random.randint(2, 5)):
                due_back = None
                if random.choice([True, False]):
                    due_back = timezone.now().date() + timedelta(days=random.randint(1, 30))
                
                BookInstance.objects.create(
                    book=book,
                    imprint=f'{random.choice(["Penguin", "Random House", "HarperCollins", "Simon & Schuster"])} Publishing',
                    due_back=due_back,
                    status=random.choice(status_choices)
                )
                self.stdout.write(f'Created instance for: {book.title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with dummy data!'))