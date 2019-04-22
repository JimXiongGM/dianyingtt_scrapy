import scrapy,re,traceback
from scrapy.linkextractors import LinkExtractor
from ..items import DyttItem


class DyttSpider(scrapy.Spider):
    name = 'dianyingtt'
    allowed_domains = ['ygdy8.net']
    start_urls = ['http://www.ygdy8.net/html/gndy/dyzz/list_23_2.html']    
    
    def re_match(self,patten,text):
        try:
            matchobj = re.match(patten, text)
            return str(matchobj.group(1)).strip()
        except:
            #traceback.print_exc()
            return ''
    #清洗response
    def clean_response(self,response):
        try:
            temp = response.text.replace('\n','').replace('\r','').replace('&middot;','`').replace('&nbsp;','')\
                .replace('&ldquo;',' ').replace('&rdquo;',' ').replace('&rdquo;',' ').replace('&quot;',' ')\
                .replace('&lt;',' ').replace('&gt;',' ').replace('&amp;',' ')
            return temp
        except:
            #traceback.print_exc()
            return ''

    def parse(self, response):        
        # 电影链接
        for link in response.xpath('//a[@class="ulink"]/@href'):    
            next_url = 'http://www.ygdy8.net'+link.extract()             
            yield scrapy.Request(next_url, callback=self.parse_item)
        
        # 下一页
        next_page = response.xpath('//div[@class="x"]//a[last()-1]/@href').extract()
        for link in next_page:
            next_page_url = 'http://www.ygdy8.net/html/gndy/dyzz/'+ link
            yield scrapy.Request(next_page_url, callback=self.parse)           
    
    def parse_item(self, response):
        item = DyttItem()
        text = self.clean_response(response)
        #print (text)
        item['weburl'] = response.url
        item['tname'] = self.re_match('.*?\u8bd1[\u3000|\u0020][\u3000|\u0020]\u540d[\u3000|\u0020|\uff1a]([\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text)+\
        self.re_match('.*?\u4e2d[\u3000|\u0020]\u6587[\u3000|\u0020]\u540d[\u3000|\u0020|\uff1a]([\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text)  #译名+中文名ok        
        item['oname'] = self.re_match('.*?\u7247[\u3000|\u0020][\u3000|\u0020]\u540d[\u3000|\u0020|\uff1a]([\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text)+\
        self.re_match('.*?\u82f1[\u3000|\u0020]\u6587[\u3000|\u0020]\u540d[\u3000|\u0020|\uff1a]([\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text)  #片名+英文名ok        
        item['year'] = self.re_match('.*?\u5e74[\u3000|\u0020][\u3000|\u0020]\u4ee3[\u3000|\u0020|\uff1a]([\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text)   #年代ok
        item['country'] = self.re_match('.*?\u4ea7[\u3000|\u0020][\u3000|\u0020]\u5730[\u3000|\u0020|\uff1a]([\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text)+\
                    self.re_match('.*?\u56fd[\u3000|\u0020][\u3000|\u0020]\u5bb6[\u3000|\u0020|\uff1a]([\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text) #产地+国家ok 
        
        item['category'] = self.re_match('.*?\u7c7b[\u3000|\u0020][\u3000|\u0020]\u522b[\u3000|\u0020|\uff1a]([\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text)   #类别ok
        item['language'] = self.re_match('.*?\u8bed[\u3000|\u0020][\u3000|\u0020]\u8a00[\u3000|\u0020|\uff1a]([\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text)   #语言ok     
        item['word'] = self.re_match('.*?\u5b57[\u3000|\u0020][\u3000|\u0020]\u5e55[\u3000|\u0020|\uff1a]([\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text)   #字幕ok
        item['issuedata'] = self.re_match('.*?\u4e0a\u6620\u65e5\u671f[\u3000|\u0020|\uff1a](.*?[\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<',text)   #上映日期ok
        item['imdb'] = self.re_match('.*?\u0049\u004d\u0044\u0042\u8bc4\u5206[\u3000|\u0020|\uff1a](.*?[\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text)   #IMDb评分ok
        item['douban'] = self.re_match('.*?\u8c46\u74e3\u8bc4\u5206[\u3000|\u0020|\uff1a](.*?[\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text)   #豆瓣评分ok
        item['fileformat'] = self.re_match('.*?\u6587\u4ef6\u683c\u5f0f[\u3000|\u0020|\uff1a](.*?[\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text)   #文件格式ok
        item['movielens'] = self.re_match('.*?\u7247[\u3000|\u0020][\u3000|\u0020]\u957f[\u3000|\u0020|\uff1a](.*?[\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<.*?',text)   #片长ok
        item['director'] = self.re_match('.*?\u5bfc[\u3000|\u0020][\u3000|\u0020]\u6f14[\u3000|\u0020|\uff1a](.*?[\u4e00-\u9fa5_a-zA-Z0-9 ].*?)<',text)   #导演ok
        item['ftpurl'] = self.re_match('.*?a href="(ftp://.*?)".*?',text) #ftpok 
   

        yield item
