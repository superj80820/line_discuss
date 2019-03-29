# line_discuss

⭐有時候上課不太想抄筆記 大家是否都會直接拿起手機來照相呢

或者會議想投票 卻還要一個一個人頭慢慢數😭

本repo希望能藉由每個人幾乎都擁有的 **Line**

讓上課/報告/會議 溝通起來更方便

讓大家討論上更簡單(更懶❓ 

## 嘗試使用技術

SocketIo:

讓每個電腦client端雖然是client 但是可以被server主動推播訊息

Sqlite:

儲存上課/報告/會議 的使用者資料與討論資料

## 使用說明

![Imgur](https://i.imgur.com/PQw4KDY.png)

* Server端:

  運行方法

  ```
  python ./__init__.py
  ```

* Client端:

  運行方法

  ```
  python./form/clientGUI.py
  ```

  ---

  課程代碼

  line使用者可以依照課程代碼加入不同的課程

  ---

  小鍵盤功能

  * 發作業功能: 將client電腦目前畫面截圖傳送至server 並且藉由Server傳送給line使用者
  * 點名: client電腦對server發起點名請求 server再檢查所有line使用者是否已加入課程 並且顯示出來
  * 投票開始/投票結束: client電腦對server發起投票請求 server再對所有line使用者發起投票 client電腦一但按投票結束的按鈕 server會將目前投票的結果匯集起來必且回傳給client電腦 並且顯示出來
  * 討論: line使用者將圖片與問題傳送給server server會將圖片傳送給client電腦 當client電腦案討論鈕的時候就會顯示圖片與問題

  ---

  簡報繪圖功能 Pointofix:

  可以將client電腦桌面截圖 並且繪圖的 免費軟體 Pointofix

  (~~本來想自己寫一個的 結果 這個軟體太完整了 還是不要造輪子好了~~😜
