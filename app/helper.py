from app.models import Movie


def apply_filters(statement, search=None, genre=None, rating=None):

    if search:
        escaped_search = (search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_"))

        statement = statement.where(Movie.title.like(f"%{escaped_search}%", escape="\\"))

    if genre:
        statement = statement.where(Movie.genre == genre)

    if rating is not None:
        statement = statement.where(Movie.rating >= rating)

    return statement


SORT_FIELDS = {
    "title": Movie.title,
    "rating": Movie.rating,
    "release_year": Movie.release_year
}
def apply_sort(statement, sort=None):
    
    # if sort == "rating":
    #     statement = statement.order_by(Movie.rating)
    # elif sort == "-rating":
    #     statement = statement.order_by(Movie.rating.desc())
    # elif sort == "title":
    #     statement = statement.order_by(Movie.title)
    # elif sort == "-title":
    #     statement = statement.order_by(Movie.title.desc())
    # elif sort == "release_year":
    #     statement = statement.order_by(Movie.release_year)
    # elif sort == "-release_year":
    #     statement = statement.order_by(Movie.release_year.desc())
    #                      ⬇
    if not sort:
        return statement

    descending = sort.startswith("-")
    field = sort.lstrip("-")
    column = SORT_FIELDS.get(field)

    if column is None:
        return statement

    if descending:
        return statement.order_by(column.desc())

    return statement.order_by(column)



def apply_pagination(statement, page: int = 1, limit: int = 10):

    page = max(page, 1)
    limit = max(limit, 1)

    offset = (page - 1) * limit

    statement = statement.offset(offset)
    statement = statement.limit(limit)

    return statement