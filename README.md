# Facebook 社群貼文爬取專案

此專案用於學習如何使用 **Python**、**Selenium** 和 **BeautifulSoup** 爬取 Facebook 社群中的貼文，目標是從社群中擷取貼文以進行數據分析與研究。

## 專案概述

此專案的主要目的是展示如何：
- 使用 Selenium 自動化瀏覽器登入 Facebook。
- 瀏覽 Facebook 社群並滾動加載貼文。
- 使用 BeautifulSoup 解析 HTML 並擷取相關的貼文數據。

### 功能
- **Selenium**：自動化瀏覽器以進行登入、滾動等操作。
- **BeautifulSoup**：解析 Facebook 貼文的 HTML 內容並擷取數據。

## 安裝

1. 克隆此倉庫：
```bash
git clone https://github.com/你的用戶名/facebook-scraping.git
cd facebook-scraping
```

2. 安裝所需的相依套件：
```bash
pip install -r requirements.txt
```
3. 確保已安裝對應版本的 Chrome 瀏覽器以及 ChromeDriver，並將 ChromeDriver 加入到你的 PATH 中。

## 使用方式
在程式碼中更新你的 Facebook 登入憑證（如果需要）。
執行腳本：
```bash
python fb.py
```

## 已知問題
- Facebook 限制：由於 Facebook 近期加強了防爬機制以及動態內容加載，該腳本目前無法正常運行。
- 登入及 CAPTCHA 驗證：Facebook 經常會觸發 CAPTCHA 驗證，Selenium 無法自動繞過這一點。
如果你在使用過程中遇到問題或有任何改善建議，歡迎在此倉庫中提出 issue。

## 貢獻方式
歡迎任何形式的貢獻！如果你發現問題或有改進建議，請按照以下步驟進行：
- Fork 此倉庫。
- 創建一個新的分支並進行修改。
- 提交 Pull Request。

