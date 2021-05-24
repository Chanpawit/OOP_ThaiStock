from tkinter import *
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup

GUI = Tk()
GUI.geometry('800x500')
GUI.title('Program Check Thai Stock')
GUI.wm_iconbitmap('money.ico')
GUI.config(background='#545763')

FONT1 = ('Calibri bold',20)

my_frame = Frame(GUI)
my_frame.pack(pady=0)
my_frame.config(background='#545763')



L = ttk.Label(GUI, text='Program Take Thailand Stock Data', font=FONT1, background='#545763',foreground='white')
L.pack(pady=20)

def Checkprice(QUOTE='KBANK'):
	global datetime
	url = 'https://www.settrade.com/C04_01_stock_quote_p1.jsp?txtSymbol={}&ssoPageId=9&selectPage=1'.format(QUOTE)

	rawdata = requests.get(url)
	rawdata = rawdata.content

	data = BeautifulSoup(rawdata, 'html.parser')

	price = data.find_all('div', {'class':'col-xs-6'})

	name = price[0].text.strip()
	stprice = float(price[2].text.strip())
	change = float(price[3].text.split()[-1])
	percentchange = float(price[4].text.split()[-1].replace('%',''))

	Classvice = data.find('div', {'class':'flex-item text-left padding-8'})
	datetime = Classvice.find_all('span')[0].text.replace(' ','')
	StatusMarket = Classvice.find_all('span')[1].text
	#print(datetime)

	result = {'name':name, 
	'price':stprice, 
	'change':change,
	'percentchange':percentchange, 
	'datetime':datetime, 
	'status':StatusMarket}

	# print(result)
	return result
	return datetime

allresult = []


def CheckStockPrice(event=None):
	global allresult
		
	for rs in allresult:
                rs.destroy()

	allresult = []
		
	v_result.set('')
	quote = v_quote.get().split(',')
	print(quote)


	for q in quote:
		try:
			price = Checkprice(q)
			print(price,'\n')
			text = '{} : {} Baht'.format(price['name'], price['price'])
			text = text + '  Change {} Baht, {} %'.format(price['change'], price['percentchange'])
			if price['percentchange'] < 0:
				color = '#FA4309'
			elif price['percentchange'] == 0:
				color = '#09FA7A'
			elif price['percentchange'] > 10:
				color = '#FAE809'
			else:
				color = '#09FAF6'
		except:
			text = "System: '{}' Is not defined".format(q)
			color = '#FFA21D'
			pass

		L = ttk.Label(GUI, text=text, foreground=color,background='#545763', font=FONT1)
		allresult.append(L)
		L.pack()

v_quote = StringVar()
E1 = ttk.Entry(GUI, textvariable=v_quote, font=FONT1)
E1.pack(pady=20)

E1.bind('<Return>', CheckStockPrice)

B1 = ttk.Button(GUI, text='Save', command=CheckStockPrice)
B1.pack(ipady=10, ipadx=10)

v_result = StringVar()
v_result.set('-----------Result-----------')
FONT2 = ('Calibri bold',25)

R1 = ttk.Label(GUI, textvariable=v_result, font=FONT2, background='#545763')
R1.pack(pady=20)


GUI.mainloop()
