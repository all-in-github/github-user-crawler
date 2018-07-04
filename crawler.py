#!/usr/bin/env python3.6
#-*- coding=utf8

import requests
import sys
import time

START_USER = 'slow-is-fast'

# "followers_url": "https://api.github.com/users/slow-is-fast/followers",
# "following_url": "https://api.github.com/users/slow-is-fast/following{/other_user}",

followers_url = "https://api.github.com/users/%s/followers?page=%d"
following_url = "https://api.github.com/users/%s/following?page=%d"
USERNAME = "slow-is-fast"
PASSWORD = "knight514"


def followers(username, page=1):
    # if username is None:
        # username = START_USER
    url = followers_url % (username, page)
    print(url)
    data = http_get(url)
    for userinfo in data:
        # print(userinfo)
        name = userinfo['login']
        user_id = userinfo['id']
        followering = username
        upload_result({
            'follower_name': name,
            'follower_id': user_id,
            'following_name': username
        })
    return data


def followering(username, page=1):
    # if username is None:
        # username = START_USER
    url = following_url % (username, page)
    print(url)
    data = http_get(url)
    # print(data)
    for userinfo in data:
        # print(userinfo)
        name = userinfo['login']
        user_id = userinfo['id']
        followering = username
        upload_result({
            'follower_name': username,
            'following_id': user_id,
            'following_name': name
        })
    return data


def upload_result(payload=None):
    url = "http://yx.lemeng.net:40804/github_relations.php"
    payload['key'] = "9d5f5cf50519ecda6342c1b03f207"

    http_post(url, payload)


def http_get(url, proxy=None, headers=None):
    r = None
    while True:
        try:
            r = requests.get(url, headers=headers, timeout=180, auth=(USERNAME, PASSWORD))
        except Exception as e:
            print(e)
            pass
        if r.status_code == 200:
            break
        else:
            print(r.content)
            continue
        time.sleep(10)

    data = None
    try:
        data = r.json()
    except Exception as e:
        pass

    return data


def http_post(url, data=None, proxy=None, headers=None):
    r = requests.post(url, data=data)
    if r.status_code == 200:
        print('upload result OK')
        # print(r.content)
    else:
        print('upload result FAILED')


def get_task():
    r = requests.get('http://yx.lemeng.net:40804/gh_task.php')
    if r.status_code == 200:
        return r.content
    return ""


def update_task_status(username):
    url = "http://yx.lemeng.net:40804/gh_task_status.php?key=9d5f5cf50519ecda6342c1b037&name=%s" % username
    requests.get(url)


def main():
    while True:
        username = get_task()
        username = username.decode("utf-8")

        page = 1
        while True:
            fs = followers(username, page)
            time.sleep(10)
            if fs == [] or fs is None:
                break
            page = page + 1

        page = 1
        while True:
            fs = followering(username, page)
            time.sleep(10)
            if fs == [] or fs is None:
                break
            page = page + 1

        update_task_status(username)


if __name__ == '__main__':
    main()
