import requests
import html2text
import os
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Referer': 'https://csdn.net',
}

csdn_urls = [
    {
        "url": "https://feelang.blog.csdn.net/article/details/126981050",
        "name": "installing",
    }, {
        "url": "https://feelang.blog.csdn.net/article/details/126989525",
        "name": "getting-started",
    }, {
        "url": "https://feelang.blog.csdn.net/article/details/126995734",
        "name": "liquid",
    }, {
        "url": "https://feelang.blog.csdn.net/article/details/127015390",
        "name": "font-matter-and-yaml",
    }, {
        "url": "https://feelang.blog.csdn.net/article/details/127033429",
        "name": "layouts",
    }, {
        "url": "https://feelang.blog.csdn.net/article/details/127050529",
        "name": "includes",
    }, {
        "url": "https://feelang.blog.csdn.net/article/details/127055114",
        "name": "blogs",
    }, {
        "url": "https://feelang.blog.csdn.net/article/details/127056148",
        "name": "collections",
    }, {
        "url": "https://feelang.blog.csdn.net/article/details/127056331",
        "name": "data-files",
    },
]

for idx, link in enumerate(csdn_urls, start=1):
    response = requests.get(link['url'], headers=headers)
    bs = BeautifulSoup(response.content, 'html.parser')
    title = bs.find('h1', {'class': 'title-article'})

    content = bs.find('div', {'id': 'article_content'})
    content = html2text.html2text(str(content))

    # Convert to markdowns
    file_name = link['name']
    output_dir = os.path.join(os.getcwd(), '_jekyll/', f'{file_name}.md')
    print(output_dir)
    with open(output_dir, 'w') as f:
        f.write('---\n')
        f.write(f'title: {title.text}\n')
        f.write(f'excerpt: \n')
        f.write(f'lesson: {idx}\n')
        f.write('---\n')
        f.write(content)
