from django.contrib.auth.models import AbstractUser
from django.db import models

# # Passenger
# id flights
# 1    1
# 2     1
# # Flight
# id passengers
# 1     1,2


# User
# id following followers
# 1     2
# 2                 1,3
# 3     2


class User(AbstractUser):
    following = models.ManyToManyField("User", blank=True, related_name="followers")

class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def serialize(self):

        return {
            "id": self.id,
            "user": self.author.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "numlikes": self.likes.count(),
        }

class Like(models.Model):
    createddatetime= models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name ="likes")

# User table
# id following followers   likes
# 1   2,3,4
# 2                1         1,2,3,4,6
# 3                1
# 4                1

# Like table
# id user     post
# 1      2     1
# 2      2     2
# 3      2     3
# 4      2     4
# 5      1     5
# 6      2     5
# 7      3     5

     

# # User table
# id likes   followgiver   followreceiver
# 1    -      
# 2    [1]

# Post table
# id  likes
#  1   1
#  2   2
#  3   3
#  4   4
#  5   5,6,7

