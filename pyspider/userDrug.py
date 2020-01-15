# coding:utf-8
import requests
from bs4 import BeautifulSoup
import operator as op
import re
import urllib
import xlwt
import xlrd
if __name__=="__main__":
    #处理数据为用户-药材矩阵,处理结果，空值有1399824，稀疏性95%以上
    yaocaiName= ['name','灵芝孢子粉', '沙棘果粉', '辣根片', '麦芽', '谷芽', '紫河车', '儿茶', '淡豆豉', '人中白', '樟脑', '冰片', '稻芽', '益母草粉', '冬瓜皮', '玉米须', '艾条', '枯矾', '巴豆霜', '獾子油', '薄荷油', '神曲', '燕窝', '鳖甲', '蚕沙', '蛤壳', '蝉蜕', '蟾皮', '麝香', '玳瑁', '地龙', '蜂房', '蛤蚧', '龟甲', '海龙', '狗鞭', '马宝', '鹿角', '蚂蚁', '蜻蜓', '虻虫', '牛黄', '蕲蛇', '猴枣', '干水蛭', '壁虎干', '鱼鳔', '珍珠', '僵蚕', '全蝎', '蜣螂', '蛇蜕', '蝼蛄干', '蛴螬', '鼠妇', '羊鞭', '干蚯蚓', '富氧林蛙', '黄花胶', '龙虱', '鲍鱼壳', '獐宝', '九香虫', '蜈蚣干', '蛞蝓干', '海螵蛸', '刺猬皮', '牛宝', '猪宝', '五灵脂', '蛤蟆油', '金沙牛', '石决明', '地牯牛', '石蚕', '海麻雀', '海马', '水牛角', '鸡内金', '夜明砂', '鹿茸', '乌梢蛇', '蛇胆', '蛇干', '鱼宝', '艾', '荷叶', '桑叶', '石韦', '莽草', '香叶', '甜茶', '棕榈叶', '枸杞叶', '杜仲叶', '沙棘叶', '大青叶', '半枫荷', '青钱柳叶', '蒲公英叶', '淫羊藿', '丁香叶', '五倍子', '罗布麻叶', '红豆杉枝叶', '枇杷叶', '山楂叶', '木豆叶', '败火草', '火炭母', '香菊', '一朵云叶', '罗勒叶', '铁树叶', '铁将军', '银杏叶', '云南美登木', '鬼箭羽', '巴豆', '豆蔻', '白果', '蒺藜', '荜茇', '槟榔', '蕤仁', '佛手片', '青果', '广枣', '榠樝', '诃子', '鹤虱', '槐角', '芥子', '橘核', '橘络', '香砂', '沙棘', '连翘', '芡实', '青皮', '瓜蒌', '桑葚干', '砂仁', '栀子', '水栀', '桃仁', '干乌梅', '香橼', '益智', '枳壳', '枣核', '枳实', '榧子', '胖大海', '辣木籽', '王不留行', '草蔻', '五味子', '牡丹籽', '茱萸', '灰苏子', '金樱子', '葡萄籽', '莲心', '地肤子', '决明子', '黄金果', '火麻', '马牯', '白苏籽', '紫苏子', '火麻仁', '八月瓜片', '罗汉果干', '化橘红', '酸枣仁', '槟榔花', '穿心莲', '文冠果', '柏树果', '蛇床子', '仁用杏', '覆盆子', '女贞子', '水飞蓟', '屈头鸡', '马槟榔', '山捻子', '木姜子', '便秘果', '苍耳子', '葶苈子', '佛手果', '苦豆子', '石榴皮', '补骨脂', '牵牛子', '白芥子', '沙苑子', '青葙子', '枳椇子', '海金沙', '乌榄', '乌榄仁', '橄榄仁', '路路通', '白花菜子', '川楝子', '楮实子', '马钱子', '天茄子', '小叶鼠李', '皂荚', '木鳖子', '棉花子', '竹米', '柏子仁', '郁李仁', '六轴子', '蔓荆子', '杜仲', '椿皮', '肉桂', '厚朴', '黄柏', '秦皮', '牡丹皮', '松皮', '地骨皮', '山高梁', '梓白皮', '旱冬瓜', '刺楸', '地枫皮', '阿魏', '琥珀', '没药', '藤黄', '血竭', '乳香', '松香', '安息香', '人参', '附子', '白及', '白蔹', '白前', '白芍', '白术', '白薇', '白芷', '百部', '苍术', '拳参', '草乌', '柴胡']
    Province=['河北','山西','内蒙古','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','广西','海南','四川','贵州','云南','西藏','陕西','甘肃','青海','宁夏','新疆','北京','天津','上海','重庆','台湾省','香港特别行政区','澳门特别行政区']
    book1 = xlwt.Workbook(encoding='utf-8')
    sheet1 = book1.add_sheet('userDrug')
    num=1
    flag = False
    for h in range(len(yaocaiName)):
        sheet1.write(0, h, yaocaiName[h])  # 写入表头
    df = xlrd.open_workbook('test.xls')
    table = df.sheet_by_name('userDetail')
    rows=table.nrows
    # print(yaocaiName)
    count=0
    lastUser = table.row_values(1)[0]
    lastDrug = table.row_values(1)[1]
    for row in range(1,rows):
        rowvalue = table.row_values(row)
        curUser = rowvalue[0]
        curDrug = rowvalue[1]
        if curDrug == lastDrug and curUser == lastUser:
            count += 1
        elif curUser == lastUser and curDrug != lastDrug:
            col = yaocaiName.index(lastDrug)
            sheet1.write(num, col, count)
            count = 1
        elif curUser != lastUser:
            col = yaocaiName.index(lastDrug)
            sheet1.write(num, col, count)
            num += 1
            count = 1
            flag = False
        lastDrug = curDrug
        lastUser = curUser
        if flag == False:
            sheet1.write(num, 0, rowvalue[0])
            flag = True
    book1.save('userDrug.xls')