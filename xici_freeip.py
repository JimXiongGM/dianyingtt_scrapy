# coding=utf-8
import re,requests,time
from scrapy.selector import Selector

def crawl_ips(page_num=100):
    # 爬取西刺的免费ip代理
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}
    ip_list = []
    for i in range(page_num):
        res = requests.get(
            "http://www.xicidaili.com/wt/{0}".format(i),
            headers=headers)
        #time.sleep(1)
        selector = Selector(text=res.text)
        all_trs = selector.css("#ip_list tr")

        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split(u"秒")[0])
            all_texts = tr.css("td::text").extract()
            cunhuo = tr.css("td::text").extract()
            match_obj1 = re.match(".*'HTTPS'.*", str(all_texts))
            match_obj2 = re.match(".*'HTTP'.*", str(all_texts))
            proxy_type = ""
            if match_obj1:
                proxy_type = "HTTPS"
                continue
            elif match_obj2:
                proxy_type = "HTTP"
            ip = all_texts[0]
            port = all_texts[1]
            if u'分钟' not in all_texts[10]:
                #print all_texts[10]
                #ip_list.append(str(ip)+':'+str(port)+'\t'+str(proxy_type)+'\t'+str(speed))
                if speed<1:
                    ip_list.append(str(ip) + ':' + str(port))

    with open('xici_freeip.txt','w')as res_file:
        for line in ip_list:
            res_file.write(line+'\n')
    print 'sucess ',len(ip_list)

if __name__ == '__main__':
    crawl_ips(5)