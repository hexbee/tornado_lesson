# coding:utf-8
def sub(a, b):
    return a-b


def upper(a):
    return str(a).upper()


class Count:
    @classmethod
    def sum(cls, a, b):
        return a+b
    @property
    def url(self):
        return '<a href="http://www.baidu.com">百度</a>'

    def args(self, *args):
        return [str(a)+'---hello' for a in args]
