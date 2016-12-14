"""
Entry point for raw requests. Can be used to compute queries of API parts for which specific methods have not been yet implemented, and still benefit from the core methods.

for instance, client.raw()
"""


def raw(client, url, extra_params=None, verbose=False):
    return client._get(url=url, extra_params=extra_params, verbose=verbose)
