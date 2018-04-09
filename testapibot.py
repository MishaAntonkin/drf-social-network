from random import randrange, sample
from itertools import chain

import requests


NUMBER_OF_USERS = 10
MAX_POSTS_PER_USER = 20
MAX_LIKES_PER_USER = 20

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password123'


def generate_user_list(user_num):
    userlist = []
    for i in range(user_num):
        username = 'username_test' + str(i)
        password = 'password_test'

        r = requests.post('http://127.0.0.1:8000/user-api/users/create_user/', json={
            'username': username,
            'email': 'email_test{}@mail.net'.format(i),
            'password': password
        })

        if r.status_code == 201:
            url = r.json()['url']
            r = requests.post('http://127.0.0.1:8000/api-token-auth/', json={'username': username,
                                                                             'password': password})
            token = 'JWT {}'.format(r.json()['token'])
        else:
            raise Exception('cant create user')

        userlist.append({'token': token, 'url': url})

    return userlist


def generate_posts(user_list, max_posts):
    postlist = []
    for user in user_list:
        post_num = randrange(max_posts)
        for i in range(post_num):
            testpost = {'title': 'title_test', 'text': 'text_test'}
            r = requests.post('http://127.0.0.1:8000/user-api/posts/', headers={'Authorization': user['token']},
                              json=testpost)
            if r.status_code == 201:
                url = r.json()['url']
                postlist.append({'url': url})
            else:
                raise Exception('cant create post')

    return postlist


def generate_likes(user_list, user_posts, max_likes):
    likelist = []
    for user in user_list:
        likes_num = randrange(max_likes)
        rand_user_posts = sample(user_posts, likes_num)
        for rand_post in rand_user_posts:
            r = requests.post('http://127.0.0.1:8000/user-api/likes/', headers={'Authorization': user['token']},
                              json={'user': user['url'], 'post': rand_post['url']})
            assert (r.status_code == 201), 'Cant create user'
            url = r.json()['url']
            likelist.append(url)
    return likelist


def end_test(admin, password, user_list, like_list, post_list):
    def clean_db(admin_token, user_list, like_list, post_list):
        for i in chain(user_list, like_list, post_list):
            r = requests.delete(i['url'], headers={'Authorization': admin_token})
        print('Test data successfully cleaned')

    r = requests.post('http://127.0.0.1:8000/api-token-auth/', json={'username': admin, 'password': password})
    assert (r.status_code == 200)
    admin_token = f'JWT {r.json()["token"]}'
    clean_db(admin_token, user_list, like_list, post_list)


def main():
    user_list = generate_user_list()
    post_list = generate_posts(user_list, MAX_POSTS_PER_USER)
    like_list = generate_likes(user_list, post_list, MAX_LIKES_PER_USER)
    end_test(ADMIN_USERNAME, ADMIN_PASSWORD, user_list, like_list, post_list)

if __name__ == '__main__':
    main()
