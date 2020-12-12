from selenium import webdriver
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import pymysql


def get_video_path(information, num):
    # 获取视频地址、用户头像、视频点赞数
    html = etree.HTML(information)
    # videoname = html.xpath("//p[@class='video-info-title']/text()")[0]
    # videoshotby = html.xpath("//span[@class='profile-user-name-title']/text()")[0]
    videoUrl = html.xpath("//video[@class='player-video']/@src")[0]
    author = html.xpath("//img[@class='avatar-img']/@src")[0]
    likenum = html.xpath("//div[@class='interactive-item like-item']/span[@class='item-text']/text()")[0]

    json_info = '''  {\n    id:%d,\n    videoUrl: "%s",\n    poster:"https://image.pearvideo.com/cont/20201104/cont-1705200-12501405.jpg",\n    likenum: "%s",\n    author:"%s",\n    playing:false\n  },\n''' % (num,videoUrl,likenum,author)
    # print(json_info)
    return json_info.encode()


def get_ks():
    # 连接数据库
    # db = pymysql.connect(user='root', password='189809nkq', host='localhost', \
    #                      port=3306, database='finalwork', charset='utf8mb4')
    # cs = db.cursor()
    # 打开文件
    video_info = open('./data.js', mode='ab')
    # 设置中文
    options = Options()
    options.add_argument('lang=zh_CN.UTF-8')
    # 设置无界面
    options.add_argument('--headless')
    # 请求头
    headers = "user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " \
              "Chrome/81.0.4044.129 Safari/537.36' "
    options.add_argument(headers)
    # chrome_driver地址
    path = r'/Applications'
    url = 'https://video.kuaishou.com/featured/'

    # 请求网站
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    # 等待视频链接加载完成
    time.sleep(1.5)
    # video = driver.find_element_by_class_name('player-video')
    num = 2
    num_big = 3
    try:
        information = driver.page_source
        video_info.write(get_video_path(information, num))
        # cs.execute(get_video_path(information, num=10))
        # db.commit()

        # <section class="main short-main">
        #  <div class="main-content">
        #   <div class="short-video-detail" data-v-70856ae8>
        #    <div class="short-video-detail-container" data-v-70856ae8>
        #     <div class="short-video-wrapper" data-v-9c8e06ee data-v-70856ae8>
        #      <div class="video-switch" data-v-3b7e9867 data-v-9c8e06ee>
        #       <div class="switch-item video-switch-last" data-v-3b7e9867></div>
        #        <div class="switch-item video-switch-next" data-v-3b7e9867></div>
        try:
            right = driver.find_element_by_xpath("//section[@class='main short-main']\
            /div[@class='main-content']\
                /div[@class='short-video-detail']\
                    /div[@class='short-video-detail-container']\
                        /div[@class='short-video-wrapper']\
                            /div[@class='video-switch']\
                                /div[@class='switch-item video-switch-next']")
        except:
            print('节点未获取')
            right = ''
            raise Exception("can't get Node")
        while right:
            print('成功获取下一个视频')
            ActionChains(driver).click(right).perform()
            time.sleep(10)
            information = driver.page_source
            video_info.write(get_video_path(information, num_big))
            video_info.flush()
            # cs.execute(get_video_path(information, num))
            # db.commit()
            num_big += 1
    except:
        print('获取下一个视频失败')
    finally:
        # 关闭页面、数据库
        # cs.close()
        # db.close()
        video_info.close()
        driver.close()
        driver.quit()


if __name__ == '__main__':
    get_ks()