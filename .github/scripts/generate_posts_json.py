import os
import json
from datetime import datetime
from bs4 import BeautifulSoup

def parse_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
        title = soup.title.string if soup.title else 'Untitled'
        date_meta = soup.find('meta', attrs={'name': 'blog-date'})
        date = date_meta['content'] if date_meta else None
        return {
            'filename': os.path.basename(file_path),
            'title': title,
            'date': date
        }

def generate_posts_json():
    posts_dir = 'posts'
    posts = []

    for filename in os.listdir(posts_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(posts_dir, filename)
            post_info = parse_html_file(file_path)
            if post_info['date']:
                posts.append(post_info)

    # Sort posts by date (newest first)
    posts.sort(key=lambda x: datetime.strptime(x['date'], '%d-%m-%Y'), reverse=True)

    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    generate_posts_json()
