
def find_by_id(items, id):
    for item in items:
        if item.id == id:
            break
    return item
