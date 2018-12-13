import json
import urllib
import bs4
class Blog:
    '''Class representing a single blogger blog'''
    def __init__(self,blogURL,key='AIzaSyDYOBCkUabgqxYcvRLO--SWmOzyywbREf0'):
        '''Create a new blog object'''
        self.key=key
        self.url=blogURL
        req='https://www.googleapis.com/blogger/v3/blogs/byurl'+'?'+urllib.parse.urlencode({'key':key,'url':blogURL})
        blogInfo=apiRequest(req)
        self.id=blogInfo['id']
    
    def getAllPosts(self):
        '''Retrieve all posts associated with this blog'''
        req='https://www.googleapis.com/blogger/v3/blogs/'+self.id+'/posts'+'?key='+self.key
        posts=apiRequest(req)
        allPosts=posts['items']
        #Each request only returns 10 posts, to get the next set of posts we need to resubmit the request with a token attached as a pageToken parameter
        while 'nextPageToken' in posts:
            newReq=req+'&pageToken='+posts['nextPageToken']
            posts=apiRequest(newReq)
            allPosts.extend(posts['items'])

        return allPosts

def apiRequest(req):
    '''Submit an http GET request specified by req and return result as a string'''
    return json.loads(urllib.request.urlopen(req).read())

def savePosts(filename,posts):
    '''Save list of posts posts to the file specified by filename, posts should be the type of list produced by Blog.getAllPosts()'''
    file=open(filename,mode='w')
    for post in posts:
        for key in post:
            #Use html parser to make text more readable
            soup=bs4.BeautifulSoup(str(post[key]), 'html.parser')
            #Strip extra newlines
            entryText=soup.get_text(' ')
            entryTextLines=entryText.split('\n')
            entryTextLines=[line for line in entryTextLines if line]
            strippedText='\n'.join(entryTextLines)
            file.write(key+': '+strippedText+'\n')
        file.write('\n')
    file.close()

def savePostsIndividually(directory,posts):
    '''Save list of posts posts to the directory specified by directory as individual files,
    posts should be the type of list produced by Blog.getAllPosts()'''
    #make sure directory ends in a file separator
    if directory[-1]!='/':
        directory=directory+'/'
    for post in posts:
        file=open(directory+post['published']+'.txt','w')
        contentSoup=bs4.BeautifulSoup(post['content'], 'html.parser')
        content=contentSoup.get_text(' ')
        #strip extra newlines
        contentLines=content.split('\n')
        contentLines=[line for line in contentLines if line]
        strippedContent='\n'.join(contentLines)
        file.write('title: '+post['title']+'\n\n')
        file.write(strippedContent)
        file.close()
