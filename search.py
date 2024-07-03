import connect
import redis
from redis_lru import RedisLRU

from models import Author, Quote


client = redis.StrictRedis(host='', port=6379, password=None)
cache = RedisLRU(client)


def parse_input(user_input):
    cmd, *args = user_input.split(':')
    cmd = cmd.strip().lower()
    return cmd, *args

def usage():
    return "Usage: 'name: <author_name>'\n'tag: <tag_name>'\n'tags: <tag_name>, <tag_name>'\n'exit'\n'close'"

@cache
def find_by_tag(tag: str) -> list[str |  None]:
    quotes = Quote.objects(tags__iregex=tag)
    # quotes = Quote.objects(tags=tag)
    # quotes = Quote.objects().all()
    result = [q.quote for q in quotes]
    return result
    # result
    # quotes = Quote.objects(tags__icontains=tag)
    # print([q.to_json() for q in quotes])

@cache
def find_by_author(author: str) -> dict:
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result

def main():
    while True:
        user_input = input("Enter a command and a value separeted by a colon: ")
        try:
            command, *args = parse_input(user_input)

            match command:
                case 'close' | 'exit':
                    break
                case 'name':
                    print(find_by_author(args))
                case 'tag' | 'tags':
                    print(find_by_tag(args))
                case _:
                    print(usage())
        except ValueError:
            print('ValueError') # usage()
        except IndexError:
            print('IndexError')
        except KeyError:
            print('KeyError')


if __name__ == '__main__':
    main()
    # quotes = Quote.objects().all()
    # print([e.to_json() for e in quotes])