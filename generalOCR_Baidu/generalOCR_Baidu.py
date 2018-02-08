# #baidu AI general OCR request output format:
# {
#     'log_id': 5759721343299524124,
#     'words_result_num': 2,
#     'words_result':
#         [
#             {'words': '致年国体米:'},
#             {'words': '为中国队加m边'},
#         ]
# }

from __future__ import print_function
import requests
import base64
import ssl,sys

url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'  

data = {}  
data['access_token']='24.a1a5534d773f63a353e1f80ecb68ec65.2592000.1520403716.282335-10795879'

headers={
    "Content-Type":"application/x-www-form-urlencoded",
    "apikey":"1nCvv5ggca8GYtlNWjEQokuE"
}


#read image

num = 1
while True:
	if num <= 1:
		imgname = str(num) + '.jpg'
		file = open(imgname,'rb')
		image= file.read()
		file.close()
		num += 1
		data['image'] = base64.b64encode(image)
		res = requests.post(url=url,headers=headers,data=data)
		print (res,type(res),"\n")
		result = res.json()
		print (type(result), result,"\n")
		print(imgname, "\n")
		with open("2.txt","a") as f:
				for line in result["words_result"]:
					# print (line["words"],end="")
					print(line["words"])
					f.write(line["words"]+"\n")
		print("\n")
	else:
		break


  



