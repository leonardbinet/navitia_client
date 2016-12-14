import os

from src.client import Client


def etl_sncf(api_paths, user, page_limit=100, count=100, debug=False):
    """
    Take a list of paths to extract, and save all data in subfolder.
    """
    for requested_path in api_paths:
        # Create Data directory if it doesn't exist
        directory = os.path.join("Data", requested_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Compute request
        request = Client(user)
        request._get_multiple_pages(
            page_limit=page_limit, count=count, url=requested_path, verbose=True)
        # Write request log
        # Parse results if sucessful
        # parser = Parser(request.results, requested_path)
        # parser.parse()
        # Print some information
        # parser.explain()
        # Write it on disk
        # parser.write_all(directory)
