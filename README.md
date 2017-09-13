# tax-policy-crawler
从国税总局，及其他税务相关机构的网站，爬取税收政策、解读、条约等信息，以备后续处理

# 技术特点：
1. 反爬虫相关的优化：
动态ua
动态IP代理（采用[proxy_pool](https://github.com/jhao104/proxy_pool)的开源服务）
延迟下载：配置处理（scrapy的系统middleware处理）
启用/禁用cookies：配置处理（scrapy的系统middleware处理）

2. 待爬取项不能遗漏：单地址的失败重试、整体的遗漏重下

3. 并发爬取

4. 多种存储方式、排重

# 使用到的技术框架及包
1. Scrapy框架
2. requests：网络请求/高级网络请求
3. Beautiful Soup：返回的html解析
4. xlrd/xlwd/xlutils.copy：Excel的读、写、读转写
5. proxy_pool：IP代理池，链接：https://github.com/jhao104/proxy_pool
6. concurrent.futures：自带线程池

