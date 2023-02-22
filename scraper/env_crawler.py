from selenium.webdriver.chrome.options import Options

hiking_index_url = 'https://hiking.biji.co/index.php?q=trail&act=detail&id='
# 假的 headers 資訊
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"

driver_path = './chromedriver'

options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
# 加入 headers 資訊
options.add_argument('--user-agent=%s' % user_agent)

