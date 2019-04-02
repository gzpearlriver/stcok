#!/usr/bin/python
# -*- coding: UTF-8 -*-
#allow chinese character in program

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
#add above to prevent this error : "UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 0: ordinal not in range(128)"

    
'''基于sqlite3的数据，输出图像化分析结果'''
    
import numpy as np
import pandas as pd
import sqlite3 as lite
import matplotlib.pyplot as plt
import pathlib

from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

chart_income_items=('营业收入年化',
'营业利润年化',
'净利润年化',
'归属于母公司所有者的净利润年化',
'经营活动产生的现金流量净额年化',
'营业税金及附加年化')


chart_value_items=('资产总计(万元)',
'负债合计(万元)',
'非流动资产合计(万元)',
'流动资产合计(万元)',
'非流动负债合计(万元)',
'流动负债合计(万元)')

chart_money_items=('货币资金(万元)',
'期末现金及现金等价物余额(万元)',
'资产总计(万元)',
'负债合计(万元)',
'所有者权益或股东权益合计(万元)',
'存货(万元)')

chart_rate_items=('ROE',
'ROA',
'资产负债率',
'毛利率',
'母公司利润比例',
'经营现金流净额比利润',
'现金流入比营业收入')

chart_cashflow_items=('营业收入年化',
'经营活动现金流入小计年化',
'经营活动现金流出小计年化',
'经营活动产生的现金流量净额年化',
'投资活动产生的现金流量净额年化',
'筹资活动产生的现金流量净额年化')

#'购买商品、接受劳务支付的现金(万元)',
#'筹资活动现金流入小计(万元)',
#'筹资活动现金流出小计(万元)',
#'投资活动现金流入小计(万元)',
#'投资活动现金流出小计(万元)',

chart_yoy_items=('营业收入YOY',
'净利润YOY',
'所有者权益或股东权益合计YOY',
'资产总计YOY',
'负债合计YOY')


#流动资产
chart_ldzc_items=('货币资金(万元)',
'结算备付金(万元)',
'拆出资金(万元)',
'交易性金融资产(万元)',
'衍生金融资产(万元)',
'应收票据(万元)',
'应收账款(万元)',
'预付款项(万元)',
'应收保费(万元)',
'应收分保账款(万元)',
'应收分保合同准备金(万元)',
'应收利息(万元)',
'应收股利(万元)',
'其他应收款(万元)',
'应收出口退税(万元)',
'应收补贴款(万元)',
'应收保证金(万元)',
'内部应收款(万元)',
'买入返售金融资产(万元)',
'存货(万元)',
'待摊费用(万元)',
'待处理流动资产损益(万元)',
'一年内到期的非流动资产(万元)',
'其他流动资产(万元)')

#非流动资产
chart_fldzc_items=('发放贷款及垫款(万元)',
'可供出售金融资产(万元)',
'持有至到期投资(万元)',
'长期应收款(万元)',
'长期股权投资(万元)',
'其他长期投资(万元)',
'投资性房地产(万元)',
'固定资产(万元)',
'在建工程(万元)',
'工程物资(万元)',
'固定资产清理(万元)',
'生产性生物资产(万元)',
'公益性生物资产(万元)',
'油气资产(万元)',
'无形资产(万元)',
'开发支出(万元)',
'商誉(万元)',
'长期待摊费用(万元)',
'股权分置流通权(万元)',
'递延所得税资产(万元)',
'其他非流动资产(万元)')

#非流动负债
chart_ldfz_items=('短期借款(万元)',
'向中央银行借款(万元)',
'吸收存款及同业存放(万元)',
'拆入资金(万元)',
'交易性金融负债(万元)',
'衍生金融负债(万元)',
'应付票据(万元)',
'应付账款(万元)',
'预收账款(万元)',
'卖出回购金融资产款(万元)',
'应付手续费及佣金(万元)',
'应付职工薪酬(万元)',
'应交税费(万元)',
'应付利息(万元)',
'应付股利(万元)',
'其他应交款(万元)',
'应付保证金(万元)',
'内部应付款(万元)',
'其他应付款(万元)',
'预提费用(万元)',
'预计流动负债(万元)',
'应付分保账款(万元)',
'保险合同准备金(万元)',
'代理买卖证券款(万元)',
'代理承销证券款(万元)',
'国际票证结算(万元)',
'国内票证结算(万元)',
'递延收益(万元)',
'应付短期债券(万元)',
'一年内到期的非流动负债(万元)',
'其他流动负债(万元)')

#非流动负债
chart_fldfz_items=('长期借款(万元)',
'应付债券(万元)',
'长期应付款(万元)',
'专项应付款(万元)',
'预计非流动负债(万元)',
'长期递延收益(万元)',
'递延所得税负债(万元)',
'其他非流动负债(万元)')

chart_crqr_items=('流动比率',
'速动比率',
'保守速动比率')
#'产权比率',
#'有形净值债务率'

chart_zzczb_items=('本公司账户类现金与总资产比值',
'非本公司账户类现金与总资产比值')

#所有收入
chart_earning_items=('营业收入(万元)',
'利息收入(万元)',
'已赚保费(万元)',
'手续费及佣金收入(万元)',
'房地产销售收入(万元)',
'其他业务收入(万元)',
'公允价值变动收益(万元)',
'投资收益(万元)',
'对联营企业和合营企业的投资收益(万元)',
'汇兑收益(万元)',
'期货损益(万元)',
'托管收益(万元)',
'补贴收入(万元)',
'其他业务利润(万元)')

#所有成本
chart_cost_items=('营业成本(万元)',
'利息支出(万元)',
'手续费及佣金支出(万元)',
'房地产销售成本(万元)',
'研发费用(万元)',
'退保金(万元)',
'赔付支出净额(万元)',
'提取保险合同准备金净额(万元)',
'保单红利支出(万元)',
'分保费用(万元)',
'其他业务成本(万元)',
'营业税金及附加(万元)',
'销售费用(万元)',
'管理费用(万元)',
'财务费用(万元)',
'资产减值损失(万元)')

#利润
chart_profit_items=('营业利润(万元)',
'营业外收入(万元)',
'营业外支出(万元)',
'非流动资产处置损失(万元)',
'利润总额(万元)',
'所得税费用(万元)',
'未确认投资损失(万元)',
'净利润(万元)',
'归属于母公司所有者的净利润(万元)')




def n_ticks(index,n):
    xticks=list(range(0,len(index),len(index)//n))
    xlabels=[index[x] for x in xticks]
    xticks.append(len(index))
    xlabels.append(index[-1])
    return xticks,xlabels


def draw_scatter(title, horizon_source, vertical_source):
    pic_filename = pic_dir  + title + '.png'
    fig1 = plt.figure()
    fig1.set_size_inches(12, 8 * 1)
    
    try:
       
        ax1 = fig1.add_subplot(111)  
        ax1.scatter(horizon_source, vertical_source)
        ax1.set_title(title)
        ax1.legend(loc='upper right')
 
        '''xticks,xlabels = n_ticks(list(index),30)
        ax1.set_xticks(xticks)
        ax1.set_xticklabels(xlabels, rotation=270)'''
    
    except:
        print ("drawing  failed!")
        
    plt.subplots_adjust(bottom=.1, top=.9, left=.1, right=.9)
    #plt.show()
    fig1.savefig(pic_filename, dpi=100)
    del fig1
    plt.close('all')

def draw_kmonth(title,left_source,right_source,index):
    pic_filename = stock_dir + "/" + stock_code + stock_name + '_' + title + '.png'
    fig1 = plt.figure()
    fig1.set_size_inches(12, 8 * 1)
    

    if True:
        ax1 = fig1.add_subplot(111)  
        ax1.plot(index, left_source,color='blue')
        ax1.set_title(stock_name + " " + title)
        ax1.legend(loc='upper left')
        
        ax2=ax1.twinx()
        ax2.plot(index, right_source, color='red')       
        ax2.legend(loc='upper right')

        xticks,xlabels = n_ticks(list(index),30)
        ax1.set_xticks(xticks)
        ax1.set_xticklabels(xlabels, rotation=270)
    try:
        print ("test")     
    except:
        print ("drawing  failed!")
        
    plt.subplots_adjust(bottom=.1, top=.9, left=.1, right=.9)
    #plt.show()
    fig1.savefig(pic_filename, dpi=100)
    del fig1
    plt.close('all')
    
def versus(stock_code , stock_name):
    #各种对比
    stock_dir=pic_dir + stock_code + stock_name

    print(stock_dir)
    pathlib.Path(stock_dir).mkdir(parents=True, exist_ok=True) 


    query = "SELECT * from kmonth_ext where code='" + stock_code + "';"
    onestock = pd.read_sql_query(query,conn)
    print(onestock.columns)
    
    #onestock = kmonth_ext[kmonth_ext['name']==stock_name]
    #onestock = onestock[onestock['date'] > '2010']
    #print(len(onestock))
    
    draw_kmonth('总市值 vs 收市价',onestock['总市值'],onestock['close'],onestock['date'])
    draw_kmonth('每股盈利 vs 收市价',onestock['基本每股收益年化'],onestock['close'],onestock['date'])
    draw_kmonth('每股净资产 vs 收市价',onestock['每股净资产'],onestock['close'],onestock['date'])
    draw_kmonth('PE vs 收市价',onestock['PE'],onestock['close'],onestock['date'])
    draw_kmonth('PEG vs 总市值',onestock['PEG'],onestock['总市值'],onestock['date'])
    draw_kmonth('PB vs 总市值',onestock['PB'],onestock['总市值'],onestock['date'])
    draw_kmonth('ROE vs 总市值',onestock['ROE'],onestock['总市值'],onestock['date'])
    draw_kmonth('ROA vs 总市值',onestock['ROA'],onestock['总市值'],onestock['date'])
    draw_kmonth('毛利率',onestock['毛利率'],onestock['总市值'],onestock['date'])


def draw_multiline(title, chart_items,stock_data):
    pic_filename = stock_dir + "/" + stock_code + stock_name + '_' + title + '.png'
    fig1 = plt.figure()
    fig1.set_size_inches(12, 8 * 1)
    ax1 = fig1.add_subplot(111)  
    
    #print(chart_items)    
    for item in chart_items:
        if item in stock_data.columns:
            #print(stock_data.index, stock_data[item])
            ax1.plot(stock_data['date'], stock_data[item]) 

    ax1.set_title(stock_name + '  ' + title)
    ax1.legend(loc='upper left')
    for tick in ax1.get_xticklabels():
        tick.set_rotation(270)        
    
    plt.subplots_adjust(bottom=.1, top=.9, left=.1, right=.9)
    #plt.show()
    fig1.savefig(pic_filename, dpi=100)
    del fig1
    plt.close('all')
    

def draw_stack(title, chart_items, stock_data):
    pic_filename = stock_dir + "/" + stock_code + stock_name + '_' + title + '.png'
    fig1 = plt.figure()
    fig1.set_size_inches(12, 8 * 1)
    
    
    df1= pd.DataFrame()
    for item in chart_items:
        if item in stock_data.columns :
            df1[item] = stock_data[item]        
    #print(df1)
    
    ax1 = fig1.add_subplot(111)  
    y = np.array(df1.T)

    ax1.stackplot(stock_data['date'], y, labels=chart_items) 
    ax1.set_title(stock_name + '  ' + title)  
    ax1.legend(loc='upper left')
    for tick in ax1.get_xticklabels():
        tick.set_rotation(270)
    del y, df1         
    
    plt.subplots_adjust(bottom=.1, top=.9, left=.1, right=.9)
    #plt.show()
    print(pic_filename)
    fig1.savefig(pic_filename, dpi=100)
    del fig1
    plt.close('all')


def finance_report(stock_code , stock_name):
    #各种对比
    stock_dir = pic_dir + stock_code + stock_name

    print(stock_dir)
    try:
        pathlib.Path(stock_dir).mkdir(parents=True) 
    except:
        print("dir already exist!")

    query = "SELECT * from stock where code='" + stock_code + "';"
    onestock = pd.read_sql_query(query,conn)
    #print(onestock.columns)
    #print(len(onestock))
    csv_filename = stock_dir + "/" + stock_code + stock_name + '.csv'
    onestock.to_csv(csv_filename,encoding='utf_8_sig')
     
    draw_stack('流动资产', chart_ldzc_items, onestock)
    draw_stack('非流动资产', chart_fldzc_items, onestock)
    draw_stack('流动负债', chart_ldfz_items, onestock)
    draw_stack('非流动负债', chart_fldfz_items, onestock)
    draw_stack('收入', chart_earning_items, onestock)
    draw_stack('成本', chart_cost_items, onestock)
    
    draw_multiline('利润', chart_profit_items, onestock)
    draw_multiline('年化营收', chart_income_items, onestock)
    draw_multiline('资产与负债', chart_value_items, onestock)
    draw_multiline('资产与资金', chart_money_items, onestock)
    draw_multiline('现金流', chart_cashflow_items, onestock)
    draw_multiline('ROE和毛利率', chart_rate_items, onestock)
    draw_multiline('年增长', chart_yoy_items, onestock)
    draw_multiline('流动比率、速动比率和保守速动比率', chart_crqr_items, onestock)
    draw_multiline('本公司现金和非本公司现金', chart_zzczb_items, onestock)



#main program begin here    
#db_file = '/code/stock/stock.db'
#pic_dir = '/stockdata/pic/'
db_file = 'D:\\stockdata\\stock.db'
pic_dir = 'D:\\stockdata\\pic\\'
conn=lite.connect(db_file)
cur = conn.cursor()

stock_name='安道麦'
stock_code='000553'
stock_dir=pic_dir + stock_code + stock_name

#versus(stock_code , stock_name)
finance_report(stock_code , stock_name)

'''query = "SELECT * from kmonth_ext;"
kmonth_ext = pd.read_sql_query(query,conn)
kmonth_ext = kmonth_ext[kmonth_ext['date'] > '2014']

grouped_stock=kmonth_ext.groupby('name')
stock_mean=grouped_stock.mean()
stock_sum=grouped_stock.sum()
stock_sum['PE合计'] = stock_sum['close'] / stock_sum['每股盈利年化']
stock_sel = stock_mean
stock_sel['PE合计'] = stock_sum['PE合计'] 
stock_sel = stock_sel[stock_sel['营业利润YOY'] > 0]
stock_sel = stock_sel[stock_sel['营业利润YOY'] < 3]
stock_sel = stock_sel[stock_sel['净利润YOY'] > 0]
stock_sel = stock_sel[stock_sel['净利润YOY'] < 3]
stock_sel = stock_sel[stock_sel['PE合计'] > 0]
stock_sel = stock_sel[stock_sel['PE合计'] < 30]
stock_sel.to_csv('d:/stockdata/lowpe.csv')


horizon_source = stock_sel['PE合计'] 
vertical_source = stock_sel['营业利润YOY']
draw_scatter('PE vs 营业利润YOY', horizon_source, vertical_source)
'''
