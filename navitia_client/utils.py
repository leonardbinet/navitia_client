"""
This module contains some useful functions.

For now:
 - flatten_columns
 - flatten_dataframe
"""


def important_print(message, level=0):
    if level == 1:
        print("-" * 70)
        print(message.capitalize())
        print("-" * 70)
    if level == 0:
        print("-" * 50)
        print(message)
        print("-" * 50)


def flattenjson(b, delim):
    val = {}
    if isinstance(b, dict):
        for i in b.keys():
            if isinstance(b[i], dict):
                get = flattenjson(b[i], delim)
                for j in get.keys():
                    val[i + delim + j] = get[j]
            else:
                val[i] = b[i]
    return val


def length_with_nan(x):
    if isinstance(x, list):
        return len(x)
    else:
        return x


def first_with_nan(x):
    if isinstance(x, list):
        return x[0]
    else:
        return x


def keys_with_nan(x):
    if isinstance(x, dict):
        return str(list(x.keys()))
    else:
        return x


def check_asked_cols(df_to_check, cols_to_check):
    real_columns = df_to_check.columns
    for column in cols_to_check:
        if column not in real_columns:
            cols_to_check.remove(column)
    return cols_to_check


def flatten_columns(df, columns_list, drop=False, debug=False):
    """
    Goal: flatten a dataframe, which has columns filled with lists or dictionnaries.

    Parameters:
    - df : dataframe: the dataframe you want to flatten
    - columns_list: list of strings: the columns you want to flatten
    - drop: boolean: to drop flattened columns

    Dataframe is changed in place, with new columns, and flattened columns deleted if drop=True.
    Returns added columns
    """

    # First, we check if asked columns are present
    columns_list = check_asked_cols(df, columns_list)

    # Instanciate list of created columns during process
    added_columns = []
    for column_flattened in columns_list:
        if debug:
            print("-" * 20)
            print("FLATTENING " + column_flattened.capitalize())

        # Find out whether the value is a dict
        # TODO check on whole column
        if isinstance(df[column_flattened][0], dict):

            # Lets check if keys are all the same:
            # First we find keys on the dictionnary
            series_keylists = df[column_flattened].apply(keys_with_nan)
            # We count occurences of unique lists of keys
            keylists_counts = series_keylists.value_counts()

            # If there is always the same key we can flatten
            if len(keylists_counts) == 1:
                if debug:
                    print("This columns has dicts of same keys. Ok to flatten.")
                keys_to_flatten = list(df[column_flattened][0].keys())
                for key in keys_to_flatten:

                    def key_with_nan(x):
                        try:
                            return x[key]
                        except:
                            return x

                    df[column_flattened + "_" +
                        key] = df[column_flattened].apply(key_with_nan)
                    added_columns.append(column_flattened + "_" + key)
                    if debug:
                        print("Created column : " +
                              column_flattened + "_" + key)
                if drop:
                    df.drop(column_flattened, axis=1, inplace=True)
                    if debug:
                        print("Removed original " + column_flattened)
            else:
                if debug:
                    print("Keys are not the same on all rows.")
                    print(keylists_counts)

        # Find out whether the value is a list
        # TODO check on whole column
        elif isinstance(df[column_flattened][0], list):
            if debug:
                print("Column " + column_flattened + " is a list.")
            # check if all of same size

            series_sizes = df[column_flattened].apply(length_with_nan)

            sizes_counts = series_sizes.value_counts()
            if debug:
                print("Counts of different sizes: ", len(sizes_counts))
            # if all of same size
            if len(sizes_counts) == 1:
                if debug:
                    print("All of same size: " + str(sizes_counts))
                # and if size is one: we can flatten list [x] -> x
                if series_sizes[0] == 1:
                    if debug:
                        print(
                            "All lists are from size one, so we can take flatten it.")
                    df[column_flattened] = df[
                        column_flattened].apply(first_with_nan)
                    added_columns.append(column_flattened)
                    if debug:
                        print("Replaced column " + column_flattened)
            else:
                if debug:
                    print(
                        "Size are not the same or >1 so we cannot flatten list, but we can count the number of elements.")
                df[column_flattened +
                    "_size"] = df[column_flattened].apply(length_with_nan)
                added_columns.append(column_flattened + "_size")
                if debug:
                    print("New column: " + column_flattened + "_size")
        else:
            if debug:
                print("Column " + column_flattened +
                      " is not a dictionnary nor a list!")
    return added_columns


def flatten_dataframe(df, drop=False, max_depth=3, debug=False):
    """
    Flatten all columns of a given dataframe, with a max_depth defined.
    """
    cols_to_flatten = df.columns
    cols_flattened = []
    k = 1
    while k <= max_depth:
        if debug:
            print("-" * 30)
            print("FLATENNING LEVEL " + str(k))
            print("-" * 30)
        # we use new columns to flatten them
        cols_to_flatten = flatten_columns(df, cols_to_flatten, drop)
        cols_flattened.append(cols_to_flatten)
        k += 1
        if len(cols_to_flatten) == 0:
            if debug:
                print("-" * 30)
                print("END NO MORE COLUMNS TO FLATTEN")
                print("-" * 30)
            break
    return cols_flattened
