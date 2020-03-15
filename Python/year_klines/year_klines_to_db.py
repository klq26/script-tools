# coding = utf8

import json
import sys
import os
import pymysql

# 把从 eastmoney 下载的 ('2012-12-31,xxxx,xxx') 数据清洗成真正的 json
# 虽然都是 js 数据，但是本地保存的时候，都写成了 .json，例如 上证50_0000151.json
def purgeEastmoneyYearData():
    print('清洗数据')
    for root, dirs, files in os.walk('input'):
        for file in files:
            if '.py' not in file:
                filepath = os.path.join(root,file)
                # print(filepath)
                # if '_new' in filepath:
                #     os.remove(filepath)
                #     continue
                indexInfos = file.replace('.json','').split('_')
                country_name= indexInfos[0]
                country_code = indexInfos[1]
                continent = ''
                if 'china' in filepath.lower():
                    continent = '中国'
                if 'asian' in filepath.lower():
                    continent = '亚洲'
                if 'euro' in filepath.lower():
                    continent = '欧洲'
                if 'america' in filepath.lower():
                    continent = '美洲'
                if len(indexInfos) == 3:
                    country_code = country_code + '_UI'
                
                with open(filepath,'r',encoding='utf-8') as f:
                    dataList = f.read().replace('(','').replace(')','').split('\n')
                    result = []
                    count = 0
                    for data in dataList:
                        values = str(data).replace('(','').split(',')
                        if len(values) < 3:
                            continue
                        count += 1
                        result.append({'date' : values[0], 'open' : values[1], 'close' : values[2], 'rate' : '{0}%'.format(round((float(values[2])/float(values[1])-1)*100,2))})

                    folderpath = os.path.join(os.getcwd(),'output')
                    if not os.path.exists(folderpath):
                        os.makedirs(folderpath)
                    with open(os.path.join(folderpath,file),'w+',encoding='utf-8') as f_out:
                        f_out.write(json.dumps({'name' : country_name, 'symbol': country_code, 'continent' : continent, 'total' : count, 'data' : result}, ensure_ascii = False, indent = 4, separators=(',', ':')))

# 把所有数据输出到一个中间 txt （后续写入 SQL 数据库）
def combineAndOutputToTxt():
    outputpath = os.path.join(os.getcwd(),'output','db.txt')
    if os.path.exists(outputpath):
        os.remove(outputpath)
    for root, dirs, files in os.walk('output'):
        for file in files:
            if '.json' in file:
                filepath = os.path.join(root,file)
                # print(filepath)
                with open(filepath,'r',encoding='utf-8') as f:
                    data = json.loads(f.read())
                    country_name= data['name']
                    country_code = data['symbol']
                    continent = data['continent']
                    total = data['total']
                    datalist = data['data']
                    
                    with open(outputpath,'a+',encoding='utf-8') as f_out:
                        for item in datalist:
                            f_out.write('\t'.join([country_name, country_code, continent, str(total), item['date'], item['open'],item['close'],item['rate']]) + '\n')

def outputToMariaDB():
    inputpath = os.path.join(os.getcwd(),'output','db.txt')
    if not os.path.exists(inputpath):
        return
    # 打开数据库
    db = pymysql.connect('112.125.25.230','klq26','abc123!@#==','finance')
    cursor = db.cursor()
    sql_placeholder = r"INSERT INTO year_klines(name, symbol, continent, total, date, open, close, rate) VALUES ('{0}', '{1}', '{2}', {3}, '{4}', '{5}', '{6}', '{7}')"
    with open(inputpath,'r',encoding='utf-8') as f:
        datalist = f.read().split('\n')
        for item in datalist:
            values = item.split('\t')
            if len(values) > 1:
                # print(values)
                try:
                    # 执行sql语句
                    sql = sql_placeholder.format(values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7])
                    print(sql)
                    cursor.execute(sql)
                    # 执行sql语句
                    db.commit()
                except Exception as e:
                    print(e)
                    # 发生错误时回滚
                    db.rollback()
        cursor.close()
        db.close()



if __name__ == "__main__":
    # 清洗数据
    # purgeEastmoneyYearData()
    # 整合所有国家指数到一个文件
    # combineAndOutputToTxt()
    # 写入阿里云数据库
    outputToMariaDB()