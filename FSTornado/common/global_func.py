# coding=utf-8
import time
from datetime import datetime, timedelta, date
from database.tbl_account import TblAccount
PAGESIZE = 5
FIRST_PAGE = 1
TIME_FORMAT = "%Y-%m-%d"


def get_expires_datetime(self):
    expires_time = time.time() + self.settings.get('session_timeout', 600)
    expires_datetime = datetime.fromtimestamp(expires_time)
    return expires_datetime


def get_datetime(stime):
    dtime = datetime.strptime(stime, TIME_FORMAT)
    return dtime


def get_week_datetime(flag=0):
    """
    flag > 0, x week ago
    flag < 0, x week after
    :param flag:
    :return:
    """
    monday, sunday = date.today(), date.today()
    one_day = timedelta(days=1)
    print(one_day)
    if flag != 0:
        deta_value = flag * 7
        deta_day = timedelta(days=deta_value)
        monday -= deta_day
        sunday -= deta_day
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    # 返回当前的星期一和星期天的日期
    return monday, sunday


def get_pages(total_page):
    pages = total_page // PAGESIZE + 1
    return pages


def get_user_info(self):
    # current_user = self.current_user
    current_user = self.current_user.decode('gbk')
    # print(current_user)
    user = self.mysqldb().query(TblAccount.id, TblAccount.nickname).filter(
        TblAccount.loginname == current_user).first()
    return user


def get_user_id(self):
    user_id = self.mysqldb().query(TblAccount.id, TblAccount.nickname).filter(
        TblAccount.loginname == self.current_user).first()
    if user_id is None:
        uid = None
    else:
        uid = user_id.id
    return uid


def get_user_nickname(self):
    user = self.mysqldb().query(TblAccount.id, TblAccount.nickname).filter(
        TblAccount.loginname == self.current_user).first()
    if user is None:
        return None
    return user


if __name__ == "__main__":
    pass
    print(get_week_datetime(-1))