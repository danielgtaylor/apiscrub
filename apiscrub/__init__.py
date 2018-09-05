'''API Scrubber'''


def should_keep(tag, keep, item):
    '''
    Determine whether we should keep an item based on the set of tag values
    that were given to be kept. If the `x-only` tag is present, then at least
    one match means we keep the item, otherwise remove it. If not present,
    then we default to keeping it.
    '''
    if tag in item:
        only = item[tag]

        # Can be either a list or string, but we want a list.
        if isinstance(only, str):
            only = [only]

        del item[tag]

        if not set(only) & keep:
            return False

    return True


def process(tag, keep, piece):
    '''
    Process a data structure to filter out items. This also removes the special
    `x-only` property, if present.
    '''
    removed = []

    for k, v in list(piece.items()):
        if v is None:
            continue

        # Below we check for "dict-like" and "list-like" structures, since
        # these can be loaded in various ways by the parser.
        if hasattr(v, 'get'):
            # This is a dictionary-like object.
            if should_keep(tag, keep, v):
                removed = process(tag, keep, v)

                # Special case: JSON Schema required fields
                if k == 'properties' and 'required' in piece:
                    for r in removed:
                        if r in piece['required']:
                            piece['required'].remove(r)
            else:
                del piece[k]
                removed.append(k)
        elif hasattr(v, 'append'):
            # This is a list-like object. Iterate a copy while deleting items.
            # TODO: this currently only goes one level deep in lists, but could
            # be updated to traverse lists of lists as well. I don't think this
            # is currently used in OpenAPI 3.x.
            for item in v[:]:
                if hasattr(item, 'get'):
                    if should_keep(tag, keep, item):
                        process(tag, keep, item)
                    else:
                        v.remove(item)

            # All items of a list were removed, so remove the list. This is
            # useful for examples where the list is only present given the
            # right permissions/role.
            if not v:
                del piece[k]
                removed.append(k)

    return removed
