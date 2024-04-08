import os
import requests
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()

def get_blog_details_by_url(blog_url, api_key):
    
    api_endpoint = f'https://www.googleapis.com/blogger/v3/blogs/byurl?url={blog_url}&key={api_key}'
    
    response = requests.get(api_endpoint)
    
    if response.status_code == 200:
        blog_details = response.json()
        return blog_details
    else:
        print(f"Failed to fetch blog details. Status code: {response.status_code}")
        return None

def get_blog_posts(blog_id, api_key):
    
    api_endpoint = f'https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts?key={api_key}'
    
    response = requests.get(api_endpoint)
    
    if response.status_code == 200:
        blog_posts = response.json()
        return blog_posts
    else:
        print(f"Failed to fetch blog posts. Status code: {response.status_code}")
        return None

api_key = os.getenv('Blogger_API_KEY')

def extract_blogger_posts(bloggerUrl):

    result = {'blog type': 'Blogger', 'posts': []}
    blog_details = get_blog_details_by_url(bloggerUrl, api_key)

    if blog_details:
        blog_id = blog_details['id']

        blog_posts = get_blog_posts(blog_id, api_key)
        if blog_posts:
        
            for post in blog_posts['items']:
                title = post['title']
                published_date = post['published']
                updated_date = post['updated']
                url = post['url']

                post = {
                    "title": title,
                    "published_date": published_date,
                    "updated_date": updated_date,
                    "url": url
                }

                result['posts'].append(post)

    return result

def extract_medium_posts(mediumUrl):

    result = {'blog type': 'Medium', 'posts': []}
    response = requests.get(mediumUrl)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        container = soup.find('div', class_='l ae')

        if container:
            articles = container.find_all('article')

            for index, article in enumerate(articles):

                post = {}

                title = article.find('h2', class_='be lq lr dq ls lt lu lv ds lw lx ly lz ma mb mc md me mf mg mh mi mj mk ml mm mn hb hd he hg hi bj').text.strip()
                post['title'] = title
                date = article.find('p', class_='be b bf z dn').find('span', class_='').text.strip()
                post['date'] = date
                blogurl = article.find('div', class_='ab q').find('a', class_='').get('href')
                endindex = blogurl.find('?')
                base_url = mediumUrl + blogurl[:endindex]
                post['url'] = base_url

                result['posts'].append(post)

        else:
            print("Error: Unable to find the container for articles")
    else:
        print(f"Error: Failed to fetch page (status code {response.status_code})")
        print(response.content)  

    return result;
