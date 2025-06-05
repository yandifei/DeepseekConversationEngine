"""contacts.py
用来管理通讯录的属性和方法
添加好友，好友遍历等方法
"""
import uiautomation
# 自带的库
from time import sleep
# 自己的库
from wcbo import WeChatBackgroundOperation  # 导入微信这个类


# 导包

class Contacts:
    def __init__(self, wechat_client : WeChatBackgroundOperation):
        """通讯录管理
        wechat_client : 微信对象
        """
        self.wc = wechat_client  # 接收微信这个对象调用里面最基础的方
        # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0(联系人列表,子控件就是人了)
        self.contacts_list_control : uiautomation.Control = None    # 好友列表控件

    def refresh_contacts_controls(self):
        """刷新通讯录控件"""
        # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0(联系人列表,子控件就是人了)
        # self.contacts_list_control = self.wc.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[1].GetChildren()[-1].GetFirstChildControl().GetFirstChildControl()
        self.contacts_list_control = self.wc.wc_win.GetLastChildControl().GetFirstChildControl().GetChildren()[1].GetLastChildControl().GetFirstChildControl().GetFirstChildControl()

    def find_same_remark_name(self, time = 2):
        """遍历好友列表找出备注名同名的好友(没有没注名就是原名)
        time ： 每次的滚动时间
        """
        self.wc.back_click(self.wc.contacts_button)  # 点击通讯录按钮
        self.refresh_contacts_controls()    # 刷新好友列表控件(之前在别的界面没拿到)
        # 拿到滚动区域的接口
        scroll_pattern = self.contacts_list_control.GetScrollPattern()  # (报黄不用管)
        scroll_pattern.SetScrollPercent(-1, 100)   # 列表移动到末尾(拿数据)
        # 倒数第一和第二个有重名
        if self.contacts_list_control.GetLastChildControl().Name == self.contacts_list_control.GetChildren()[-2].Name:
            print(f"\033[93m末尾出现重名：{self.wc.contacts_button.GetChildren()[-1].Name}\033[0m")
        end_flag = self.contacts_list_control.GetChildren()[-1].Name   # 设置结束标志
        scroll_pattern.SetScrollPercent(-1, 0)   # 列表移动到开头
        # 开始遍历逻辑
        remark_name_list = [name for name in self.contacts_list_control.GetChildren().Name]   # 备注名列表(初始化是带上旧表)
        while self.contacts_list_control.GetLastChildControl().Name != end_flag:  # 如果没有找到最后一个控件就不停止滚动
            old_list = [name for name in self.contacts_list_control.GetChildren().Name] # 遍历好友备注名
            self.wc.back_wheel(self.contacts_list_control, time)  # 滚动列表
            new_list = [name for name in self.contacts_list_control.GetChildren().Name] # 遍历滚动后的好友备注名
            link_index =  old_list[-1] # 拿到旧表最后一个值
            # 判断这个值在不在新表
            if link_index not in new_list:    # 旧表的最后一个元素不在新表代表滚动过头了(断链)
                raise ValueError("\033[93m滚动太快了，请缩短滚动时间(修该滚动参数)")
            new_index = new_list.index(old_list[-1]) + 1   # 拿到新内容开始的索引下标
            remark_name_list.append(new_name for new_name in new_list[new_index:])  # 切片拿到新名字
        print()




        print(1)


        scroll_percent = 0  # 滚动百分比，初始为0 代表开头
        # while scroll_percent <= 1:  # 小于等于 1 代表没有遍历完整个列表
        #     scroll_pattern.SetScrollPercent(-1, scroll_percent)
        #     scroll_percent += incremental_value / 100  # 每次增加的百分比


    def record_all_friends(self,path):
        """记录所有的好友
        path : 保存记录文件的路径
        """
        self.wc.back_click(self.wc.contacts_button) # 点击通讯录按钮
        # control.GetScrollPattern().SetScrollPercent(horizontal, vertical)


