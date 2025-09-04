## Description
"Mini-Blog Platform"
The backend of application where users can write posts (blogs), comment on them, and react to them.

## Features
### User authentication:
* Registration/authorization with [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html). 
* Ability to edit profile (store avatar on AWS S3; upload with presigned ur).

### Posts:
* User can create, edit and delete their own posts.
* Ability to like/dislike.
* Home page with a list of recent posts.
* Sort by popularity (by number of likes).
* Search by title/text.

### Comments:
* Authorized users can leave comments under posts in real time.(Django Channels)


## Technologies
* Python 3.13
* Django REST framework
* Django ORM
* Django Channels
* PostgreSQL 17