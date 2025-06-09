"""contacts.py
用来管理通讯录的属性和方法
添加好友，好友遍历等方法
"""
# 系统自带库
from time import sleep
# 第三方库
import uiautomation
# 自己的库
from wcbo import WeChatBackgroundOperation  # 导入微信这个类

class Contacts:
    def __init__(self, wechat_client : WeChatBackgroundOperation):
        """通讯录管理
        wechat_client : 微信对象
        """
        self.wc = wechat_client  # 接收微信这个对象调用里面最基础的方
        # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0(联系人列表,子控件就是人了)
        self.contacts_list_control : uiautomation.ListControl = None    # 好友列表控件

    def click(self):
        """点击和获得(刷新)通讯录控件"""
        # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0(联系人列表,子控件就是人了)
        # self.contacts_list_control = self.wc.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[1].GetChildren()[-1].GetFirstChildControl().GetFirstChildControl()
        self.wc.back_click(self.wc.contacts_button)  # 点击通讯录按钮
        self.contacts_list_control = self.wc.wc_win.GetLastChildControl().GetFirstChildControl().GetChildren()[1].GetLastChildControl().GetFirstChildControl().GetFirstChildControl()

    def find_same_remark_name(self,sleep_time = 0.02, out = False):
        """遍历好友列表找出备注名同名的好友(没有没注名就是原名)
        参数：
        sleep_time : 按键的间隔时间(必须设置，不然滚动太快导致无法到达第一个好友处)
        out : 是否输出提示
        返回值：
        如果没用同名返回False, 如果有同名返回字典{同名的名字: 有多少个同名的数量}
        """
        if sleep_time < 0.02:   # 速度太快
            raise ValueError("速度太快了，建议0.02及以上，不然好友读取可能有遗漏")
        count_name_dict = dict()  # 创建字典统计好友名的次数

        self.click()    # 刷新好友列表控件(之前在别的界面没拿到)
        # 拿到滚动区域的接口
        scroll_pattern = self.contacts_list_control.GetScrollPattern()  # (报黄不用管)

        # 开始遍历逻辑
        scroll_pattern.SetScrollPercent(-1, 0)  # 列表移动到开头
        self.wc.back_click(self.contacts_list_control.GetChildren()[2])  # 后台点击第三个控件(新朋友控件，为了能后台键盘)
        self.wc.back_key(self.contacts_list_control.GetFirstChildControl(),35) # 列表移动到结尾拿结束标志
        sleep(1)  # 停顿，等待渲染加载
        # scroll_pattern.SetScrollPercent(-1, 1)   # 列表移动到结尾拿结束标志
        # 判断倒数第一和第二个是否有重名(如果末尾同名就不会遍历到最后一个控件)
        if self.contacts_list_control.GetLastChildControl().Name == self.contacts_list_control.GetChildren()[-2].Name:
            if out: print(f"\033[93m末尾出现重名：{self.wc.contacts_button.GetLastChildControl().Name}\033[0m")
            count_name_dict[self.wc.contacts_button.GetLastChildControl().Name] = count_name_dict.get(self.wc.contacts_button.GetLastChildControl().Name, 0) + 1
        end_flag = self.contacts_list_control.GetLastChildControl().Name   # 设置结束标志
        # print(f"退出标志(最后一个好友):{end_flag}，间隔:{sleep_time}")
        scroll_pattern.SetScrollPercent(-1, 0)   # 列表移动到开头
        # self.wc.back_key(self.contacts_list_control.GetFirstChildControl(),36) # 滚到开头# 列表移动到开头
        self.wc.back_click(self.contacts_list_control.GetChildren()[2]) # 后台点击第三个控件(新朋友控件，为了键盘的下移)

        # 星标朋友遍历（在星标的好友不会被录入下面的好友列表A-Z）
        # print("开始遍历星标朋友")
        # 判断是否有星标朋友
        if self.contacts_list_control.GetChildren()[3].GetFirstChildControl().GetFirstChildControl().Name == "星标朋友":
            self.wc.back_key(self.contacts_list_control, 40)  # 按下键，如果没有星标好友就是公众号（必须按键，后台点击无法获得选中属性）
            while True: # 不断循环，等待退出条件
                for control in self.contacts_list_control.GetChildren():  # 遍历选中的控件
                    if control.GetLegacyIAccessiblePattern().State > 3000000:  # 选中状态
                        # 如果到达公众号控件就停止遍历(名字是公众号，子孩子的子孩子也是公众号)
                        if control.Name == "公众号" and control.GetFirstChildControl().GetFirstChildControl().Name == "ContactListItem":
                            break  # 退出for
                        count_name_dict[control.Name] = count_name_dict.get(control.Name, 0) + 1
                        if out: print(control.Name)  # 打印名字
                else:
                    self.wc.back_key(self.contacts_list_control, 40)  # 按下键
                    sleep(sleep_time)  # 停顿，等待渲染加载
                    continue    # 跳过下面的break
                break

        sleep(1)   # 停顿，等待渲染加载
        # sleep(sleep_time)  # 停顿，等待渲染加载

        # 遍历非星标好友
        # print("开始遍历非星标好友")
        # print(f"下标：{len(self.contacts_list_control.GetChildren()) - 1}")
        # 到第一个非星标好友控件（2种情况，1：A已经在了，不需要翻页了。2：需要翻页）
        scroll_pattern.SetScrollPercent(-1, 0)  # 列表移动到开头
        self.wc.back_click(self.contacts_list_control.GetChildren()[2])  # 后台点击第三个控件(新朋友控件，为了能后台键盘)
        no_A_flag = True    # 当前界面没有A的标志位
        # 检测当前界面是否有A
        for control in self.contacts_list_control.GetChildren():  # 获得好友控件列表
            if control.Name == "" and control.GetFirstChildControl().GetFirstChildControl().Name == "A":  # 当前界面有A
                no_A_flag = False   # 设置A的标志位存在，避免下面继续遍历A
                # print("A存在当前界面")

        # 当前界面有A
        if not no_A_flag:   # 滚动到第1个好友控件
            while True:
                for index, control in enumerate(self.contacts_list_control.GetChildren()):  # 获得控件列表和下标
                    if control.GetLegacyIAccessiblePattern().State > 3000000:  # 选中状态且上一个控件是A(一定能拿到上一个控件，因为有A)
                        if self.contacts_list_control.GetChildren()[index - 1].GetFirstChildControl().GetFirstChildControl().Name == "A":    # A控件
                            break   # 到达好友控件了，退出for
                else:
                    self.wc.back_key(self.contacts_list_control, 40)  # 按下键
                    sleep(sleep_time)  # 停顿，等待渲染加载
                    continue
                break   # 退出while

        # A不存在当前界面
        if no_A_flag:
            # print("A不存在当前界面")
            # 一直滚动，直到当前列表控件最后是A(最后一个控件是因为要翻页)
            # 注意：这里不需要怕这个控件是最后一个控件，因为下移后会预留一个控件
            while self.contacts_list_control.GetLastChildControl().GetFirstChildControl().GetFirstChildControl().Name != "A":
                self.wc.back_key(self.contacts_list_control, 40)  # 按下键
                sleep(0.1)  # 停顿，等待渲染加载
            # 移动到第一个好友控件
            self.wc.back_key(self.contacts_list_control, 40)  # 按下键
            sleep(sleep_time)  # 停顿，等待渲染加载

        sleep(1)  # 停顿，等待渲染加载
        # print("到达A处")
        # sleep(sleep_time)  # 停顿，等待渲染加载

        # 开始遍历好友控件
        while True:  # 如果没有找到最后一个控件就不停止滚动
            for control in self.contacts_list_control.GetChildren():
                if control.GetLegacyIAccessiblePattern().State > 3000000:  # 选中状态
                    count_name_dict[control.Name] = count_name_dict.get(control.Name, 0) + 1
                    if out: print(control.Name) # 打印名字
                    if control.Name == end_flag:   # 到达退出标志(录入最后一个再退)
                        break   # 退出for循环
            else:
                self.wc.back_key(self.contacts_list_control, 40)  # 按下键
                sleep(sleep_time)  # 停顿，等待渲染加载
                continue
            break   # 提出while循环

        # 还原现场（滚回开头）
        scroll_pattern.SetScrollPercent(-1, 0)  # 列表移动到开头
        self.wc.back_click(self.contacts_list_control.GetChildren()[2])  # 后台点击第三个控件(新朋友控件，为了能后台键盘)


        # 筛选重复次数键值
        duplicate_dict = {k: v for k, v in count_name_dict.items() if v >= 2}
        if out:
            if duplicate_dict:
                print(f"重名名字和重名人数\n{'\n'.join(f'{name}：{count}' for name, count in duplicate_dict.items())}")
            else:
                print("无重名好友，不会产生控件歧义")
            num = 0
            for name, count in count_name_dict.items():
                num += count
            print(f"共有：{num} 好友")
        return duplicate_dict



    def record_all_friends(self,path):
        """记录所有的好友
        path : 保存记录文件的路径
        """
        self.wc.back_click(self.wc.contacts_button) # 点击通讯录按钮
        # control.GetScrollPattern().SetScrollPercent(horizontal, vertical)


