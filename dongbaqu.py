import re
import datetime


class TimeUtil(object):
    @classmethod
    def parse_timezone(cls, timezone):
        """
        解析时区表示
        :param timezone: str eg: +8
        :return: dict{symbol, offset}
        """
        result = re.match(r'(?P<symbol>[+-])(?P<offset>\d+)', timezone)
        symbol = result.groupdict()['symbol']
        offset = int(result.groupdict()['offset'])

        return {
            'symbol': symbol,
            'offset': offset
        }

    @classmethod
    def convert_timezone(cls, dt, timezone="+0"):
        """默认是utc时间，需要"""
        result = cls.parse_timezone(timezone)
        symbol = result['symbol']

        offset = result['offset']

        if symbol == '+':
            return dt + datetime.timedelta(hours=offset)
        elif symbol == '-':
            return dt - datetime.timedelta(hours=offset)
        else:
            raise Exception('dont parse timezone format')


# if __name__ == '__main__':
#     utc_now = datetime.datetime.utcnow()
    
#     convert_now = TimeUtil.convert_timezone(utc_now, '+8')
#     convert_now = str(convert_now.year)[2:] + '/' + str(convert_now.month) + '/' + str(convert_now.day)
#     print("ret",convert_now)
