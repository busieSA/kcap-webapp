from functools import wraps

_sitemap_entries = {}

def sitemap_page(
        changefreq="monthly",
        priority=0.5
):
    def decorator(func):

        _sitemap_entries[func.__name__] = {
            "changefreq" : changefreq,
            "priority": priority
        }

        @wraps(func)

        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        return wrapper
    
    return decorator

    def get_sitemap_entries():
        return _sitemap_entries.copy()
    
    #check fot this file improvement later on:

