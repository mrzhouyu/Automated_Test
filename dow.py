'''
首次启动时需要输入用例编号，之后顺延用例编号，直到出现重复的编号时提示输入新的用例编号
'''
import time
from prettytable import PrettyTable
import os,sys


def start():
	print('\n\n★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★欢迎使用旷视收银系统☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆')
	if os.path.isfile(os.path.join(sys.path[0], 'log.csv')) is False:
		with open('log.csv', 'w', encoding='utf-8') as f:
			f.write('用例编号, 交易时间, 商品编码, 商品名称, 商品分类_1, 商品分类_2, 单价, 数量, 总价\n')
	with open('log.csv', 'r', encoding='utf-8') as f:
		content = f.readlines()
	order_id = input('请输入用例编号：')
	while order_id.isdigit() is False:
		order_id = input('用例编号无效，请重新输入订单起始编号：')
	for i in content:
		if order_id == i.split(',')[0]:
			print('用例编号已存在，请重新输入：')
			start()
	order_id = int(order_id)
	erp = get_sku_info()
	buy_list = []
#	print(erp)

	while True:
		co = buy(erp, buy_list, order_id)
		if co == False:
			break
	#save log into log.csv
	for i in buy_list:
		with open('log.csv', 'a', encoding='utf-8') as f:
			f.write(i)
	show_table(buy_list)
	print('\n\n☆★☆★☆★☆★☆★☆★☆★☆★☆★☆感谢惠顾，欢迎下次光临！★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★\n\n')
	s_loop(erp, order_id)

def s_loop(erp, order_id):
	buy_list = []
	while True:
		order_id += 1
		with open('log.csv', 'r', encoding='utf-8') as f:
			content = f.readlines()
			latest_order_id = content[-1].split(',')[0]
		for i in content[1:]:
			id  = i.split(',')[0]
			if order_id == int(id):
				order_id = input('*********！！！用例编号已存在，请重新输入！！！*********：')
				break
		co = buy(erp, buy_list, order_id)
		if co == False:
			break
	# save log into log.csv
	for i in buy_list:
		with open('log.csv', 'a', encoding='utf-8') as f:
			f.write(i)
	show_table(buy_list)
	print('\n\n☆★☆★☆★☆★☆★☆★☆★☆★☆★☆感谢惠顾，欢迎下次光临！★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★\n\n')
	s_loop(erp, order_id)

def get_sku_info():
	with open('new_erp.csv', 'r', encoding='utf-8') as f:
		content = f.readlines()
	sku_list = []
	for i in content[1:]:
#       0 No, 1 shop_sku, 2 barcode, 3 sku_info, 4 price, 5 weight
		sku_info = [i.split(',')[0],i.split(',')[1],i.split(',')[2],i.split(',')[3],i.split(',')[4],i.split(',')[5],i.split(',')[6],i.split(',')[7],i.split(',')[8][:-1]]
		sku_list.append(sku_info)
	return sku_list


def buy(erp, buy_list, order_id):
	with open('log.csv', 'r', encoding='utf-8') as f:
		content = f.readlines()
#	order_id = int(content[-1].split(',')[0]) + 1
	print(('########################################### %s  %s ###########################################' % (
		order_id, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))))
	print('****************(R：重新扫描本单；DEL 订单号：删除订单；LIST：查看订单历史)****************')
	barcode = input('请输入命令或直接扫描商品编码：')
	current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#	current_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
	while (barcode.isdigit() and 0 < len(barcode) < 5) or barcode == '':
		print('(R：重新扫描本单；DEL 订单号：删除订单；LIST：查看订单历史)')
		barcode = input('!!!!!!!!!!!!!!!!!!!!!!!!!!!!编码有误，请重新输入命令或扫描商品编码!!!!!!!!!!!!!!!!!!!!!!!!!!!!：')
	if barcode == '':
		return False
	elif barcode == 'r' or barcode == 'R':
		s_loop(erp, order_id)
	elif barcode[:3] == 'del' or barcode[:3] == 'DEL':
		del_order_id = barcode.split(' ')[1]
		del_order_list = []
		for i in range(len(content)):
			if del_order_id == content[i].split(',')[0]:
				del_order_list.append(content[i])
		x = PrettyTable(['订单号', '交易时间', '商品编码', '商品名称', '商品分类_1', '商品分类_2', '单价', '数量', '总价'], encoding='utf-8')
		for i in del_order_list:
			x.add_row(i[:-1].split(','))
		print(x)
		conform = input('确认删除?（Y：确认；N：取消）:')
		if conform == 'y' or conform == 'Y':
			for i in del_order_list:
				for j in range(len(content)):
					if i == content[j]:
						content.remove(i)
			with open('log.csv', 'a', encoding='utf-8') as f:
				f.seek(0)
				f.truncate()
				for i in content:
					f.write(i)
			s_loop(erp, order_id)
		else:
			s_loop(erp, order_id)
	elif barcode == 'list' or barcode == 'LIST':
		print_log('log')
	for i in erp:
		sku_barcode = i[2]
		sku_name = i[3]
		sku_price = float(i[5])
		sku_cat1 = i[7]
		sku_cat2 = i[8]
		if barcode == sku_barcode:
			print('【%s】' % sku_name, end = '')
			quantity = input('请输入商品数量：')
			while len(quantity) > 2:
				quantity = input('库存不足，请重新输入商品数量：')
			if len(quantity) == 0:
				quantity = 1
			total = sku_price * int(quantity)
#			print('%s\t%s\t%s\t%s\t%s' % (sku_barcode, sku_name, sku_price, quantity, total))
			buy = '%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (order_id, current_time, sku_barcode, sku_name, sku_cat1, sku_cat2, sku_price, quantity, total)
			buy_list.append(buy)
			x = PrettyTable(['订单号', '交易时间', '商品编码', '商品名称', '商品分类_1', '商品分类_2', '单价', '数量', '总价'], encoding='utf-8')
			x.add_row(buy[:-1].split(','))
			#print(x)
			#print('\n\n')
			return False
	print('\n\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■命令错误，请重试■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n\n')
	return True


def print_log(file_name, erp, order_id):
	with open('{}.csv'.format(file_name), 'r', encoding='utf-8') as f:
		content = f.readlines()
	x = PrettyTable(['订单号', '交易时间', '商品编码', '商品名称', '商品分类_1', '商品分类_2', '单价', '数量', '总价'], encoding='utf-8')
	total_count = []
	total_quantity = []
	for i in content:
		total_count.append(float(i[:-1].split(',')[-1]))
		total_quantity.append(int(i.split(',')[-2]))
		x.add_row(i.split(','))
	x.add_row(
		['----------', '----------', '----------', '--------------------', '----------', '----------', '----------',
		 '----------', '----------'])
	total_count = float('{:.2f}'.format(sum(total_count)))
	total_quantity = sum(total_quantity)
	print(x)
#	print('\n\n')
	s_loop(erp, order_id)

def show_table(buy_list):
	print('\n')
	x = PrettyTable(['测试用例', '交易时间', '商品编码', '商品名称', '商品分类_1', '商品分类_2', '单价', '数量', '总价'], encoding='utf-8')
	total_count = 0
	for i in buy_list:
		x.add_row(i[:-1].split(','))
		total_count += float(i[:-1].split(',')[-1])
	print(x)

if __name__ == '__main__':
    start()