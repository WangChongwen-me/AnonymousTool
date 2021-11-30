import requests
import json
import argparse
import base64
import codecs

if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='FoFa Search')
   parser.add_argument('-e','--email',help='fofa email',default='')
   parser.add_argument('-k','--key',help='fofa key',default='')
   args = parser.parse_args()
   email = args.email
   key = args.key
   fofa_url = "https://fofa.so/api/v1/info/my?email={}&key={}".format(email,key)
   header = {
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
   "Content-Type": "application/x-www-form-urlencoded"
       }
   res = requests.get(fofa_url, headers=header)
   if email != None and key != None:
       if 'errmsg' not in res.text:
           print("[+] FoFa接口认证成功")
       else:
           print("[-] FoFa接口认证失败，请检查KEY值")
   fofa_search = 'app="Apache-Shiro"'
   sentence = base64.b64encode(fofa_search.encode('utf-8')).decode("utf-8")
   #print(sentence)
   fofa_search_url = "https://fofa.so/api/v1/search/all?email={}&key={}&qbase64={}".format(email,key,sentence)
   res = requests.get(fofa_search_url, headers=header)
   if 'errmsg' not in res.text:
       result = json.loads(res.text)
       for link in result['results']:
               print(link[0])
   else:
       print("[-] 查询失败，请检查fofa语句或key值")