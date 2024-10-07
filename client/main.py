import requests

url = 'http://localhost:3000/api/list_blogs'
blog_url = 'http://localhost:3000/api/blog'
# get_blogs = requests.get(url, params={'id': 1}, json={'query': 'hello world'})
get_blog = requests.get(blog_url, params={'id': 1})
print(get_blog.json())