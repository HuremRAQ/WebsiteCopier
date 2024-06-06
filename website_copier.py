import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class WebsiteCopier:
    def __init__(self, base_url, output_dir):
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited_urls = set()

    def make_dirs(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def save_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(content)

    def get_filename_from_url(self, url):
        parsed_url = urlparse(url)
        path = parsed_url.path
        if path.endswith('/'):
            path += 'index.html'
        if not os.path.splitext(path)[1]:
            path += '.html'
        return os.path.join(self.output_dir, path.lstrip('/'))

    def download_resource(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")
            return None

    def save_resource(self, url):
        resource_content = self.download_resource(url)
        if resource_content:
            resource_path = self.get_filename_from_url(url)
            self.make_dirs(os.path.dirname(resource_path))
            self.save_file(resource_path, resource_content)

    def process_html(self, url, content):
        soup = BeautifulSoup(content, 'html.parser')

        # Update resources URLs
        for tag in soup.find_all(['img', 'link', 'script']):
            if tag.name == 'img' and tag.get('src'):
                tag['src'] = self.update_resource_url(url, tag['src'])
            elif tag.name == 'link' and tag.get('href'):
                tag['href'] = self.update_resource_url(url, tag['href'])
            elif tag.name == 'script' and tag.get('src'):
                tag['src'] = self.update_resource_url(url, tag['src'])

        # Save updated HTML
        html_path = self.get_filename_from_url(url)
        self.make_dirs(os.path.dirname(html_path))
        self.save_file(html_path, soup.prettify('utf-8').encode('utf-8'))

        # Follow links to other pages
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(url, a_tag['href'])
            if self.should_visit_url(link):
                self.visited_urls.add(link)
                self.copy_website(link)

    def update_resource_url(self, base_url, resource_url):
        full_url = urljoin(base_url, resource_url)
        resource_path = self.get_filename_from_url(full_url)
        relative_path = os.path.relpath(resource_path, os.path.dirname(self.get_filename_from_url(base_url)))
        self.save_resource(full_url)
        return relative_path

    def should_visit_url(self, url):
        return url.startswith(self.base_url) and url not in self.visited_urls

    def copy_website(self, url):
        print(f'Copying {url}')
        html_content = self.download_resource(url)
        if html_content:
            self.process_html(url, html_content)

if __name__ == '__main__':
    base_url = input('Enter the base URL of the website: ')
    output_dir = input('Enter the output directory: ')
    copier = WebsiteCopier(base_url, output_dir)
    copier.copy_website(base_url)
    print('Website copy completed.')
