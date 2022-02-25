import re
import requests
import sys
class EnumAll:
    urls_list = []
    files_found = []
    def geturl(self,url):
        self.header={'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9'}
        global p
        p=requests.get(url,headers=self.header)
    def start(self,search,string):
        addup=[]
        i=0
        findings = search.finditer(string)
        for url in findings:
            if url.group(0) not in addup:
                addup.append(url.group(0))
                print(addup[i])
                i+=1
        print("\tTotal = %i"%i)
        return addup
    def url_search(self, urls, extension):
        for index,url in enumerate(urls):
            u=p.url.rstrip("/")+url
            u=requests.get(u,headers=self.header)
            #print(u.url,u.status_code)
            if u.status_code==200:
                self.urls_list.append(u.url)
                url_200 = requests.get(u.url,headers=self.header)
                pattern = re.compile(r'/[a-zA-Z0-9/]+.%s'% extension, re.I) #crazy
                url_return=self.start(pattern,url_200.text)
                self.files_found.append(url_return)
        print("Found :",self.files_found)
        print("Webpages :",self.urls_list)
    def any_file(self,any_file,extension):
        #search = re.compile(r'\/[a-zA-Z0-9+-_]+\.%s'% extension, re.I) #crazy
        self.search = re.compile('/[a-zA-Z0-9/]+/', re.I) #crazy
        #for http(s):// uncomment
        #self.search = re.compile(r'htt(p|ps)://(www\.)?([a-zA-Z0-9]+\.\w{2,})(\.\w{2,})?(\.\w{2,})?\/.+\.%s'% extension, re.I)

        urls=self.start(self.search,any_file)
        self.url_search(urls,extension)
    def domain(self,_domain):
        search = re.compile(r'htt(p|ps)://(www\.)?([a-zA-Z0-9]+\.\w{2,})(\.\w{2,})?(\.\w{2,})?', re.I)
        self.start(search,_domain)
    def phone(self,_phone):
        search = re.compile(r'\+?([)(][0-9]{2,}[()])?[0-9]{2,}[-*][0-9]{2,}[-*]([0-9]{2,}[-*])?([0-9]{1,})?', re.I)
        self.start(search,_phone)
    def email(self,_email):
        search = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.+]+\.[a-zA-Z]{2,}', re.I)
        self.start(search,_email)
    def banner(self):
        print("""\n
        ███████ ███    ██ ██    ██ ███    ███ 
        ██      ████   ██ ██    ██ ████  ████ 
        █████   ██ ██  ██ ██    ██ ██ ████ ██ 
        ██      ██  ██ ██ ██    ██ ██  ██  ██ 
        ███████ ██   ████  ██████  ██      ██ 
                                            
    '-->@4yub1k  -->Youtube: Nerdy Ayubi                                                                            """)
    def help(self):
        print("""[OPTIONS-HELP]
        -u\tUrl to search in.
        -p\tSearch for phone numbers
        -d\tGrab all domains from source
        -e\tSearch for emails
        -ff\tSearch for specfific file
        enum1.py -u http://<url> <option>
        """)

if __name__=="__main__":
    try:
        sys.argv.append("0") #temporary Fix
        enum=EnumAll()
        enum.banner()
        if sys.argv[1] !='0':
            for i in range(1,len(sys.argv)-1):
                if '-u'==sys.argv[i]:
                    web=sys.argv[i+1]
                    enum.geturl(web)
                elif '-p'==sys.argv[i]:
                    print("----------------Phone----------------")
                    enum.phone(p.text)
                elif '-d'==sys.argv[i]:
                    print("----------------Domains----------------")
                    enum.domain(p.text)       
                elif '-e'==sys.argv[i]:
                    print("----------------Emails----------------")
                    enum.email(p.text)
                elif '-f'==sys.argv[i]:
                    print("----------------File/Extensions----------------")
                    enum.url(p.text,sys.argv[i+1])
                    print("----------------File/Extensions----------------")
                    enum.any_file(p.text,sys.argv[i+1])
                elif '-ff'==sys.argv[i]:
                    print("----------------Specific----------------")
                    enum.any_file(p.text,sys.argv[i+1])
                elif '-h'==sys.argv[i]:
                    print("----------------Specific----------------")
                    enum.help()
        else:
            raise Exception("Please provide any options !")
    except requests.exceptions.ConnectionError:
        print(r"Make sure the url is accessable : %s" % web)
    except Exception as error:
        print(error)
