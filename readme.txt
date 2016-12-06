Using Selenium + WebDriver in python to search for news about bitcoin. This will get the links and loop the results' pages. I used the page objects from https://github.com/dakotasmith/page-object-examples.

Steps to use:

1. From http://docs.seleniumhq.org/download/ Download, install and add to the path: 1) standalone server 2) browser drivers (Google Chrome Driver)
2. Run the server using `java -jar selenium-server-standalone-3.0.1.jar`
3. Run google-test.py

*Python 3.5 and PyCharm IDE.*

Links:
- https://www.youtube.com/watch?v=l15ZJAbxCL8
- https://github.com/dakotasmith/page-object-examples

Corpus:
- https://github.com/lmiguelmh/selenium-web-mining/blob/master/data/corpus/links/20161001.txt
- https://github.com/lmiguelmh/selenium-web-mining/blob/master/data/corpus/links_contents/20161001-149dea6ad97c8559-Monero%25E2%2580%2599s_Bubble_Pops%252C_Price_Plummets_As_Currency_Loses_Top_Five.txt
- https://github.com/lmiguelmh/selenium-web-mining/blob/master/data/corpus/links_contents_clean/20161001-149dea6ad97c8559-Monero%25E2%2580%2599s_Bubble_Pops%252C_Price_Plummets_As_Currency_Loses_Top_Five.txt

The sentiment analysis was done using Stanford's CoreNLP:
- http://corenlp.run/
- http://nlp.stanford.edu:8080/sentiment/rntnDemo.html
