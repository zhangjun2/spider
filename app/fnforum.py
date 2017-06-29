
import urllib
import re
import time
from urllib.request import Request

import requests
from bs4 import BeautifulSoup

from app.database import db_session
from app.models import ForumPost, ForumPostDetail, User

_author__ = 'ZHANGJUN'
#-*- coding:utf-8 -*-
# 人像论坛图片爬取

fn_base_url = 'http://bbs.fengniao.com'
post_detail_base_url = 'http://bbs.fengniao.com/forum/showthread.php?'
#论坛基础地址
baseurl = "http://bbs.fengniao.com/forum/forumdisplay.php?"
user_info_url = "https://my.fengniao.com/info.php?"
# f=101&\ #101代表人像
# type=list&\ #暂不知
# order=desc&\    #倒序
# sort=lastpost&\ #按什么排序
# page=3  #页码
ISOTIMEFORMAT='%Y%m%d%H%M%S'


class fnForum:

    def __init__(self, f='101', type='list', order='desc', sort='lastpost'):
        self.baseurl = "http://bbs.fengniao.com/forum/forumdisplay.php?"
        self.f = f
        self.type = type
        self.order = order
        self.sort = sort

    def get_crawl_url(self, page):
        if page == 1:
            return baseurl + 'f=' + self.f + '&type=' + self.type + '&order=' + self.order \
                                    + '&sort=' + self.sort
        else:
            return baseurl + 'f=' + self.f + '&type=' + self.type + '&order=' + self.order \
                                    + '&sort=' + self.sort + '&page=' + str(page)

    def post_request(self, url, data=None):
        # request = Request(url,data=data)
        # response = urllib.request.urlopen(request)
        html = requests.get(url, data).text
        print(url)
            # response.read().decode('utf-8')
        # print(html)
        return html

    def crawl_post(self, page):
        html = self.post_request(self.get_crawl_url(page))
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find_all('table', class_='dkopex', style=re.compile('b'))
        if table:
            trs = table[0].find_all('tr')
            for tr in trs:
                author = tr.find('td', class_='author')
                common = tr.find('td', class_='common')
                post_user_href = author.find('a').get('href')
                post_user_nick = author.find('a').contents
                post_user_id = post_user_href.split('/')[3].strip()
                post_detail_href = common.find('h3').find('a').get('href')
                post_title = common.find('h3').find('a').contents
                post_id = post_detail_href.split('/')[2].split('.')[0]
                post_publish_time = author.find('p').contents
                child_a = common.find_all('a')
                post_detail_href_children = ''
                for index, a in enumerate(child_a):
                    if index > 0:
                        post_detail_href_children += (a.get('href')+',')

                post = ForumPost(post_id, post_title[0], post_user_id, post_detail_href,
                                 post_user_nick[0], post_user_href,post_detail_href_children,post_publish_time[0])
                # self.crawl_user_info(post_user_id)
                # self.crawl_post_detail(post.post_id, post.post_user_id)
                try:
                    db_session.add(post)
                    db_session.commit()
                    self.crawl_user_info(post_user_id)
                    self.crawl_post_detail(post.post_id, post.post_user_id)
                except Exception as e:
                    db_session.rollback()
                    print('add post exception:', e)
                    pass

    def crawl_user_info(self, user_id):
        html = self.post_request(user_info_url + 'userid=' + user_id)
        soup = BeautifulSoup(html, 'html.parser')
        info_p = soup.find('div', class_='content').find('span').find_all('p')
        user_name = info_p[0].contents[0].partition('：')[2]
        user_nick = info_p[1].contents[0].partition('：')[2]
        user_sex = info_p[2].contents[0].partition('：')[2]
        user_address = info_p[3].contents[0].partition('：')[2]
        user_weibo = info_p[4].contents[0].partition('：')[2]
        user_qq = info_p[5].contents[0].partition('：')[2]
        user = User(user_id, user_nick=user_nick, user_name=user_name, user_sex=user_sex, user_weibo=user_weibo,
                    user_qq=user_qq, user_address=user_address)
        try:
            db_session.add(user)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            print('add user exception:',e)
            pass

    def crawl_post_detail(self, post_id, user_id, page=None):
        value={}
        value['t'] = post_id
        value['user_id'] = user_id
        value['page'] = page
        html = self.post_request(post_detail_base_url, value)
        soup = BeautifulSoup(html,'html.parser')
        tables = soup.find_all('table', class_='subList')
        pageNum =soup.find('div',class_='pageNum')
        pages = pageNum.find_all('a', target='_self')
        # print(tables[0])
        for table in tables:
            trs = table.find_all('tr')
            div_mainTitleBox = trs[0].find('div',class_='mainTitleBox')
            td_postSide = trs[0].find('td',class_='postSide')
            post_lc_num = div_mainTitleBox.find('span', class_='floor').contents[0]
            post_lc_time = div_mainTitleBox.find('span', class_='time').contents[0]
            post_lc_user_id = td_postSide.find('p',class_='contact').find('a',class_='private').get('uid')
            post_lc_user_nick = td_postSide.find('p',class_='contact').find('a',class_='private').get('uname')
            img_tag = trs[1].find('img', class_='thread-img')
            post_lc_img_url = ''
            if img_tag:
                post_lc_img_url = img_tag.get('src')
            infos = trs[1].find_all('p',class_='info')
            post_lc_img_info = ''
            if infos and len(infos) > 1:
                post_lc_img_info = infos[1].contents[0]
            # print(post_lc_num,'楼------', post_lc_time,'userid---',post_lc_user_id,'username-----',post_lc_user_nick,
            #       'img---',post_lc_img_url,'info---', post_lc_img_info)
            # print('================================================================================================')
            post_lc = ForumPostDetail(post_id, post_lc_num, user_id, post_lc_time=post_lc_time,
                                      post_lc_user_nick=post_lc_user_nick, post_lc_img_info=post_lc_img_info,
                                      post_lc_img_url=post_lc_img_url)
            try:
                db_session.add(post_lc)
                db_session.commit()
                self.save_post_detail_img(post_lc_img_url, post_lc.post_lc_user_id)
            except Exception as e:
                db_session.rollback()
                print('add post detail exception:',e)
                pass
        # if pages:
        #     for p in pages:
        #         page_urls = p.get('href').replace('?', post_detail_base_url)
        #         print('pageurl:', p.get('href'))
        #
        #         # self.parse_post_img(html)

    def save_post_detail_img(self, imgurl, user_id):
        data = urllib.request.urlopen(imgurl)
        t = str(time.strftime(ISOTIMEFORMAT))
        filename = 'D:\soft\\fnsy\\img\\' + t + '-' + user_id + '.jpg'
        with open(filename, 'wb') as f:
            f.write(data.read())


def start_crawl(maxpage):
    fn = fnForum()
    for x in range(2, maxpage):
        fn.crawl_post(x)

