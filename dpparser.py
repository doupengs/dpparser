# coding: utf-8

import re
import datetime
from lxml import etree
from dplog.dplog import Logger

__version__ = '0.0.1'


class Parser(object):
    """
    :class: html parser
    """
    def __init__(self, data=None, response=None, url=None, encoding='utf-8'):
        """
        :param data: response.text
        :param response: response
        :param url: url
        :param encoding: response.encoding
        """
        try:
            self.data = data
            self.url = url
            if response is not None:
                if data is None:
                    response.encoding = encoding
                    self.data = response.text
                if url is None:
                    self.url = response.request.url
            self.__html = etree.HTML(self.data) if data else None
        except Exception as e:
            Logger.error(e)

    def xpathone(self, xpath):
        """
        :param xpath: xpath expression
        :function: xpath match one
        :return: class Parser
        """
        try:
            labels = self.__html.xpath(xpath)
        except Exception as e:
            Logger.error("%s [-] <xpath> %s <url> %s" % (e, xpath, self.url))
            return Parser(data='', url=self.url)
        if len(labels) > 0:
            label = labels[0]
            return Parser(
                data=etree.tostring(label, encoding="unicode", method="html"),
                url=self.url
            ) if isinstance(label, etree._Element) else Parser(data=label, url=self.url)
        else:
            Logger.warning("The parsing result is None [-] <xpath> %s <url> %s" % (xpath, self.url))
            return Parser(data='', url=self.url)

    def xpathall(self, xpath):
        """
        :param xpath: xpath expression
        :function: xpath match all
        :return: [class Parser, class Parser, ...]
        """
        try:
            labels = self.__html.xpath(xpath)
        except Exception as e:
            Logger.error("%s [-] <xpath> %s <url> %s" % (e, xpath, self.url))
            return []
        if len(labels) > 0:
            return [Parser(data=etree.tostring(label, encoding="unicode", method="html"), url=self.url)
                    if isinstance(label, etree._Element) else Parser(data=label, url=self.url) for label in labels]
        else:
            Logger.warning("The parsing result is None [-] <xpath> %s <url> %s" % (xpath, self.url))
            return []

    def reone(self, pattern):
        """
        :param pattern: regular expression
        :function: regular match one
        :return: class Parser
        """
        try:
            labels = re.findall(pattern, self.data)
        except Exception as e:
            Logger.error("%s [-] <pattern> %s <url> %s" % (e, pattern, self.url))
            return Parser(data='', url=self.url)
        if len(labels) > 0:
            return Parser(data=labels[0], url=self.url)
        else:
            Logger.warning("The parsing result is None [-] <pattern> %s <url> %s" % (pattern, self.url))
            return Parser(data='', url=self.url)

    def reall(self, pattern):
        """
        :param pattern: regular expression
        :function: regular match all
        :return: [class Parser, class Parser, ...]
        """
        try:
            labels = re.findall(pattern, self.data)
        except Exception as e:
            Logger.error("%s [-] <pattern> %s <url> %s" % (e, pattern, self.url))
            return []
        if len(labels) > 0:
            return [Parser(data=label, url=self.url) for label in labels]
        else:
            Logger.warning("The parsing result is None [-] <pattern> %s <url> %s" % (pattern, self.url))
            return []

    def resub(self, pattern, goalStr, count=0):
        """
        :param pattern: regular expression
        :param count: replace number
        :function: re.sub(pattern,goalStr)
        :return: class Parser
        """
        try:
            data = re.compile(pattern).sub(goalStr, self.data, count)
        except Exception as e:
            Logger.error("%s [-] <pattern> %s <url> %s" % (e, pattern, self.url))
            return self
        return Parser(data=data, url=self.url)

    def unicode(self):
        """
        :function: <class Parser> return <class unicode>
        :return: class unicode if Error u''
        """
        if self.__html is not None:
            return etree.tostring(self.__html, encoding="unicode", method='text')
        else:
            return u''

    def bytes(self, encoding='utf8'):
        """
        :param encoding: encoding
        :function: <class Parser> return <class bytes>
        :return: class bytes if Error b''
        """
        if self.__html is not None:
            return etree.tostring(self.__html, encoding=encoding, method='text')
        else:
            return u''.encode('utf8')

    def int(self):
        '''
        :function: <class Parser> return <class int>
        :return: class int if Error 0
        '''
        try:
            integer = int(self.data)
        except Exception as e:
            Logger.error(e)
            return 0
        return integer

    def float(self):
        """
        :function: <class Parser> return <class float>
        :return: class float if Error 0.0
        """
        try:
            f = float(self.data)
        except Exception as e:
            Logger.error(e)
            return 0.0
        return f

    def datetime(self, timeStrFormat="%Y-%m-%d %H:%M:%S", returnStrType=True):
        """
        :param timeStrFormat: time format
        :param returnStrType: bool
        :return: True -> return string time
                 False -> return datetime.datetime
                 current time if search failed
        """
        S = re.search(u"(\d+)\s*秒前", self.data)
        M = re.search(u"(\d+)\s*分钟前", self.data)
        H = re.search(u"(\d+)\s*小时前", self.data)
        D = re.search(u"(\d+)\s*天前", self.data)
        W = re.search(u"(\d+)\s*周前", self.data)
        JT = re.search(u'今天\s*(\d+:\d+:?\d*)', self.data)
        ZT = re.search(u'昨天\s*(\d+:\d+:?\d*)', self.data)
        QT = re.search(u'前天\s*(\d+:\d+:?\d*)', self.data)
        SZ = re.search(u'((\d+)[-/年](\d+)[-/月](\d+)日?\s*(\d*):?(\d*):?(\d*))', self.data)
        if S or M or H or D or W:
            seconds = int(S.group(1)) if S else 0
            minutes = int(M.group(1)) if M else 0
            hours = int(H.group(1)) if H else 0
            days = int(D.group(1)) if D else 0
            weeks = int(W.group(1)) if W else 0
            dtf = datetime.datetime.now() - datetime.timedelta(days, seconds, 0, 0, minutes, hours, weeks)
            strDt = dtf.strftime(timeStrFormat)
            dt = datetime.datetime.strptime(strDt, timeStrFormat)
        elif JT or ZT or QT:
            strTime = JT.group(1) if JT else ZT.group(1) if ZT else QT.group(1)
            startDay = 1 if JT else 2 if ZT else 3
            days = datetime.date.today() - datetime.date(1900, 1, startDay)
            try:
                dt = datetime.datetime.strptime(strTime, "%H:%M:%S") + days
            except:
                dt = datetime.datetime.strptime(strTime, "%H:%M") + days
            strDt = dt.strftime(timeStrFormat)
        elif SZ:
            year = SZ.group(2)
            mouth = SZ.group(3)
            day = SZ.group(4)
            hour = SZ.group(5) if SZ.group(5) else u'00'
            minute = SZ.group(6) if SZ.group(6) else u'00'
            second = SZ.group(7) if SZ.group(7) else u'00'
            if len(year) == 4:
                dt = datetime.datetime.strptime('%s%s%s%s%s%s' % (year, mouth, day, hour, minute, second),
                                                '%Y%m%d%H%M%S')
            elif len(year) == 2:
                dt = datetime.datetime.strptime('%s%s%s%s%s%s' % (year, mouth, day, hour, minute, second),
                                                '%y%m%d%H%M%S')
            else:
                Logger.error('Search The length of the year not 4 or 2')
                return None
            strDt = dt.strftime(timeStrFormat)
        else:
            dtf = datetime.datetime.now()
            strDt = dtf.strftime(timeStrFormat)
            dt = datetime.datetime.strptime(strDt, timeStrFormat)
            Logger.error('Search time format failed, return current time')
        if returnStrType:
            return strDt
        else:
            return dt
