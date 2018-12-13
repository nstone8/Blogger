import json
import urllib
class blog:
    def __init__(self,blogURL,key='AIzaSyDYOBCkUabgqxYcvRLO--SWmOzyywbREf0'):
        self.key=key
        self.url=blog
        req='https://www.googleapis.com/blogger/v3/blogs/byurl'+'?'+urllib.parse.urlencode({'key':key,'url':blogURL})
        blogInfo=apiRequest(req)
        self.id=blogInfo['id']
    
    def getAllPosts(self):
        req='https://www.googleapis.com/blogger/v3/blogs/'+self.id+'/posts'+'?key='+self.key
        posts=apiRequest(req)
        allPosts=posts['items']

        while 'nextPageToken' in posts:
            newReq=req+'&pageToken='+posts['nextPageToken']
            posts=apiRequest(newReq)
            allPosts.extend(posts['items'])

        return allPosts

def apiRequest(req):
    return json.loads(urllib.request.urlopen(req).read())

def savePosts(filename,posts):
    file=open(filename,mode='w')
    for post in posts:
        for key in post:
            file.write(key+': '+str(post[key])+'\n')
        file.write('\n')
