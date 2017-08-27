pip install scrapy

scrapy startproject novelcrawl
cd novelcrawl
scrapy genspider jianke
scrapy crawl jianke

但是, scrapy是无序的


使用requests和beautifulsoup重写
pip install requests beautifulsoup