import base64, hmac, json, time
import copy


# 自定义类，提供jwt的加密和接密接口
class Jwt:
    def __init__(self):
        pass

    @staticmethod
    def encode(payload, key, exp=60 * 60 * 12):
        # 创建header
        header = {"alg": "HS256", "typ": "JWT"}
        # separators参数：生成紧凑型的json字符串(原字典中如果有空格的话，转成json后默认是会保留的)
        # 指明json字符串中 每个键值对 以及 key和value之间 用什么相连
        # sort_key：json字符串按key排序输出，保证每次转换之后得到相同的字符串(因为字典是无序的)
        header_j = json.dumps(header, separators=(',', ':'), sort_keys=True)
        # 使用自定义的b64encode方法进行加密
        header_bs = Jwt.b64encode(header_j.encode())

        # 创建payload
        payload = copy.deepcopy(payload)
        # 设置过期时间标记
        payload['exp'] = int(time.time()) + exp
        payload_j = json.dumps(payload, separators=(',', ':'), sort_keys=True)
        # 使用python提供的base64方法加密
        payload_bs = base64.urlsafe_b64encode(payload_j.encode())

        # 生成sign 预签名串
        to_sign_str = header_bs + b'.' + payload_bs
        if isinstance(key, str):
            key = key.encode()
        # 创建加密对象，hamc new 中的参数需要用bytes格式
        hmac_obj = hmac.new(key, to_sign_str, digestmod='SHA256')
        # 获得签名的摘要(结果)
        sign = hmac_obj.digest()
        sign_bs = Jwt.b64encode(sign)

        return header_bs + b'.' + payload_bs + b'.' + sign_bs

    # jwt解密方法，返回payload
    @staticmethod
    def decode(token, key):
        '''
        校验token
        :param token:
        :param key:
        :return:
        '''
        header_bs, payload_bs, sign = token.split(b'.')

        if isinstance(key, str):
            key = key.encode()
        # 重新计算签名
        hmac_obj = hmac.new(key, header_bs + b'.' + payload_bs, digestmod='SHA256')
        new_sign = Jwt.b64encode(hmac_obj.digest())
        if sign != new_sign:
            # 当前传过来的token违法，raise异常，由外部进行捕获
            raise JwtError('token不合法')
        # token验证合法，判断是否过期
        # 将base64的payload解码为json串，这里得到的是bytes格式
        payload_j = Jwt.b64decode(payload_bs)
        payload = json.loads(payload_j)
        # 拿到过期时间
        exp = payload['exp']
        now = time.time()
        # 对比是否过期
        if now > exp:
            raise JwtError('token 失效')
        return payload

    @staticmethod
    def b64encode(s):
        # 原生base64编码：每3个字符进行编码，最终可能出现等号，此处将等号替换掉，解码时也要做对应的处理
        return base64.urlsafe_b64encode(s).replace(b'=', b'')

    @staticmethod
    def b64decode(bs):
        # 将编码时=替换为''的进行恢复，补足长度
        rem = len(bs) % 4
        bs += b'=' * (4 - rem)
        return base64.urlsafe_b64decode(bs)


# 自定义jwt异常类
class JwtError(Exception):
    def __init__(self, error_msg):
        self.error = error_msg

    def __str__(self):
        return '<JwtError error %s>' % self.error


if __name__ == '__main__':
    res = Jwt.encode({'username': 'kzzf'}, 'abcd1234')
    # res = b'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzY3MjM4MDMsInVzZXJuYW1lIjoia3p6ZiJ9._pYMylwFW1GSeJi3ltpA3_3EWFNJ2fmMrXwFekKMljI'
    print(res)
    print(Jwt.decode(res, 'abcd1234'))
