Main functions of the utility:
Downloading HTML content of pages.
Downloading and saving related resources (images, styles, scripts).
Creating a local copy of the site structure.

The ‘requests’ and ‘beautifulsoup4’ libraries will need to be installed for the utility to work. You can install them using the commands:
pip install requests
pip install beautifulsoup4

WebsiteCopier class initialisation:

‘__init__’: Initialises a base URL, a directory to save, and a set of visited URLs.
Directory creation:

‘make_dirs’: Creates directories if they don't exist.
Saving files:

‘save_file’: Saves content to the specified path.
Getting a filename from a URL:

‘get_filename_from_url’: Converts the URL to a local path for saving.
Downloading a resource:

‘download_resource’: Downloads the content of the URL.
Saving the resource:

‘save_resource’: Saves the downloaded resource to a local path.
HTML content processing:

‘process_html’: Updates the resource URLs in the HTML content and saves it. Follows links to other pages.
Updates the resource URL:

‘update_resource_url’: Converts the resource URL to a relative path and saves the resource.
Checks if the URL should be visited:

‘should_visit_url’: Checks if the URL should be visited (whether it is within the base URL and has not already been visited).
Copy website:

‘copy_website’: The basic method for copying a website. Loads the HTML content of the page, processes it and saves it.

support the author:
PayPal: bratavmaskah@gmail.com
USDT TRC-20: TV3LpYeQE2t96f9HfmMY4hqjQXstVgn7tt
