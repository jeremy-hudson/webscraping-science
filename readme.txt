1) Install scrapy:
    pip install scrapy
2) Run crawler with following command
    scrapy crawl articles_list -o output.csv -a keywords='radial,artery,occlusion'
where output.csv - output file, please note that extension is required (choices: 'json', 'jsonlines', 'jl', 'csv', 'xml', 'marshal', 'pickle')
also you can omit "-a keywords='radial,artery,occlusion'" part, default keywords are "radial", "artery", "occlusion". Keywords should be separated with comma, without spaces.
run it on same directory where scrapy.cfg placed.
3) Check results in output file