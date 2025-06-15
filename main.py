import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

# 配置参数
DESKTOP_SEARCH_TIMES = 30  # 桌面端搜索次数
MOBILE_SEARCH_TIMES = 20   # 移动端搜索次数
WAIT_TIME_MIN = 2          # 每次搜索后等待的最短时间（秒）
WAIT_TIME_MAX = 6          # 每次搜索后等待的最长时间（秒）

# 自定义日志过滤器
class IgnoreSpecificErrorsFilter(logging.Filter):
    def filter(self, record):
        # 忽略特定的 USB 错误日志
        usb_error_messages = [
            "SetupDiGetDeviceProperty",
            "Failed to read descriptors from",
            "Failed to read length for configuration",
            "Failed to read all configuration descriptors",
            "USB: usb_device_win.cc:95 Failed to read descriptors from"
        ]
        
        # 忽略特定的 SSL 错误日志
        ssl_error_messages = [
            "handshake failed; returned -1, SSL error code 1, net_error -101"
        ]
        
        # 忽略特定的 Renderer 任务提供者错误日志
        renderer_error_messages = [
            "Every renderer should have at least one task provided by a primary task provider. If a \"Renderer\" fallback task is shown, it is a bug."
        ]
        
        for message in (usb_error_messages + 
                      ssl_error_messages + 
                      renderer_error_messages):
            if message in record.getMessage():
                return False
        return True

# 初始化日志
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 清空日志文件
with open('search.log', 'w') as log_file:
    pass

file_handler = logging.FileHandler('search.log')
file_handler.setFormatter(log_formatter)
file_handler.addFilter(IgnoreSpecificErrorsFilter())
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.addFilter(IgnoreSpecificErrorsFilter())
logger.addHandler(console_handler)

KEYWORDS = [
    "2025年最佳编程语言", "Python 对比 JavaScript", "机器学习教程",
    "什么是云计算", "如何搭建网站", "C++ 智能指针", "Git 对比 SVN",
    "Docker 对比虚拟机", "REST 对比 GraphQL", "区块链如何工作", "MSFXP BLOG",
    "ChatGPT 工作原理", "OpenAI 最新消息", "人工智能的未来", "提高生产力的 AI 工具",
    "ChatGPT 编程辅助", "DALL·E 图像生成", "提示词工程技巧",
    "特斯拉股票新闻", "比特币价格预测", "如何投资 ETF", "今日股市新闻",
    "黄金是否是好的投资", "标普 500 指数含义", "加密货币税务规则",
    "健康早餐创意", "如何改善睡眠", "如何减轻压力", "咖啡是否健康",
    "喝水的好处", "最佳家庭锻炼", "间歇性禁食的好处",
    "权力的游戏回顾", "2025年最佳 Netflix 剧集", "搞笑猫咪视频", "漫威对比 DC",
    "2025年即将上映的电影", "奥斯卡最佳影片获奖名单", "2025年顶级 YouTuber", "Twitch 对比 Kick",
    "世界顶级大学", "最佳在线课程", "如何快速学习英语",
    "考试学习技巧", "GRE 考试介绍", "2025年是否需要 SAT 考试",
    "2025年最佳旅游目的地", "如何获取廉价机票", "最适合居住的十大城市",
    "东京天气", "附近的徒步旅行路线", "数字游民生活方式",
    "乌克兰冲突解释", "美国总统选举", "全球变暖事实",
    "气候变化解决方案", "最新科技新闻", "AI 取代工作", "智能手机的隐私问题",
    "如何创业", "在线赚钱方法", "被动收入创意", "顶级电商平台",
    "Dropshipping 对比亚马逊 FBA", "远程工作趋势", "自由职业对比全职工作",
    "2025年最佳 PC 游戏", "Valorant 技巧", "如何提高 Fortnite 水平",
    "Steam 夏季促销", "任天堂 Switch 2 传闻", "顶级电竞战队",
    "星座性格", "梦境含义", "趣味小知识", "关于太空的奇怪事实",
    "披萨上是否应该放菠萝", "yuexps", "ikaros",
    "伊卡洛斯", "yuexpsの主页", "MSFXP Search", "MSFXP服务器"
]

# 桌面端浏览器配置
def get_desktop_driver():
    """获取桌面端配置好的 WebDriver 实例"""
    service = Service(executable_path='./msedgedriver.exe')
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")  # 无痕模式
    options.add_argument("--disable-extensions")  # 禁用扩展
    options.add_argument("--disable-gpu")  # 禁用GPU加速
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    return webdriver.Edge(service=service, options=options)

# 移动端浏览器配置
def get_mobile_driver():
    """获取移动端配置好的 WebDriver 实例"""
    service = Service(executable_path='./msedgedriver.exe')
    options = webdriver.EdgeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")  # 无痕模式
    options.add_argument("--disable-extensions")  # 禁用扩展
    options.add_argument("--disable-gpu")  # 禁用GPU加速
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; Nexus 5X Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36")
    options.add_experimental_option("mobileEmulation", {
        "deviceName": "Nexus 5X"
    })
    return webdriver.Edge(service=service, options=options)

# 执行单次搜索
def perform_search(driver, keyword):
    """执行单次搜索操作"""
    try:
        time.sleep(1)  # 等待页面加载完成
        search_box = driver.find_element(By.NAME, "q")
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.submit()
        logger.info(f"搜索成功：{keyword}")
        return True
    except Exception as e:
        logger.error(f"搜索失败：{e}")
        return False

# 执行多轮搜索
def run_search(driver, times, is_mobile=False):
    """执行多轮搜索"""
    success_count = 0

    try:
        while success_count < times:
            driver.get("https://cn.bing.com")
            time.sleep(1)

            keyword = random.choice(KEYWORDS)
            logger.info(f"准备搜索：{keyword}")

            if perform_search(driver, keyword):
                success_count += 1

                if is_mobile:
                    print(f"移动端搜索进度：{success_count}/{times}", end='\r')
                else:
                    print(f"桌面端搜索进度：{success_count}/{times}", end='\r')

            time.sleep(random.uniform(WAIT_TIME_MIN, WAIT_TIME_MAX))

    finally:
        return success_count

# 主函数
def main():
    """主函数，负责执行所有搜索任务"""
    # 桌面端搜索
    desktop_driver = get_desktop_driver()
    desktop_driver.get("https://cn.bing.com")
    logger.info("桌面端浏览器已启动")

    desktop_success = run_search(desktop_driver, DESKTOP_SEARCH_TIMES)
    desktop_driver.quit()
    logger.info("桌面端浏览器已关闭")

    # 移动端搜索
    mobile_driver = get_mobile_driver()
    mobile_driver.get("https://cn.bing.com")
    logger.info("移动端浏览器已启动")

    mobile_success = run_search(mobile_driver, MOBILE_SEARCH_TIMES, is_mobile=True)
    mobile_driver.quit()
    logger.info("移动端浏览器已关闭")

    # 显示总结
    print(f"\n桌面端搜索总结：成功搜索 {desktop_success} 次")
    print(f"移动设备搜索总结：成功搜索 {mobile_success} 次")

if __name__ == "__main__":
    main()
