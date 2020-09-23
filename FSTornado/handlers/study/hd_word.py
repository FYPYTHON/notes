#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/20 11:40
# @Author  : 1823218990@qq.com
# @File    : tbl_word.py
# @Software: PyCharm

from handlers.basehd import BaseHandler, check_token
from tornado.log import app_log as weblog
from database.tbl_word import TblWord
import json

from handlers.show.hd_play import get_img_base64


class WordHandler(BaseHandler):
    @check_token
    def get(self):
        wid = self.get_argument("wid", None)
        if wid == "-1":
            return self.write(json.dumps({"error_code": 0, "words": self.get_all_word()}))
        else:
            word = self.get_one_word(wid)
            if word is None:
                return self.write(json.dumps({"error_code": 1, "word": word, "msg": u"word id不存在"}))
            return self.write(json.dumps({"error_code": 0, "word": word}))
        pass

    def get_all_word(self):
        words = self.mysqldb().query(TblWord.id, TblWord.word, TblWord.chn).order_by(TblWord.word).all()
        datas = list()
        for word in words:
            datas.append([word.id, word.word, word.chn])

        return datas

    def get_one_word(self, wid):
        word = self.mysqldb().query(TblWord).filter(TblWord.id == wid).first()
        if word is None:
            return None
        else:
            return word.tojson

    @check_token
    def post(self):
        word = self.get_argument("word", None)
        chn = self.get_argument("chn", None)
        picture = self.get_argument("picture", None)
        describe = self.get_argument("describe", None)

        tblword = TblWord()
        tblword.word = word
        tblword.chn = chn
        base64Picture = get_img_base64(picture, "jpg")
        tblword.picture = base64Picture
        tblword.describe = describe

        self.mysqldb().add(tblword)

        try:
            self.mysqldb().commit()
            return self.write(json.dumps({"error_code": 0, "msg": ""}))
        except Exception as e:
            weblog.error("{}".format(e))
            return self.write(json.dumps({"error_code": 1, "msg": u"添加失败"}))

    @check_token
    def delete(self):
        wid = self.get_argument("wid")

        tblword = self.mysqldb().query(TblWord).filter(TblWord.id == wid).first()

        if tblword is None:
            self.mysqldb().commit()
            return self.write(json.dumps({"error_code": 1, "msg": u"word不存在，无法删除"}))
        else:
            self.mysqldb().query(TblWord).filter(TblWord.id == wid).delete()
            try:
                self.mysqldb().commit()
                return self.write(json.dumps({"error_code": 0, "msg": ""}))
            except Exception as e:
                weblog.error("{}".format(e))
                return self.write(json.dumps({"error_code": 1, "msg": u"删除失败"}))
