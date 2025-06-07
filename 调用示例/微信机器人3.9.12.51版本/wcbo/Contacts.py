"""contacts.py
用来管理通讯录的属性和方法
添加好友，好友遍历等方法
"""
# 系统自带库
from time import sleep
# 第三方库
import uiautomation
import win32con
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
        self.contacts_list_control : uiautomation.ListControl = None    # 好友列表控件

    def get_contacts_controls(self):
        """获得(刷新)通讯录控件"""
        # 微信-最后控件-控件0-控件1-最后控件-控件0-控件0(联系人列表,子控件就是人了)
        # self.contacts_list_control = self.wc.wc_win.GetChildren()[-1].GetChildren()[0].GetChildren()[1].GetChildren()[-1].GetFirstChildControl().GetFirstChildControl()
        self.contacts_list_control = self.wc.wc_win.GetLastChildControl().GetFirstChildControl().GetChildren()[1].GetLastChildControl().GetFirstChildControl().GetFirstChildControl()

    def is_same_remark_name(self, out = False):
        """遍历好友列表找出备注名同名的好友(没有没注名就是原名)
        参数：
        sleep_time : 按键的间隔时间(必须设置，不然滚动太快导致无法到达第一个好友处)
        out : 是否输出提示
        返回值：
        如果没用同名返回False, 如果有同名返回字典{同名的名字: 有多少个同名的数量}
        """
        # if sleep_time < 0.01:   # 速度太快
        #     raise ValueError("速度太快了，建议0.01及以上，不然无法到达初始位置")
        count_name_dict = dict()  # 创建字典统计好友名的次数
        self.wc.back_click(self.wc.contacts_button)  # 点击通讯录按钮
        self.get_contacts_controls()    # 刷新好友列表控件(之前在别的界面没拿到)
        # 拿到滚动区域的接口
        scroll_pattern = self.contacts_list_control.GetScrollPattern()  # (报黄不用管)

        # 开始遍历逻辑
        scroll_pattern.SetScrollPercent(-1, 1)   # 列表移动到结尾拿结束标志
        # 判断倒数第一和第二个是否有重名(如果末尾同名就不会遍历到最后一个控件)
        if self.contacts_list_control.GetLastChildControl().Name == self.contacts_list_control.GetChildren()[-2].Name:
            if out: print(f"\033[93m末尾出现重名：{self.wc.contacts_button.GetChildren()[-1].Name}\033[0m")
            count_name_dict[self.wc.contacts_button.GetChildren()[-1].Name] = count_name_dict.get(self.wc.contacts_button.GetChildren()[-1].Name, 0) + 1
        end_flag = self.contacts_list_control.GetChildren()[-1].Name   # 设置结束标志
        scroll_pattern.SetScrollPercent(-1, 0)   # 列表移动到开头
        self.wc.back_click(self.contacts_list_control.GetChildren()[2]) # 后台点击第三个控件(新朋友控件，为了键盘的下移)

        # 星标遍历（在星标的好友不会被录入下面的好友列表A-Z）
        # 判断是否有星标朋友
        if self.contacts_list_control.GetChildren()[3].GetFirstChildControl().GetFirstChildControl().Name == "星标朋友":
            self.wc.back_key(self.contacts_list_control, 40)  # 按下键，如果没有星标好友就是公众号（必须按键，后台点击无法获得选中属性）
            while True: # 不断循环，等待退出条件
                for control in self.contacts_list_control.GetChildren():  # 遍历选中的控件
                    if control.GetLegacyIAccessiblePattern().State == 3145734:  # 选中状态
                        # 如果到达公众号控件就停止遍历(名字是公众号，子孩子的子孩子也是公众号)
                        if control.Name == "公众号" and control.GetFirstChildControl().GetFirstChildControl().Name == "ContactListItem":
                            break  # 退出for
                        count_name_dict[control.Name] = count_name_dict.get(control.Name, 0) + 1
                        if out: print(control.Name)  # 打印名字
                else:
                    self.wc.back_key(self.contacts_list_control, 40)  # 按下键
                    continue    # 跳过下面的break
                break
            # print("遍历完了星标朋友")

        # 遍历非星标好友
        while True:
            for index in range(len(self.contacts_list_control.GetChildren()) - 1): # 获得好友控件列表
                # 判断当前列表是否存在此控件
                if self.contacts_list_control.GetChildren()[index].GetLegacyIAccessiblePattern().State == 3145734:  # 选中状态
                    if self.contacts_list_control.GetChildren()[index - 1].Name == "":
                        print(self.contacts_list_control.GetChildren()[index-1].GetFirstChildControl().GetFirstChildControl().Name)
                    # 判断上一个控件是不是A(双条件直接给我出bug了，判读""和A，空直接给我bug找不到A)
                    if self.contacts_list_control.GetChildren()[index-1].GetFirstChildControl().GetFirstChildControl().Name == "A":
                        break   # 跳出for循环
            else:
                self.wc.back_key(self.contacts_list_control, 40)  # 按下键
                continue  # 跳过下面的break
            break   # 跳出继续往下


        # 下标先定位到好友的开始部分(A字母位置)
        # while self.contacts_list_control.GetFirstChildControl().GetFirstChildControl().GetFirstChildControl().Name != "A":
        #     self.wc.back_key(self.contacts_list_control, 40)        # 按下键
        #     sleep(sleep_time)
        # self.wc.back_key(self.contacts_list_control, 40)  # 第一个好友位置
        # if out: print("已移动到A位置，下个控件即为第一个好友控件")
        while self.contacts_list_control.GetLastChildControl().Name != end_flag:  # 如果没有找到最后一个控件就不停止滚动
            for control in self.contacts_list_control.GetChildren():
                if control.GetLegacyIAccessiblePattern().State == 3145734:  # 选中状态
                    count_name_dict[control.Name] = count_name_dict.get(control.Name, 0) + 1
                    if out: print(control.Name) # 打印名字
            self.wc.back_key(self.contacts_list_control, 40)  # 按下键


        # 筛选重复次数键值
        duplicate_dict = {k: v for k, v in count_name_dict.items() if v > 1}
        if out:
            if duplicate_dict:
                print(f"重名名字\t\t重名人数\n{'\n'.join(f'{name}\t{count}' for name, count in duplicate_dict.items())}")
            else:
                print("无重名好友，不会产生控件歧义")
            print()
        return duplicate_dict









    def record_all_friends(self,path):
        """记录所有的好友
        path : 保存记录文件的路径
        """
        self.wc.back_click(self.wc.contacts_button) # 点击通讯录按钮
        # control.GetScrollPattern().SetScrollPercent(horizontal, vertical)


