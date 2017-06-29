from app.database import init_db
from app.fnforum import start_crawl

max_page = 3

def start_crawl_fn_forum():
    init_db()
    start_crawl(max_page)


if __name__ == '__main__':
    start_crawl_fn_forum()