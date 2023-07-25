from enum import Enum


class ErrorEnum(Enum):
    """
    定义错误 code 和 msg
    """
    PROJECT_NO_EXIST = "100001", "项目不存在"

    def __init__(self, code, msg):
        self._code = code
        self._msg = msg

    @property
    def msg(self):
        return self._msg

    @property
    def code(self):
        return self._code


if __name__ == '__main__':
    print(ErrorEnum.PROJECT_NO_EXIST.name)
    print(ErrorEnum.PROJECT_NO_EXIST.value)
    print(ErrorEnum.PROJECT_NO_EXIST.code)
    print(ErrorEnum.PROJECT_NO_EXIST.msg)

    print(type(ErrorEnum.PROJECT_NO_EXIST))