from src import dumps, register, JSONAbleABC, JSONSupportedTypes


class Test(JSONAbleABC):
    def __init__(self, content: str):
        self.content = content

    def __jsonable_encode__(self, obj: JSONAbleABC) -> JSONSupportedTypes:
        return

test = Test(content='test string')

print(dumps([1, 2, 3], ensure_ascii=False))
