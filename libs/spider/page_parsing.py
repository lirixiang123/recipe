import requests
from bs4 import BeautifulSoup
import time
import pymysql
from multiprocessing import Pool

from pandas import DataFrame

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

#抓取每一页所有菜谱
def get_links_from(channel, pages):
    #http://www.meishij.net/china-food/caixi/qingzhencai/?&page=2
    list_view = '{}?&page={}'.format(channel, str(pages))
    wb_data = requests.get(list_view, headers = header)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # print(soup.find('div',class_='searchform_div')('input')[0]['placeholder'])
    if soup.find('div',class_='searchform_div'):
        try:
            nav = soup.find('div',class_='searchform_div')('input')[0]['placeholder']
        except:
            nav = None
    else:
        pass

    if soup.find('div', class_='i_w'):
        for link in soup.select('.listtyle1'):
            try:
                item_link = link.select('a')[0]['href'] #获取链接
            except:
                item_link = None
            try:
                image_link = link.select('a > img')[0]['src'] #获取链接
            except:
                image_link = None
            try:
                title = link.select('.c1')[0]('strong')[0].text #获取标题
            except:
                title = None
            try:
                comment = link.select('.c1')[0]('span')[0].text.split()[0] #获取评论数
            except:
                comment = '0'
            try:
                likes = link.select('.c1')[0]('span')[0].text.split()[-2] #获取人气数
            except:
                likes = '0'
            try:
                #加判断，去除不规则格式的老文章
                if comment.isdigit() and likes.isdigit():

                    item = []
                    image = []
                    t = []
                    com = []
                    like = []
                    na = []
                    item.append(item_link[0])
                    image.append(image_link[0])
                    t.append(title[0])
                    com.append(int(comment[0]))
                    like.append(int(likes[0]))
                    na.append(nav[0])

                    dict_data = {
                        'item_url':item,
                        'image_url':image,
                        'title':t,
                        'comment':com,
                        'likes':like,
                        'nav':na
                    }

                    data=DataFrame(dict_data)

                    DataFrame(data).to_excel(r'C:\Users\86132\Desktop\recipe\recipe.xlsx',sheet_name='Sheet1')
                    # db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='cook', charset='utf8')
                    # cursor = db.cursor()
                    # sql="""insert into item(url,image_url,title,comment,likes,series) values(%s,%s,%s,%s,%s,%s)"""
                    # cursor.execute(sql,[item_link,image_link,title,int(comment),int(likes),nav])
                    # db.commit()
                    # cursor.close()
                    # db.close()

                else:
                    pass
            except Exception as e:
                print('数据出错')
                print(e)
            try:
                print({'url':item_link,'image_url':image_link, 'title':title, 'comment':int(comment),\
                                         'likes':int(likes), 'series':nav})
            except:
                print('标题出错')
    else:
        pass

#5大类链接列表
# head_list = '''
#     http://www.meishij.net/chufang/diy/
#     http://www.meishij.net/china-food/caixi/
#     http://www.meishij.net/china-food/xiaochi/
#     http://www.meishij.net/chufang/diy/guowaicaipu1/
#     http://www.meishij.net/hongpei/
# '''

#获取所有类目链接
# def get_total_urls(head_urls):
#     res = requests.get(head_urls, headers = header)
#     soup = BeautifulSoup(res.text, 'lxml')
#     link = soup.select('.listnav_dl_style1 > dd > a')
#     for i in link:
#         url = i.get('href')
#         name = i.text
#         print({'url':url,'name':name})
#     return url
# total_url = []
# for i in head_list.split():
#     total_url.append(get_total_urls(i))
# print(total_url)
#全部链接
total_url = '''{'url': 'http://www.meishij.net/chufang/diy/jiangchangcaipu/', 'name': '家常菜'}
{'url': 'http://www.meishij.net/chufang/diy/sijiacai/', 'name': '私家菜'}
{'url': 'http://www.meishij.net/chufang/diy/langcaipu/', 'name': '凉菜'}
{'url': 'http://www.meishij.net/chufang/diy/haixian/', 'name': '海鲜'}
{'url': 'http://www.meishij.net/chufang/diy/recaipu/', 'name': '热菜'}
{'url': 'http://www.meishij.net/chufang/diy/tangbaocaipu/', 'name': '汤粥'}
{'url': 'http://www.meishij.net/chufang/diy/sushi/', 'name': '素食'}
{'url': 'http://www.meishij.net/chufang/diy/jiangliaozhanliao/', 'name': '酱料蘸料'}
{'url': 'http://www.meishij.net/chufang/diy/weibolucaipu/', 'name': '微波炉'}
{'url': 'http://www.meishij.net/chufang/diy/huoguo/', 'name': '火锅底料'}
{'url': 'http://www.meishij.net/chufang/diy/tianpindianxin/', 'name': '甜品点心'}
{'url': 'http://www.meishij.net/chufang/diy/gaodianxiaochi/', 'name': '糕点主食'}
{'url': 'http://www.meishij.net/chufang/diy/ganguo/', 'name': '干果制作'}
{'url': 'http://www.meishij.net/chufang/diy/rujiangcai/', 'name': '卤酱'}
{'url': 'http://www.meishij.net/chufang/diy/yinpin/', 'name': '时尚饮品'}
{'url': 'http://www.meishij.net/chufang/diy/zaocan/', 'name': '早餐'}
{'url': 'http://www.meishij.net/chufang/diy/wucan/', 'name': '午餐'}
{'url': 'http://www.meishij.net/chufang/diy/wancan/', 'name': '晚餐'}
{'url': 'http://www.meishij.net/chufang/diy/xiawucha/', 'name': '下午茶'}
{'url': 'http://www.meishij.net/chufang/diy/yexiao/', 'name': '夜宵'}
{'url': 'http://www.meishij.net/chufang/diy/laonian/', 'name': '老年人'}
{'url': 'http://www.meishij.net/chufang/diy/chanfu/', 'name': '产妇'}
{'url': 'http://www.meishij.net/chufang/diy/yunfu/', 'name': '孕妇'}
{'url': 'http://www.meishij.net/chufang/diy/baobaocaipu/', 'name': '宝宝食谱-婴儿食谱'}
{'url': 'http://www.meishij.net/china-food/caixi/chuancai/', 'name': '川菜'}
{'url': 'http://www.meishij.net/china-food/caixi/xiangcai/', 'name': '湘菜'}
{'url': 'http://www.meishij.net/china-food/caixi/yuecai/', 'name': '粤菜'}
{'url': 'http://www.meishij.net/china-food/caixi/dongbeicai/', 'name': '东北菜'}
{'url': 'http://www.meishij.net/china-food/caixi/lucai/', 'name': '鲁菜'}
{'url': 'http://www.meishij.net/china-food/caixi/zhecai/', 'name': '浙菜'}
{'url': 'http://www.meishij.net/china-food/caixi/sucai/', 'name': '苏菜'}
{'url': 'http://www.meishij.net/china-food/caixi/qingzhencai/', 'name': '清真菜'}
{'url': 'http://www.meishij.net/china-food/caixi/mincai/', 'name': '闽菜'}
{'url': 'http://www.meishij.net/china-food/caixi/hucai/', 'name': '沪菜'}
{'url': 'http://www.meishij.net/china-food/caixi/jingcai/', 'name': '京菜'}
{'url': 'http://www.meishij.net/china-food/caixi/hubeicai/', 'name': '湖北菜'}
{'url': 'http://www.meishij.net/china-food/caixi/huicai/', 'name': '徽菜'}
{'url': 'http://www.meishij.net/china-food/caixi/yucai/', 'name': '豫菜'}
{'url': 'http://www.meishij.net/china-food/caixi/xibeicai/', 'name': '西北菜'}
{'url': 'http://www.meishij.net/china-food/caixi/yuguicai/', 'name': '云贵菜'}
{'url': 'http://www.meishij.net/china-food/caixi/jiangxicai/', 'name': '江西菜'}
{'url': 'http://www.meishij.net/china-food/caixi/shancicai/', 'name': '山西菜'}
{'url': 'http://www.meishij.net/china-food/caixi/guangxicai/', 'name': '广西菜'}
{'url': 'http://www.meishij.net/china-food/caixi/gangtai/', 'name': '港台菜'}
{'url': 'http://www.meishij.net/china-food/caixi/other/', 'name': '其它菜'}
{'url': 'http://www.meishij.net/china-food/xiaochi/sichuan/', 'name': '四川小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/guangdong/', 'name': '广东小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/beijing/', 'name': '北京小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/shanxii/', 'name': '陕西小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/shandong/', 'name': '山东小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/shanxi/', 'name': '山西小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/hunan/', 'name': '湖南小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/henan/', 'name': '河南小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/shanghai/', 'name': '上海小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/jiangsu/', 'name': '江苏小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/hubei/', 'name': '湖北小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/chongqing/', 'name': '重庆小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/tianjin/', 'name': '天津小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/hebei/', 'name': '河北小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/zhejiang/', 'name': '浙江小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/xinjiang/', 'name': '新疆小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/jiangxi/', 'name': '江西小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/fujian/', 'name': '福建小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/guangxi/', 'name': '广西小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/yunnan/', 'name': '云南小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/liaoning/', 'name': '辽宁小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/jilin/', 'name': '吉林小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/guizhou/', 'name': '贵州小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/anhui/', 'name': '安徽小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/taiwan/', 'name': '台湾小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/gansu/', 'name': '甘肃小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/xianggang/', 'name': '香港小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/menggu/', 'name': '蒙古小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/ningxia/', 'name': '宁夏小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/qinghai/', 'name': '青海小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/hainan/', 'name': '海南小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/xizang/', 'name': '西藏小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/chengduxiaochi/', 'name': '成都小吃'}
{'url': 'http://www.meishij.net/china-food/xiaochi/heilongjiang/', 'name': '黑龙江小吃'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/hanguo/', 'name': '韩国料理'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/japan/', 'name': '日本料理'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/ccmd/', 'name': '西餐面点'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/faguo/', 'name': '法国菜'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/yidali/', 'name': '意大利餐'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/usa/', 'name': '美国家常菜'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/dongnanya/', 'name': '东南亚菜'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/moxige/', 'name': '墨西哥菜'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/aozhou/', 'name': '澳大利亚菜'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/other/', 'name': '其他国家'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/canqianxiaochi/', 'name': '餐前小吃'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/tangpin/', 'name': '汤品'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/zhucai/', 'name': '主菜'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/zhushi/', 'name': '主食'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/yinpin/', 'name': '饮品'}
{'url': 'http://www.meishij.net/chufang/diy/guowaicaipu1/tiandian/', 'name': '甜点'}
{'url': 'http://www.meishij.net/hongpei/dangaomianbao/', 'name': '蛋糕面包'}
{'url': 'http://www.meishij.net/hongpei/bingganpeifang/', 'name': '饼干配方'}
{'url': 'http://www.meishij.net/hongpei/tianpindianxin/', 'name': '甜品点心'}
{'url': 'http://www.meishij.net/hongpei/hongpeigongju/', 'name': '烘焙工具'}
{'url': 'http://www.meishij.net/hongpei/hongpeichangshi/', 'name': '烘焙常识'}
{'url': 'http://www.meishij.net/hongpei/hongpeiyuanliao/', 'name': '烘焙原料'}'''

a = total_url.split('\n')
print(a)
list = []
for i in a:
    b=eval(i)['url']
    list.append(b)

def get_all_links_from(channel):
    for num in range(1,57):
        get_links_from(channel, num)

if __name__ == '__main__':
    pool = Pool() #进程池
    pool.map(get_all_links_from, list) #将所有频道链接放入函数，一次请求获取菜谱
