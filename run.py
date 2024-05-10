# from src.main.app import app

# if __name__ == '__main__':
#     app.run(debug=True)

from src.database.bookmarks_database import *

from sqlalchemy import inspect


# def object_as_dict(obj):
#     return {c.key: getattr(obj, c.key)
#             for c in inspect(obj).mapper.column_attrs}


print(get_bookmark_by_id(1, 1))
