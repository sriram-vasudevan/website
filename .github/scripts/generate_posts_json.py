import os
import sys
import time
import json
import re
from pathlib import Path
from datetime import datetime
import markdown
from bs4 import BeautifulSoup
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MarkdownConverter(FileSystemEventHandler):
    def __init__(self, drafts_dir, posts_dir):
        self.drafts_dir = drafts_dir
        self.posts_dir = posts_dir
        Path(posts_dir).mkdir(exist_ok=True)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            self.process_markdown_file(event.src_path)

    def process_markdown_file(self, md_file_path):
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        html_content = self.convert_md_to_html(md_content)
        
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string if soup.title else 'Untitled'
        
        filename = self.generate_filename(title)
        
        output_path = os.path.join(self.posts_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Generated file: {filename}")
        self.generate_posts_json()

    def convert_md_to_html(self, md_content):
        # Split the content into title+date and body
        parts = md_content.split('\n', 2)
        title_date = parts[0].strip()
        body = parts[2] if len(parts) > 2 else ''

        # Extract title and date
        title_match = re.match(r'(.*?)\s*(\d{4}-\d{2}-\d{2})?$', title_date)
        title = title_match.group(1).strip() if title_match else 'Untitled'
        date = title_match.group(2) if title_match and title_match.group(2) else ''

        # Convert markdown body to basic HTML
        html_body = markdown.markdown(body, extensions=['extra'])
        
        soup = BeautifulSoup(html_body, 'html.parser')
        
        # Add class='responsive' to all img tags
        for img in soup.find_all('img'):
            img['class'] = img.get('class', []) + ['responsive']
        
        # Convert YouTube links to iframe
        for a in soup.find_all('a', href=re.compile(r'https?://(?:www\.)?youtube\.com/watch\?v=')):
            iframe = soup.new_tag('iframe', 
                                  src=f"https://www.youtube.com/embed/{a['href'].split('v=')[1]}",
                                  frameborder="0",
                                  allowfullscreen=True)
            iframe['class'] = ['youtube-video']
            a.replace_with(iframe)
        
        # Create the full HTML structure
        full_html = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <meta name="blog-date" content="{date}">
            <link rel="stylesheet" href="../styles.css">
        </head>
        <body>
            <main>
                <a href="../index.html" class="back-link">← Back to Home</a>
                <br>
                <article>
                    <h1>{title}</h1>
                    {soup.prettify()}
                </article>
                <br>
            </main>
        </body>
        </html>
        """
        
        return BeautifulSoup(full_html, 'html.parser').prettify()

    def generate_filename(self, title):
        return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') + '.html'

    def parse_html_file(self, file_path):
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

    def generate_posts_json(self):
        posts = []
        for filename in os.listdir(self.posts_dir):
            if filename.endswith('.html'):
                file_path = os.path.join(self.posts_dir, filename)
                post_info = self.parse_html_file(file_path)
                if post_info['date']:
                    posts.append(post_info)
        # Sort posts by date (newest first)
        posts.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
        with open('posts.json', 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print("Updated posts.json")

if __name__ == "__main__":
    drafts_dir = 'drafts'
    posts_dir = 'posts'
    
    event_handler = MarkdownConverter(drafts_dir, posts_dir)
    observer = Observer()
    observer.schedule(event_handler, path=drafts_dir, recursive=False)
    observer.start()

    print(f"Watching for changes in {drafts_dir}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
