ITEMS_PER_PAGE = 3

# I use universal naming as I might use it on other routes
# Currently it is the same items per page variable.
# In order to change this, define another parameter here and
# Add arguement with its own variable when calling the function
def paginate(req, db_array):
    page = req.args.get('page', 1, type=int)
    start = (page -1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [item.format() for item in db_array]

    return items[start:end]

