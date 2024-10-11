import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import time
import re

from lxml import etree

from base import BaseSpider


# 提取文本，自动在换行标签等位置加上换行符或空格
def extract_text_with_formatting(element):
    text_list = []
    
    for node in element.iter():
        if node.tag == 'br':  # 遇到 <br> 标签时添加换行符
            text_list.append('\n')
        elif node.tag == 'b':  # 处理 <b> 标签的文本
            if node.text:
                text_list.append(node.text.replace(u'\u00A0', ' '))  # 替换 &nbsp; 为普通空格
            text_list.append('\n')  # 在 <b> 结束后添加换行
        elif node.text:
            text_list.append(node.text.replace(u'\u00A0', ' '))  # 替换 &nbsp;
        
        if node.tail:
            text_list.append(node.tail.replace(u'\u00A0', ' '))  # 替换 &nbsp;

    return ''.join(text_list).strip()

class CMSOET_Spider(BaseSpider):
    def parse_name_homepage_dict(self, content):
        try:
            tree = etree.HTML(content)
            yp_ity_list = tree.xpath(self.xpath_dict["identity_xpath"])
            name_homepage_dict = {}
            for yp_ity in yp_ity_list:
                name = yp_ity.xpath(self.xpath_dict["name_xpath"])[0]
                homepage_url = yp_ity.xpath(self.xpath_dict["homepage_xpath"])[0]
                homepage_url = homepage_url.replace("http:", "https:")
                name_homepage_dict[name] = homepage_url
            return name_homepage_dict
        except Exception as e:
            print(f"Error parsing homepage: {e}")
            return {}
    
    def parse_name_email_dict(self, content):
        try:
            tree = etree.HTML(content)
            bp_enty = tree.xpath('//div[@class="bp-enty"]')[0]
            text_content = bp_enty.xpath('string(.)').strip()  # 提取元素内的文本内容
            # text_content = extract_text_with_formatting(bp_enty)
            text_content = re.sub(r'\s+', ' ', text_content)
            print(text_content)
            # 使用正则表达式查找邮箱地址
            emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text_content)
            # emails = re.findall(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(?:\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$', text_content)

            # 输出找到的邮箱地址
            print("找到的邮箱地址：", emails)
            return {}
        except Exception as e:
            print(f"Error parsing homepage: {e}")
            return {}

    def run(self):
        """Run the spider to fetch and parse."""
        content = self.fetch_page(self.url)
        if content:
            name_homepage_dict = self.parse_name_homepage_dict(content)
            print(f"Found {len(name_homepage_dict)} links:")
            count = 0
            for name, homepage_url in name_homepage_dict.items():
                print(name, homepage_url)
                homepage_content = self.fetch_page(homepage_url)
                if homepage_content:
                    self.parse_name_email_dict(homepage_content)
                    time.sleep(1.5)
                print("="*100)
                count +=1
                if count > 20:
                    break
        else:
            print("No content to parse.")


if __name__ == "__main__":
    
    url = "https://cmo.ucas.ac.cn/index.php/zh-cn/szdw/graduateteacher"  # Replace with your target URL
    xpath_dict = {
        "identity_xpath": '//div[@class="yp_ity"]',
        "name_xpath": './a/p/text()',
        "homepage_xpath": './a/@href'
    }
    spider = CMSOET_Spider(url, xpath_dict)
    spider.run()

# export PYTHONPATH="$PWD" python universities\University_of_Chinese_Academy_of_Sciences\College_of_Materials_Science_and_Opto-Electronic_Technology.py