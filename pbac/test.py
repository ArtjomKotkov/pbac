from typing import Optional

from pydantic import BaseModel

from tree import Group, Policy, Rule
from const import Algorithm, Effect
from entity import Entity
from action import Action
from actor import Subject, Target
from const import Actions
from request import PBacRequest


class TestModel(BaseModel):
    test: str


class UserTest(BaseModel):
    id: str
    role: str
    test: Optional[str]


TestModel_ = Entity(TestModel)
UserTest_ = Entity(UserTest)


TEST_TREE = Group(
    _id='access_by_roles',
    description='Доступ к функциям системы по ролям',
    algorithm=Algorithm.DENY_UNLESS_PERMIT,
    items=[
        Policy(
            _id='admin_access',
            description='Админу разрешено все',
            algorithm=Algorithm.PERMIT_UNLESS_DENY,
            actors=Subject == UserTest_,
            condition=UserTest_.role == 'admin'
        ),
        Policy(
            _id='simple_user',
            description='Права доступа обычным юзерам',
            algorithm=Algorithm.DENY_UNLESS_PERMIT,
            actors=Subject == UserTest_,
            condition=(UserTest_.role == 'simple') & (Action == Actions.READ),
            rules=[
                Rule(
                    _id='test_rule',
                    description='тестовое правило',
                    effect=Effect.PERMIT,
                    actors=Target == TestModel_,
                    condition=UserTest_.test == '10'
                )
            ]
        ),
    ],
)


a = Entity(UserTest)
b = Entity(TestModel)

user_simple = UserTest(id='agsdgdsgsdg23r523', role='simple', test='10')
user_admin = UserTest(id='gsadgsadg', role='admin')
user_random = UserTest(id='gsadgsadg', role='asdgsdagdsg',)
test_model = TestModel(test='asdgsadgsadgsadg')


request = PBacRequest(
    action=Actions.READ,
    subject=user_random,
    target=test_model,
)

print(TEST_TREE.execute(request))