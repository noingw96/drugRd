# coding:utf-8
import requests
from bs4 import BeautifulSoup
import operator as op
import re
import urllib
import xlwt
#药材每个页面的url
def getUrlList():
    user_agent = 'Mozilla/4.0 (compatible;MSIE5.5;windows NT)'
    headers = {'User-Agent': user_agent}
    url = 'https://www.cnhnb.com/p/zyc/'
    yaocai_url = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
    yaocai_a = soup.find_all(class_="third-cate-item link-expanded")
    for yaocai_a_item in yaocai_a:
        a = yaocai_a_item.get('href')
        b = yaocai_a_item.text.replace('\n','').strip()
        yaocai_url.append(b)
    return yaocai_url
#药材-地区-评分信息
def savePositionGrade(yaocaiUrl,yaocaiName,Province):
    user_agent = 'Mozilla/4.0 (compatible;MSIE5.5;windows NT)'
    headers = {'User-Agent': user_agent}
    Host = 'https://www.cnhnb.com'
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('position')
    head = ['name','position','grade']  # 表头
    num=1
    for h in range(len(head)):
        sheet.write(0, h, head[h])  # 写入表头
    for x in range(len(yaocaiName)):
        res = requests.get(Host + yaocaiUrl[x], headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser', from_encoding='utf-8')
        Place = []  # 获取到该药材供应地-省的列表
        place = soup.find_all(class_="place")
        for i in range(1,len(place)-1,2):
            place_item = place[i].text
            # 简化到省
            if place_item[0:2] in Province:
                Place.append(place_item[0:2])
            elif place_item[0:3] in Province:
                Place.append(place_item[0:3])
            elif place_item[0:7] in Province:
                Place.append(place_item[0:7])
        grade = {}  # 评分的字典
        for i in Place:
            if grade.get(i) == None:
                grade[i] = 1
            else:
                cur_times = grade.get(i)
                grade[i] = cur_times + 1
        # print(grade)#{'山东': 6, '广西': 1, '吉林': 18, '辽宁': 1, '河北': 1, '安徽': 8, '河南': 1, '江西': 1, '黑龙江': 1, '广东': 1}
        print(x,yaocaiName[x],grade)
        for key in grade:
            sheet.write(num, 0, yaocaiName[x])
            sheet.write(num, 1, key)
            sheet.write(num, 2, grade[key] / 4)
            num = num + 1
    book.save('E:/WU/pyfile/xin/pos.xls')
def saveDetail(yaocaiUrl,yaocaiName,Province):
    user_agent = 'Mozilla/4.0 (compatible;MSIE5.5;windows NT)'
    headers = {'User-Agent': user_agent}
    Host = 'https://www.cnhnb.com'
    book1 = xlwt.Workbook(encoding='utf-8')
    sheet1 = book1.add_sheet('position')
    head1 = ['name','position','grade']  # 表头
    num=1
    for h in range(len(head1)):
        sheet1.write(0, h, head1[h])  # 写入表头
    for x in range(len(yaocaiName)):
        Place = []  # 获取到该药材供应地-省的列表
        grade = {}  # 评分的字典
        count=0   #计数，该药材的用户量
        for y in range(1,4):
            try:
                res = requests.get(Host + yaocaiUrl[x][0:-1] + '-0-0-0-0-' + str(y) + '/', headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser', from_encoding='utf-8')
                place = soup.find_all(class_="place")
                for i in range(1, len(place) - 1, 2):
                    place_item = place[i].text
                    # 简化到省
                    if place_item[0:2] in Province:
                        Place.append(place_item[0:2])
                    elif place_item[0:3] in Province:
                        Place.append(place_item[0:3])
                    elif place_item[0:7] in Province:
                        Place.append(place_item[0:7])
                    count+=1
            except:
                break
        for i in Place:
            if grade.get(i) == None:
                grade[i] = 1
            else:
                cur_times = grade.get(i)
                grade[i] = cur_times + 1
        # print(grade)#{'山东': 6, '广西': 1, '吉林': 18, '辽宁': 1, '河北': 1, '安徽': 8, '河南': 1, '江西': 1, '黑龙江': 1, '广东': 1}
        print(x, yaocaiName[x], grade)
        for key in grade:
            sheet1.write(num, 0, yaocaiName[x])
            sheet1.write(num, 1, key)
            sheet1.write(num, 2, round(grade[key] / count,3))
            num = num + 1
    book1.save('E:/WU/pyfile/xin/times.xls')
def saveAll(yaocaiUrl,yaocaiName,Province):
    user_agent = 'Mozilla/4.0 (compatible;MSIE5.5;windows NT)'
    headers = {'User-Agent': user_agent}
    Host = 'https://www.cnhnb.com'
    book1 = xlwt.Workbook(encoding='utf-8')
    sheet1 = book1.add_sheet('position')
    head1 = ['name','user','standard','position']  # 表头
    num=1
    for h in range(len(head1)):
        sheet1.write(0, h, head1[h])  # 写入表头
    for x in range(len(yaocaiName)):
        Place = []  # 获取到该药材供应地-省的列表
        grade = {}  # 评分的字典
        count=0   #计数，该药材的用户量
        for y in range(1,4):
            try:
                res = requests.get(Host + yaocaiUrl[x][0:-1] + '-0-0-0-0-' + str(y) + '/', headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser', from_encoding='utf-8')
                product = soup.find_all(class_="product-bg")
                for item in product:
                    standard = item.find_all(class_="fruit-explain")[0].text
                    user = item.find_all(class_="li-img")[0].text.strip()
                    position = item.find_all(class_="place")[1].text
                    Place.append({
                        'standard': standard,
                        'user': user,
                        'position': position
                    })
            except:
                break
        for key in Place:
            sheet1.write(num, 0, yaocaiName[x])
            sheet1.write(num, 1, key['user'])
            sheet1.write(num, 2, key['standard'])
            sheet1.write(num, 3, key['position'])
            num = num + 1
    book1.save('E:/WU/pyfile/xin/all_data.xls')
if __name__=="__main__":
    yaocaiUrl = ['/p/lzpzf/', '/p/sjgf/', '/p/lgp/', '/p/maiya/', '/p/guaya/', '/p/zhc/', '/p/ercha/', '/p/ddc/', '/p/rzb/', '/p/zhangnao/', '/p/bingpian/', '/p/daoya/', '/p/ymcf/', '/p/dongguapi/', '/p/yumixu/', '/p/at/', '/p/kufan/', '/p/bds/', '/p/huanziyou/', '/p/boheyou/', '/p/shenqu/', '/p/yanwo/', '/p/biejia/', '/p/cansha/', '/p/hake/', '/p/chantui/', '/p/chanpi/', '/p/shexiang/', '/p/daimao/', '/p/dilong/', '/p/fengfang/', '/p/gejie/', '/p/guijia/', '/p/hailong/', '/p/goubian/', '/p/mabao/', '/p/lujiao/', '/p/mayi/', '/p/qingting/', '/p/mengchong/', '/p/niuhuang/', '/p/qishe/', '/p/houzao/', '/p/gsz/', '/p/bihuo/', '/p/yubiao/', '/p/zhenzhu/', '/p/jiangcan/', '/p/quanxie/', '/p/qianglang/', '/p/shetui/', '/p/lougug/', '/p/qicao/', '/p/shufu/', '/p/yangbian/', '/p/gqy/', '/p/fylw/', '/p/hhj/', '/p/longshi/', '/p/baoyuke/', '/p/zhangbao/', '/p/jiuxiangchong/', '/p/wugonggan/', '/p/kuoyugan/', '/p/hpx/', '/p/cwp/', '/p/niubao/', '/p/zhubao/', '/p/wlz/', '/p/hamy/', '/p/jsn/', '/p/shijm/', '/p/dgn/', '/p/sc/', '/p/hmq/', '/p/haim/', '/p/snj/', '/p/jnj/', '/p/yems/', '/p/lurong/', '/p/wss/', '/p/shed/', '/p/sheg/', '/p/yb/', '/p/aiye/', '/p/heye/', '/p/sangye/', '/p/shiwei/', '/p/mangcao/', '/p/xiangye/', '/p/tiancha/', '/p/zly/', '/p/goqy/', '/p/dzy/', '/p/sjy/', '/p/dqy/', '/p/bfh/', '/p/qqly/', '/p/pgyy/', '/p/yinyanghuo/', '/p/dxy/', '/p/wbz/', '/p/lbmy/', '/p/hdszy/', '/p/pipaye/', '/p/shanzhaye/', '/p/mudouye/', '/p/bhc/', '/p/htm/', '/p/xj/', '/p/ydyy/', '/p/lly/', '/p/tsy/', '/p/tjj/', '/p/yxy/', '/p/ynmdm/', '/p/gjy/', '/p/badou/', '/p/doukou/', '/p/baiguo/', '/p/jili/', '/p/biba/', '/p/binglang/', '/p/ruiren/', '/p/foshou/', '/p/qingguo/', '/p/guangzao/', '/p/mingzha/', '/p/hezi/', '/p/heshi/', '/p/huaijiao/', '/p/jiezi/', '/p/juhe/', '/p/juluo/', '/p/xiangsha/', '/p/shaji/', '/p/lianqiaoo/', '/p/qianshi/', '/p/qingpi/', '/p/gualou/', '/p/sangsheno/', '/p/sharen/', '/p/zhiz/', '/p/shuizhit/', '/p/taoren/', '/p/ganwumei/', '/p/xiangyuan/', '/p/yizhi/', '/p/zhike/', '/p/zaohe/', '/p/zhishi/', '/p/feizi/', '/p/pangdahai/', '/p/lmz/', '/p/wblx/', '/p/caokuo/', '/p/wwz/', '/p/mdz/', '/p/zhuyu/', '/p/hsz/', '/p/jyz/', '/p/ptz/', '/p/lianxin/', '/p/dfz/', '/p/jmz/', '/p/hjg/', '/p/huoma/', '/p/maku/', '/p/bsz/', '/p/zsz/', '/p/hmr/', '/p/bayueguapi/', '/p/lhgg/', '/p/hjh/', '/p/szr/', '/p/binglanghu/', '/p/chuanxin/', '/p/wenguanguo/', '/p/baishuguo/', '/p/shechaungz/', '/p/renyongx/', '/p/fupenzi/', '/p/nvzhenzizy/', '/p/shuifeiji/', '/p/qtj/', '/p/mbl/', '/p/shannianzi/', '/p/mjz/', '/p/bianmiguo/', '/p/cez/', '/p/tlz/', '/p/foshouguo/', '/p/kdz/', '/p/slp/', '/p/bgz/', '/p/qnz/', '/p/bjz/', '/p/swz/', '/p/qxz/', '/p/zhijuzi/', '/p/haijinsha/', '/p/wulan/', '/p/wlr/', '/p/glr/', '/p/llt/', '/p/bhcz/', '/p/clz/', '/p/csz/', '/p/mqz/', '/p/tqz/', '/p/xysl/', '/p/zaojia/', '/p/mbz/', '/p/mhz/', '/p/zm/', '/p/bzr/', '/p/ylr/', '/p/lzz/', '/p/manjz/', '/p/duzhong/', '/p/chunpi/', '/p/rougui/', '/p/houpu/', '/p/huangbai/', '/p/qinpi/', '/p/mdp/', '/p/sp/', '/p/dgp/', '/p/sgl/', '/p/zbp/', '/p/hdg/', '/p/cj/', '/p/dfp/', '/p/awei/', '/p/hupo/', '/p/meiyao/', '/p/tenghuang/', '/p/xuejie/', '/p/ruxiang/', '/p/songxiang/', '/p/axx/', '/p/renshen/', '/p/fuzi/', '/p/baiji/', '/p/bailian/', '/p/baiqian/', '/p/baishao/', '/p/baizhu/', '/p/baiwei/', '/p/baizhi/', '/p/baibu/', '/p/cangzhu/', '/p/quancan/', '/p/caowu/', '/p/chaihu/', '/p/changshan/', '/p/chishao/', '/p/chuanwu/', '/p/chuanxiong/', '/p/dahuang/', '/p/danshen/', '/p/danggui/', '/p/dangshen/', '/p/diyu/', '/p/ezhu/', '/p/fangfeng/', '/p/fangji/', '/p/ganjiang/', '/p/gancao/', '/p/gansong/', '/p/baqia/', '/p/gansui/', '/p/gaoben/', '/p/gangegeno/', '/p/gouji/', '/p/shanyaop/', '/p/banxia/', '/p/huzhang/', '/p/niuxi/', '/p/huangjing/', '/p/huanglian/', '/p/huangqi/', '/p/huangqin/', '/p/jianghuang/', '/p/jugeng/', '/p/yymoyo/', '/p/kushen/', '/p/xixin/', '/p/xiecao/', '/p/longdan/', '/p/lugen/', '/p/maidong/', '/p/zhimu/', '/p/oujie/', '/p/qianhu/', '/p/qiancao/', '/p/qianghuo/', '/p/qinjiao/', '/p/sanqi/', '/p/shannai/', '/p/shanglu/', '/p/yegan/', '/p/shengma/', '/p/dihuang/', '/p/tiandong/', '/p/tianma/', '/p/wuyao/', '/p/xianmao/', '/p/xiangfu/', '/p/xiebai/', '/p/xuduan/', '/p/xuanshen/', '/p/yuzhu/', '/p/yujin/', '/p/yuanzhi/', '/p/muxiang/', '/p/zexie/', '/p/chonglou/', '/p/zicao/', '/p/ziyuan/', '/p/sanleng/', '/p/langdu/', '/p/lilu/', '/p/loulu/', '/p/maka/', '/p/shouwu/', '/p/banlangen/', '/p/congrong/', '/p/niudali/', '/p/xys/', '/p/chuanduan/', '/p/sd/', '/p/yuanhu/', '/p/disen/', '/p/beimu/', '/p/niubang/', '/p/ssg/', '/p/nnsg/', '/p/xbah/', '/p/shasen/', '/p/wzmt/', '/p/bss/', '/p/cms/', '/p/tnx/', '/p/guangzhong/', '/p/cahgen/', '/p/nanblg/', '/p/gusuipu/', '/p/gangmeigen/', '/p/taizishen/', '/p/bmg/', '/p/wlx/', '/p/tianhuafen/', '/p/zhuzishen/', '/p/danzhuye/', '/p/zjc/', '/p/jlg/', '/p/mth/', '/p/sys/', '/p/qjb/', '/p/pj/', '/p/sbp/', '/p/liangmz/', '/p/bxp/', '/p/bajiaolian/', '/p/xiatianwu/', '/p/mhtg/', '/p/dxmz/', '/p/zbfp/', '/p/liangjiang/', '/p/bqz/', '/p/btw/', '/p/bsw/', '/p/csl/', '/p/tkz/', '/p/zhqh/', '/p/jjg/', '/p/luohanshen/', '/p/hs/', '/p/qingys/', '/p/sh/', '/p/bbc/', '/p/tfl/', '/p/jj/', '/p/jlt/', '/p/huotg/', '/p/wzss/', '/p/lgw/', '/p/xsyzs/', '/p/dgal/', '/p/zmt/', '/p/wjp/', '/p/hyz/', '/p/dsz/', '/p/zsl/', '/p/dqg/', '/p/nwc/', '/p/fenxm/', '/p/hongsg/', '/p/tiekz/', '/p/tiebj/', '/p/slb/', '/p/tmd/', '/p/gsx/', '/p/longchi/', '/p/zhusha/', '/p/cishi/', '/p/danfan/', '/p/zaofan/', '/p/hongfen/', '/p/huashi/', '/p/liuhuang/', '/p/cihuang/', '/p/mangxiao/', '/p/pengsha/', '/p/lvfan/', '/p/qiushi/', '/p/shigao/', '/p/shiyan/', '/p/yunmu/', '/p/longgu/', '/p/xionghuang/', '/p/zheshi/', '/p/manao/', '/p/qiandan/', '/p/naosha/', '/p/shuiyin/', '/p/mfs/', '/p/yqs/', '/p/gehua/', '/p/dingxiango/', '/p/honghua/', '/p/huaihua/', '/p/gjh/', '/p/lianfang/', '/p/lianxu/', '/p/meihua/', '/p/puhuang/', '/p/xinyi/', '/p/shidi/', '/p/guihuaob/', '/p/yuanhua/', '/p/taohua/', '/p/jinyinhua/', '/p/hhdsl/', '/p/shh/', '/p/sqh/', '/p/bwh/', '/p/kdh/', '/p/dzxh/', '/p/xuelian/', '/p/syh/', '/p/meiguiqie/', '/p/huanglianhua/', '/p/xysh/', '/p/zhh/', '/p/hehuanhua/', '/p/hm/', '/p/jhh/', '/p/yuanshenhua/', '/p/mgh/', '/p/mimh/', '/p/jiguanh/', '/p/zhuling/', '/p/leiwan/', '/p/zhuhuang/', '/p/sanghuang/', '/p/hzg/', '/p/hongjun/', '/p/hsr/', '/p/dmcz/', '/p/cc/', '/p/xueer/', '/p/rzrong/', '/p/fuling/', '/p/fushen/', '/p/yunzhi/', '/p/kunbu/', '/p/lingzhi/', '/p/mabo/', '/p/cch/', '/p/chenxiango/', '/p/huangteng/', '/p/gouteng/', '/p/guizhi/', '/p/taozhi/', '/p/kumu/', '/p/bili/', '/p/zhangmu/', '/p/sangzhi/', '/p/sumu/', '/p/tanxiang/', '/p/tongcao/', '/p/zhemu/', '/p/zhuru/', '/p/jxt/', '/p/longxuteng/', '/p/hauizhi/', '/p/sl/', '/p/hft/', '/p/lst/', '/p/ht/', '/p/yjt/', '/p/tsq/', '/p/js/', '/p/qft/', '/p/jist/', '/p/lgt/', '/p/rdt/', '/p/bohe/', '/p/daji/', '/p/bianxu/', '/p/muzei/', '/p/juju/', '/p/ximi/', '/p/huoxiang/', '/p/jingjie/', '/p/juanbai/', '/p/mahuang/', '/p/peilan/', '/p/qinghao/', '/p/lvcao/', '/p/shemei/', '/p/suoyang/', '/p/wasong/', '/p/xiangru/', '/p/gouwen/', '/p/xiaoji/', '/p/yinchen/', '/p/xuedang/', '/p/zelan/', '/p/dangyao/', '/p/baijiang/', '/p/honglian/', '/p/fuping/', '/p/longkui/', '/p/qumai/', '/p/dijiao/', '/p/zeqi/', '/p/xiangmao/', '/p/shanxiang/', '/p/qitaqcl/', '/p/dxc/', '/p/tsz/', '/p/cqc/', '/p/mdc/', '/p/xiancao/', '/p/banzhilian/', '/p/jiucaizi/', '/p/yimucao/', '/p/pugongy/', '/p/shenjincao/', '/p/guizhencao/', '/p/xiakucao/', '/p/shp/', '/p/didc/', '/p/yg/', '/p/hxc/', '/p/bxc/', '/p/tqdb/', '/p/jiaogulan/', '/p/mtj/', '/p/jqc/', '/p/jtsq/', '/p/lhc/', '/p/jgc/', '/p/honggencao/', '/p/hjt/', '/p/tgc/', '/p/yizhihuanghua/', '/p/dujiaolian/', '/p/shiganlan/', '/p/mry/', '/p/doubanlv/', '/p/niuerfeng/', '/p/kdd/', '/p/ssb/', '/p/mxc/', '/p/jxl/', '/p/yeju/', '/p/xueshen/', '/p/hsc/', '/p/tielb/', '/p/ydj/', '/p/zhdd/', '/p/ync/', '/p/cqz/', '/p/guojl/', '/p/tbo/', '/p/chiche/', '/p/hnc/', '/p/jxq/', '/p/dm/', '/p/syk/', '/p/gylq/', '/p/xfjc/', '/p/fxc/', '/p/lbz/', '/p/scg/', '/p/hcc/', '/p/qingyd/', '/p/jsc/', '/p/byl/', '/p/fengwc/', '/p/ydc/', '/p/shidl/', '/p/cxc/', '/p/gzj/', '/p/sg/', '/p/kmc/', '/p/syl/', '/p/hxcao/', '/p/ccr/', '/p/lys/', '/p/lfs/', '/p/qj/', '/p/gj/', '/p/hsx/', '/p/lsh/', '/p/yzj/', '/p/fwc/', '/p/lxf/', '/p/dhh/', '/p/fsc/', '/p/ljn/', '/p/ylhc/', '/p/shhc/', '/p/xmcao/', '/p/lzc/', '/p/gyc/', '/p/jgcao/', '/p/bhssc/', '/p/bqc/', '/p/sscao/', '/p/dzxx/', '/p/dqc/', '/p/mhl/', '/p/ld/', '/p/chqc/', '/p/nzc/', '/p/brcao/', '/p/tef/', '/p/tes/', '/p/sycao/', '/p/spz/', '/p/scc/', '/p/mpc/', '/p/skw/', '/p/midx/', '/p/xhz/', '/p/wgc/', '/p/wlc/', '/p/sxt/', '/p/yxz/', '/p/xhc/', '/p/djg/', '/p/qxj/', '/p/njc/', '/p/lnj/', '/p/blh/', '/p/sliao/', '/p/xpc/', '/p/hanxc/', '/p/zyca/', '/p/qiyd/', '/p/xjnc/', '/p/ths/', '/p/zbc/', '/p/dkc/', '/p/bx/', '/p/hx/', '/p/ghx/', '/p/fgdc/', '/p/bms/', '/p/xqc/', '/p/tdh/', '/p/fbc/', '/p/whz/', '/p/lrc/', '/p/bby/', '/p/dcc/', '/p/syq/', '/p/gss/', '/p/ltc/', '/p/ly/', '/p/shl/', '/p/tjh/', '/p/dssk/', '/p/nmt/']
    yaocaiName= ['灵芝孢子粉', '沙棘果粉', '辣根片', '麦芽', '谷芽', '紫河车', '儿茶', '淡豆豉', '人中白', '樟脑', '冰片', '稻芽', '益母草粉', '冬瓜皮', '玉米须', '艾条', '枯矾', '巴豆霜', '獾子油', '薄荷油', '神曲', '燕窝', '鳖甲', '蚕沙', '蛤壳', '蝉蜕', '蟾皮', '麝香', '玳瑁', '地龙', '蜂房', '蛤蚧', '龟甲', '海龙', '狗鞭', '马宝', '鹿角', '蚂蚁', '蜻蜓', '虻虫', '牛黄', '蕲蛇', '猴枣', '干水蛭', '壁虎干', '鱼鳔', '珍珠', '僵蚕', '全蝎', '蜣螂', '蛇蜕', '蝼蛄干', '蛴螬', '鼠妇', '羊鞭', '干蚯蚓', '富氧林蛙', '黄花胶', '龙虱', '鲍鱼壳', '獐宝', '九香虫', '蜈蚣干', '蛞蝓干', '海螵蛸', '刺猬皮', '牛宝', '猪宝', '五灵脂', '蛤蟆油', '金沙牛', '石决明', '地牯牛', '石蚕', '海麻雀', '海马', '水牛角', '鸡内金', '夜明砂', '鹿茸', '乌梢蛇', '蛇胆', '蛇干', '鱼宝', '艾', '荷叶', '桑叶', '石韦', '莽草', '香叶', '甜茶', '棕榈叶', '枸杞叶', '杜仲叶', '沙棘叶', '大青叶', '半枫荷', '青钱柳叶', '蒲公英叶', '淫羊藿', '丁香叶', '五倍子', '罗布麻叶', '红豆杉枝叶', '枇杷叶', '山楂叶', '木豆叶', '败火草', '火炭母', '香菊', '一朵云叶', '罗勒叶', '铁树叶', '铁将军', '银杏叶', '云南美登木', '鬼箭羽', '巴豆', '豆蔻', '白果', '蒺藜', '荜茇', '槟榔', '蕤仁', '佛手片', '青果', '广枣', '榠樝', '诃子', '鹤虱', '槐角', '芥子', '橘核', '橘络', '香砂', '沙棘', '连翘', '芡实', '青皮', '瓜蒌', '桑葚干', '砂仁', '栀子', '水栀', '桃仁', '干乌梅', '香橼', '益智', '枳壳', '枣核', '枳实', '榧子', '胖大海', '辣木籽', '王不留行', '草蔻', '五味子', '牡丹籽', '茱萸', '灰苏子', '金樱子', '葡萄籽', '莲心', '地肤子', '决明子', '黄金果', '火麻', '马牯', '白苏籽', '紫苏子', '火麻仁', '八月瓜片', '罗汉果干', '化橘红', '酸枣仁', '槟榔花', '穿心莲', '文冠果', '柏树果', '蛇床子', '仁用杏', '覆盆子', '女贞子', '水飞蓟', '屈头鸡', '马槟榔', '山捻子', '木姜子', '便秘果', '苍耳子', '葶苈子', '佛手果', '苦豆子', '石榴皮', '补骨脂', '牵牛子', '白芥子', '沙苑子', '青葙子', '枳椇子', '海金沙', '乌榄', '乌榄仁', '橄榄仁', '路路通', '白花菜子', '川楝子', '楮实子', '马钱子', '天茄子', '小叶鼠李', '皂荚', '木鳖子', '棉花子', '竹米', '柏子仁', '郁李仁', '六轴子', '蔓荆子', '杜仲', '椿皮', '肉桂', '厚朴', '黄柏', '秦皮', '牡丹皮', '松皮', '地骨皮', '山高梁', '梓白皮', '旱冬瓜', '刺楸', '地枫皮', '阿魏', '琥珀', '没药', '藤黄', '血竭', '乳香', '松香', '安息香', '人参', '附子', '白及', '白蔹', '白前', '白芍', '白术', '白薇', '白芷', '百部', '苍术', '拳参', '草乌', '柴胡', '常山', '中药材赤芍', '川乌', '川芎', '大黄', '丹参', '当归', '党参', '地榆', '莪术', '防风', '防己', '干姜', '甘草', '甘松', '菝葜', '甘遂', '藁本', '干葛根', '狗脊', '山药片', '半夏', '虎杖', '牛膝', '黄精', '黄连', '黄芪', '黄芩', '姜黄', '桔梗', '药用魔芋', '苦参', '细辛', '缬草', '龙胆', '芦根', '麦冬', '知母', '藕节', '前胡', '茜草', '羌活', '秦艽', '三七', '山柰', '商陆', '射干', '升麻', '地黄', '天冬', '天麻', '乌药', '仙茅', '香附', '薤白', '续断', '玄参', '玉竹', '郁金', '远志', '木香', '泽泻', '重楼', '紫草', '紫菀', '三棱', '狼毒', '藜芦', '漏芦', '玛咖', '首乌', '板蓝根', '苁蓉', '牛大力', '西洋参', '川断', '熟地', '元胡', '地参', '贝母', '牛蒡', '石参根', '牛奶树根', '鲜巴戟', '沙参', '五指毛桃', '北沙参', '川明参', '天南星', '贯众', '茶根', '南板蓝根', '骨碎朴', '岗梅根', '太子参', '白茅根', '威灵仙', '天花粉', '珠子参', '淡竹叶', '皂角刺', '金果榄', '墓头回', '四叶参', '千斤拔', '炮姜', '桑白皮', '两面针', '白鲜皮', '八角莲', '夏天无', '猕猴桃根', '地下明珠', '制白附片', '良姜', '冰球子', '白头翁', '白首乌', '穿山龙', '天葵子', '紫花前胡', '菊苣根', '罗汉参', '黄参', '\u200b青阳参', '石斛', '百部草', '土茯苓', '假蒟', '九龙藤', '火头根', '五指山参', '了哥王', '雪上一枝蒿', '东革阿里', '走马胎', '五加皮', '黄药子', '滴水珠', '朱砂莲', '大气(菊)根', '牛尾菜', '分心木', '红参果', '铁筷子', '铁包金', '树萝卜', '天门冬', '隔山消', '龙齿', '朱砂', '磁石', '胆矾', '皂矾', '红粉', '滑石', '硫黄', '雌黄', '芒硝', '硼砂', '绿矾', '秋石', '石膏', '石燕', '云母', '龙骨', '雄黄', '赭石', '玛瑙', '铅丹', '硇砂', '水银', '麦饭石', '阳起石', '葛花', '干丁香', '红花', '槐花', '干菊花', '莲房', '莲须', '梅花', '蒲黄', '辛夷', '柿蒂', '桂花瓣', '芫花', '桃花', '金银花', '黄花倒水莲', '石斛花', '三七花', '霸王花', '款冬花', '杜仲雄花', '雪莲', '山银花', '玫瑰茄', '黄莲花', '西洋参花', '藏红花', '合欢花', '槐米', '橘红花', '园参花', '玫瑰花', '密蒙花', '中药材鸡冠花', '猪苓', '雷丸', '竹黄', '桑黄', '红椎菇', '红菌', '桦树茸', '椴木赤芝', '虫草', '血耳', '肉苁蓉', '茯苓', '茯神', '云芝', '昆布', '灵芝', '马勃', '虫草花', '沉香', '黄藤', '钩藤', '桂枝', '桃枝', '苦木', '薜荔', '樟木', '桑枝', '苏木', '檀香', '通草', '柘木', '竹茹', '鸡血藤', '龙须藤', '槐枝', '蛇莲', '海风藤', '络石藤', '红藤', '夜交藤', '藤三七', '寄生', '青风藤', '鸡矢藤', '雷公藤', '忍冬藤', '薄荷', '大蓟', '萹蓄', '木贼', '菊苣', '菥蓂', '藿香', '荆芥', '卷柏', '麻黄', '佩兰', '中药材青蒿', '葎草', '蛇莓', '锁阳', '瓦松', '香薷', '钩吻', '小蓟', '茵陈', '血党', '泽兰', '当药', '败酱', '洪连', '浮萍', '龙葵', '瞿麦', '地椒', '泽漆', '香茅', '山香', '其它全草类', '灯芯草', '菟丝子', '车前草', '中药麦冬草', '仙草', '半枝莲', '韭菜子', '益母草', '蒲公英', '伸筋草', '鬼针草', '夏枯草', '石黄皮', '地胆草', '野菰', '红雪茶', '白雪茶', '天青地白', '绞股蓝', '马蹄金', '金钱草', '景天三七', '鹿含草', '鸡骨草', '红根草', '红景天', '透骨草', '一枝黄花', '独角莲', '石橄榄', '明日叶', '豆瓣绿', '牛耳枫', '苦地丁', '石上柏', '猫须草', '金线莲', '野菊', '血参', '化石草', '铁篱笆（药材）', '阴地蕨', '紫花地丁', '岩白菜', '车前子', '过江龙', '塘边耦', '赤车', '黄牛茶', '见血清', '胆木', '三丫苦', '贯叶连翘', '小肺筋草', '肺心草', '芦巴子', '山慈菇', '中药材回春草', '青叶胆', '金丝草', '斑叶兰', '蜂窝草', '忧遁草', '石吊兰', '穿心草', '瓜子金', '蛇菰', '苦荬菜', '四叶莲', '回心草（药材）', '草苁蓉', '六月霜', '理肺散', '青箭', '葛菌', '红丝线', '冷水花', '一支箭', '凤尾草', '落新妇', '大还魂', '腹水草', '刘寄奴', '野老鹤草', '伤寒草', '血满草', '荔枝草', '观音草', '接骨草', '白花蛇舌草', '白屈菜', '双肾草', '灯盏细辛', '颠茄草', '墨旱莲', '列当', '中药材车前草', '牛至草', '百蕊草', '兔耳风', '兔儿伞', '肾炎草', '石见穿', '石蝉草', '磨盘草', '四块瓦', '中药材迷迭香', '绣花针', '蜈蚣草', '委陵菜', '野生石仙桃', '叶下珠', '仙鹤草', '独脚柑', '七星剑', '牛筋草', '六棱菊', '博落回', '水蓼', '小蓬草', '韩信草', '獐牙菜', '七叶胆', '小金牛草', '天胡荽', '猪鬃草', '倒扣草', '扁蓄', '霍香', '广霍香', '风柜斗草', '白毛蛇', '豨签草', '土大黄', '翻白草', '无患子', '鹿茸草', '白背叶', '断肠草', '三叶青', '公石松', '犁头草', '蒌叶', '水黄连', '田基黄', '多穗石柯', '糯米藤']
    Province=['河北','山西','内蒙古','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','广西','海南','四川','贵州','云南','西藏','陕西','甘肃','青海','宁夏','新疆','北京','天津','上海','重庆','台湾省','香港特别行政区','澳门特别行政区']
    # yaocaiName =getUrlList()
    # savePositionGrade(yaocaiUrl,yaocaiName,Province)
    saveDetail(yaocaiUrl,yaocaiName,Province)
    saveAll(yaocaiUrl,yaocaiName,Province)














