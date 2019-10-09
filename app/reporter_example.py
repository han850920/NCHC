#路徑請參照相對
# call Reporter 的 script 和app在同一層
from .utils import Reporter
# call Reporter 的 script 和app在上一層
# from app.utils import Reporter

if __name__=='__main__':
    # 宣告 Reporter 並指定報表排列位置 0=>小圖置下 ; 1=>小圖置右 
    # 讀取/tmp中最新的flag檔案 產生報表存在/tmp中 (不用另外傳data)
    # 若要改俵儲存位置 請改Reporter中的make_report 在最後return前的橻存路徑
    RP = Reporter(0)
    RP.make_report()
    print("hello")