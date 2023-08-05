# AI於釣魚郵件辨別之應用
### 參考資料
1. [機器學習分析垃圾&釣魚郵件標頭檔](https://github.com/kregg34/EmailHeaderAnomalyDetection/tree/797406a0bcf44a5d9840e72f3759061d1224f8de)
2. [Learning OpenAI API](https://youtu.be/9AXP7tCI9PI)
3. [OpenAI 專屬助理--網頁部分](https://youtu.be/jTNgTQLa528)
4. [ChatGPT Writer](https://chrome.google.com/webstore/detail/chatgpt-writer-write-mail/pdnenlnelpdomajfejgapbdpmjkfpjkp/related)

### (2)	專題背景與目的
- 尋找資料集
    - ❌[資料集是.raff（attribute-relation file format）檔](https://archive.ics.uci.edu/dataset/327/phishing+websites)
    - ❓[資料集是phishtank，現在不能註冊](https://github.com/zerofox-oss/phishpond)
    - ❓[Monkey.org(Mbox)資料集較舊，新的打不開](https://monkey.org/~jose/phishing/)
    - ⭕[OpenPhish：資料及即時更新:)](https://openphish.com/)
- 初步訓練
  - 輸入一則郵件，抓取裡面的 URL 當作爬蟲的基準點(可能有多個 url)，爬取 URL 裡面的HTML ，再利用剛剛寫的簡化 HTML 轉成 .txt 黨傳給我們的 chatGPT，阿T會讀取裡面的內容，分析是否為釣魚郵件。
- 經過訓練後
  - 直接給網站一個URL，他會顯示是 safe 或是 warning！並提供分數
  
### 一鍵搜索資料夾
- Confusion Matrix：計算與挑選模糊矩陣的樣本
- crawl：bug1只抓文字；bug2抓取整個html；craw以firefox引擎為模板
- de-identification：一鍵將儲存資料夾裡的html抓取文本。coool有 meta 值、html、url，有資料夾；lighter沒有 meta 值
- weeeb：如果 chatGPT 無法分析的備案，再傳入URL時將初步訓練的所有步驟全部在後台跑一次
- main：後端訓練
- gpt-master：串接與網站 Demo

### 遭遇問題與解方
- ![Alt text](image.png)
  一直沒辦法使用 chatGPT 的機器人，後來跟可以使用的組員比對後發現缺少了一個 persist 資料夾
