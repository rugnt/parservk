from abc import ABC, abstractmethod
from functools import partial
from time import sleep
from handlers import *

import requests

class Option:
    version = "5.131"
    token = open("token.txt","tr").read()

class Request(Option):
    address = "https://api.vk.com/method/"

    def __init__(self,method):
        self.address = self.address + method

    def __call__(self,**kwargs) -> dict:
        return requests.get(self.address,
                params=kwargs | {\
                'access_token': self.token,
                'v':self.version
            }).json()

class Post:

    def __init__(self,data):
        self.data = data
        
    def __getattr__(self,key):
        try:
            return self.data[key]
        except KeyError:
            return None

    def __repr__(self):
        return f"<class Post, date={self.data['date']}>"

    def __str__(self):
        return self.__repr__()

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,value):
        self.data[key] = value

class Posts:

    def __init__(self,json):
        self.data = []
        self.count = json["response"]["count"]

        for data in json["response"]["items"]:
            self.data.append(Post(data))

    def pop(self,i):
        return self.data.pop(i)

    def extend(self,posts):
        return self.data.extend(posts.data)

    def sort(self,**kwargs):
        return self.data.sort(**kwargs)

    def __getitem__(self,pos):
        return self.data[pos]

    def __setitem__(self,pos,value):
        self.data[pos] = value

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return len(self.data)

    def __add__(self,obj):
        return self.data + obj.data


class Group:

    """
    Класс, отображающий группу вк
    """
    handler = None

    def __init__(self,domain,count):
        parsing = partial(
            Request("wall.get"),
            domain=domain,
            count=100,
        )
        posts = Posts(parsing(offset=0))
        offset = 100
        while count > offset:
            try:
                print(offset)
                posts.extend(Posts(parsing(offset=offset)))
                offset += 100
                sleep(0.5)
            except KeyError:
                sleep(1)

        self.posts = posts
        self.count = posts.count

    def __getitem__(self,pos):
        return self.posts[pos]

    def start_handler(self):
        self.handler(self.posts)

    def __add__(self,obj):
        groups = Groups(self.posts + obj.posts)
        groups.count = self.count + obj.count
        groups.handler = self.handler + obj.handler
        return groups

class PostGroup:
    posting = Request("wall.post")

    def __init__(self,domain):
        self.domain = domain

    def get_attachments(self,attachments):
        lst = []

        for attachment in attachments:
            try:
                tp = attachment["type"]
                lst.append(f'{tp}{attachment[tp]["owner_id"]}_{attachment[tp]["id"]}')
            except KeyError:
                pass

        return ",".join(lst)

    def add_post(self,post):
        print(post.attachments)
        self.posting(
            attachments=self.get_attachments(post.attachments),
            message=post.text,
            owner_id=self.domain
        )

    def add_group(self,group,count=31243243):
        for post in group:
            print(post)
            if count <= 0:
                break
            self.add_post(post)
            count -= 1
            sleep(0.5)

class Groups(Group):
    
    def __init__(self,data):
        self.posts = data


if __name__ == "__main__":
    a = Group("netflix_show",100)
    b = Group("donetsk",100)
    a.handler = Sorted(False)
    b.handler = Sorted(True)
    c = a + b
    c.start_handler()
    for i in c:
        print(i)
    #a.sortedset(True)
    #a.filterset([],[])
    #a.filter()
    #a.sorted()
    #pg = PostGroup(-209190157)
    #pg.add_group(a,3)
    #for i in a:
    #    print(i.text)







