import json

import connect

from mongoengine.errors import NotUniqueError

from models import Author, Quote


if __name__ == '__main__':
    with open('authors.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(fullname=el.get('fullname'),
                                born_date=el.get('born_date'),
                                born_location=el.get('born_location'),
                                description=el.get('description'))
                author.save()
            except NotUniqueError:
                print(f'Author {el.get('fullname')} already exists')
        
    with open('quotes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            author, *_ = Author.objects(fullname=el.get('author'))
            quote = Quote(quote=el.get('quote'), tags=el.get('tags'), author=author)
            quote.save()
