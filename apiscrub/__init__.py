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
    removed_paths = []
    _process(tag, keep, piece, '#', removed_paths)
    _clean_refs(removed_paths, piece)


def _process(tag, keep, piece, path, removed_paths):
    removed = []

    for k, v in list(piece.items()):
        if v is None:
            continue

        # Use JSON-Pointer (RFC6901) encoding for building the path.
        cur_path = path + '/' + str(k).replace("~", "~0").replace("/", "~1")

        # Below we check for "dict-like" and "list-like" structures, since
        # these can be loaded in various ways by the parser.
        if hasattr(v, 'get'):
            # This is a dictionary-like object.
            if should_keep(tag, keep, v):
                removed = _process(tag, keep, v, cur_path, removed_paths)

                # Special case: JSON Schema required fields
                if k == 'properties' and 'required' in piece:
                    for r in removed:
                        if r in piece['required']:
                            piece['required'].remove(r)
            else:
                del piece[k]
                removed.append(k)
                removed_paths.append(cur_path)
        elif hasattr(v, 'append'):
            # This is a list-like object. Iterate a copy while deleting items.
            # TODO: this currently only goes one level deep in lists, but could
            # be updated to traverse lists of lists as well. I don't think this
            # is currently used in OpenAPI 3.x.
            for item in v[:]:
                if hasattr(item, 'get'):
                    if should_keep(tag, keep, item):
                        _process(tag, keep, item, cur_path, removed_paths)
                    else:
                        v.remove(item)

            # All items of a list were removed, so remove the list. This is
            # useful for examples where the list is only present given the
            # right permissions/role.
            if not v:
                del piece[k]
                removed.append(k)
                removed_paths.append(cur_path)

    return removed


def _clean_refs(removed_refs, piece):
    # This is basically the same logic as above, but done in a second pass
    # so we know all the items that were removed. We go through and remove any
    # references to items that now no longer exist.
    for k, v in list(piece.items()):
        if v is None:
            continue

        if hasattr(v, 'get'):
            # This is a dictionary-like object.
            if v.get('$ref') in removed_refs:
                del piece[k]
                continue

            _clean_refs(removed_refs, v)
        elif hasattr(v, 'append'):
            # This is a list-like object. Iterate a copy while deleting items.
            for item in v[:]:
                if hasattr(item, 'get'):
                    if item.get('$ref') in removed_refs:
                        v.remove(item)

                if not v:
                    del piece[k]
