1. 把从 eastmoney 下载的各国指数数据保存到本地 json，如 .\input\america\巴西_BVSP_UI.json（虽然他是 js 对象，直接从网页上保存下来即可）
2. 通过 combine 函数，把所有指数数据整合到一个 txt 文件，如 .\output\db.txt
3. 通过 mariaDB 接口把数据录入阿里云服务器中，finance 数据库中的 year_klines 表。