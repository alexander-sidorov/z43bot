from config import settings

BLOG_URL = settings.blog_url

URL_API = f"{BLOG_URL}/api"
URL_API_USER = f"{BLOG_URL}/api/user"
URL_API_BLOG = f"{BLOG_URL}/api/blog/post"

CONTENT_TYPE = "application/vnd.api+json"
