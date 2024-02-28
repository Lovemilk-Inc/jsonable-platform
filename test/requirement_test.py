from jsonable_platform import register, JSONAbleABC, Self, JSONAbleABCEncodedType, loads, dumps


class RequirementC(JSONAbleABC):
    def __init__(self):
        self.content = 'Anything~'

    def __repr__(self):
        return f'RequirementC({self.content=})'

    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONAbleABCEncodedType:
        return obj.content

    @classmethod
    def __jsonable_decode__(cls, data: JSONAbleABCEncodedType) -> Self:
        self = cls()
        self.content = data
        return self


class RequirementB(JSONAbleABC):
    def __init__(self):
        self.content = 'Nothing~'
        self.datas = [RequirementC(), ]

    def __repr__(self):
        return f'RequirementB({self.content=}, {self.datas=})'

    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONAbleABCEncodedType:
        return [obj.content, obj.datas]

    @classmethod
    def __jsonable_decode__(cls, data: JSONAbleABCEncodedType) -> Self:
        self = cls()
        self.content = data[0]
        self.datas = data[1]
        return self


class RequirementA(JSONAbleABC):
    def __init__(self):
        self.information = [RequirementB(), RequirementC()]

    def __repr__(self):
        return f'RequirementA({self.information=})'

    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONAbleABCEncodedType:
        return obj.information

    @classmethod
    def __jsonable_decode__(cls, data: JSONAbleABCEncodedType) -> Self:
        self = cls()
        self.information = data
        return self


def test_requirement():
    RequirementA()
    register(RequirementA)

    try:
        loads(dumps({'test': RequirementA()}))
    except ValueError as e:
        assert e.args[0] == 'Cannot convert RequirementB to JSON'

    register(RequirementA, RequirementB, RequirementC)

    encoded = dumps({'test': RequirementA()})

    decoded = loads(encoded)

    assert isinstance(decoded['test'].information[0], RequirementB)
