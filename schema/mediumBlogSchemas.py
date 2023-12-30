import os
import requests
from dotenv import load_dotenv

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

    blog_details = get_blog_details_by_url(bloggerUrl, api_key)
    extracted_data = [] 

    if blog_details:
        blog_id = blog_details['id']

        blog_posts = get_blog_posts(blog_id, api_key)
        if blog_posts:
        
            for post in blog_posts['items']:
                title = post['title']
                published_date = post['published']
                updated_date = post['updated']
                url = post['url']

                post_data = {
                    "title": title,
                    "published_date": published_date,
                    "updated_date": updated_date,
                    "url": url
                }

                extracted_data.append(post_data) 

    return extracted_data