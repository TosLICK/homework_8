import connect
import redis
from redis_lru import RedisLRU

from models import Author, Quote


client = redis.StrictRedis(host='', port=6379, password=None)
cache = RedisLRU(client)


def parse_input(user_input: str) -> tuple[str, list]:
    if ':' not in user_input:
        cmd = user_input.strip().lower()
        return cmd, []
    cmd = user_input[:user_input.index(':')].strip().lower()
    args = user_input[user_input.index(':') + 1:].lower().split(',')
    args = [arg.strip() for arg in args]
    return cmd, args

def usage():
    return "Usage:\n'name: <author_name>'\n'tag: <tag_name>'\n'tags: <tag_name>, <tag_name>'\n'exit'\n'close'"

@cache
def find_by_tags(tags: list) -> tuple[str | None]:
    quotes = []
    for tag in tags:
        quotes.extend(Quote.objects(tags__iregex=tag))
    # quotes = Quote.objects(__raw__={"tags": {"$in": tags }})
    quotes = set(quotes)
    result = tuple([q.quote.encode('utf-8') for q in quotes])
    return result

@cache
def find_by_author(author: str) -> dict:
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote.encode('utf-8') for q in quotes]
    return result

def main():
    while True:
        user_input = input("Enter a command and a value separeted by a colon: ")
        try:
            command, args = parse_input(user_input)

            match command:
                case 'close' | 'exit':
                    break
                case 'name':
                    args = args[0]
                    print(find_by_author(args))
                case 'tag' | 'tags':
                    print(find_by_tags(args))
                case _:
                    print(usage())
        except ValueError:
            print('ValueError')
        except IndexError:
            print('IndexError')
        except KeyError:
            print('KeyError')


if __name__ == '__main__':
    main()
