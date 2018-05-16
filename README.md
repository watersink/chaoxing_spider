# chaoxing_spider
a spider used to crawl [chaoxing](http://book.chaoxing.com/) books in jpg format.

## functions:
- [x] only can crawl the first 17 pages of every book,because without full member
- [x] can crawl the book's contents and stored in txt format
- [x] the verification code is cnn,but the pics is few,so the rsult is not good

## dependencies:
urllib
> 
urllib.request
> 
BeautifulSoup
> 
selenium
> 
[phantomjs](http://phantomjs.org/)
> 
[chromedriver](http://chromedriver.storage.googleapis.com/index.html),should be placed C:\Program Files (x86)\Google\Chrome\Application
> 
[geckodriver](https://github.com/mozilla/geckodriver/releases/)

## original cnn multiple lables classification
    cd ./cnn
### train
    python3 train_cnn.py
![image]( https://github.com/watersink/chaoxing_spider/raw/master/img/Figure_1.png)
### test
    python3 eval_test_cnn.py

## crawl contents
    python3 chaoxing_contents.py
![image]( https://github.com/watersink/chaoxing_spider/raw/master/img/d1.png)
## crawl first 17 pics
    python3 chaoxing_17.py
![image]( https://github.com/watersink/chaoxing_spider/raw/master/img/d2.png)

## Note
only used for study,no commerical use

