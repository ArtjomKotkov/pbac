# Pbac

### Basic example

Python abac class-based realization.

```python
from typing import Optional

from pydantic import BaseModel

from pbac import (
    Group, Policy, Rule,
    Algorithm, Effect,
    Action, Subject, Target,
    Context, Actions
)


class TestModel(BaseModel):
    test: str


class UserTest(BaseModel):
    id: str
    role: str
    test: Optional[str]


test_tree = Group(
    _id='access_by_roles',
    description='Доступ к функциям системы по ролям',
    algorithm=Algorithm.DENY_UNLESS_PERMIT,
    items=[
        Policy(
            _id='admin_access',
            description='Админу разрешено все',
            algorithm=Algorithm.PERMIT_UNLESS_DENY,
            actors=Subject == UserTest,
            condition=Subject.role == 'admin'
        ),
        Policy(
            _id='simple_user',
            description='Права доступа обычным юзерам',
            algorithm=Algorithm.DENY_UNLESS_PERMIT,
            actors=Subject == UserTest,
            condition=(Subject.role == 'simple') & (Action == 'read'),
            rules=[
                Rule(
                    _id='test_rule',
                    description='тестовое правило',
                    effect=Effect.PERMIT,
                    actors=Target == TestModel,
                    condition=Subject.some_attr == 'value' and Context.some_context == 'some_value'
                )
            ]
        ),
    ],
)

user_simple = UserTest(id='1', role='simple', some_attr='value')
user_admin = UserTest(id='2', role='admin')
user_random = UserTest(id='3', role='random', )
test_model = TestModel(test='test')


# random subject
print(test_tree.execute(subject=user_random, target=test_model, action=Actions.READ, context={})) # Effect.DENY

# admin subject
print(test_tree.execute(subject=user_admin, target=test_model, action=Actions.READ, context={})) # Effect.PERMIT

# simple subject no context
print(test_tree.execute(subject=user_simple, target=test_model, action=Actions.READ, context={})) # Effect.DENY

# simple subject no context
print(test_tree.execute(subject=user_simple, target=test_model, action=Actions.READ, context={'some_context': 'some_value'})) # Effect.PERMIT
```

### Information

Only 4 types of Entities are supported.

* Subject
* Target
* Context
* Action

You can perform simple comparison operations with them.
```python
result = Subject.arg == 12 and Target.arg == 'some_arg'
# or
result = Subject.same_arg == Target.same_arg
```

Its allowed to get sub arg from provided entity, like:
```python
result = Subject.some_object.arg == 10
```

You can use string representation of algrorithm, action and effect.
```python

print(Algorithm.PERMIT_UNLESS_DENY == 'permit_unless_deny')  # True
print(Action.READ == 'read')  # True
print(Effect.DENY == 'deny')  # True
```

Also you can provide dicts, classes and mixed construction as entities.
```python
from pydantic import BaseModel

# Class based entity
class ClassBasedEntity(BaseModel):
    attr: str
    
entity = ClassBasedEntity(attr='value')

# Object based Entity
entity = {
    'attr': 'value'
}
    
# Mixed Entity.
entity = {
    'attr': ClassBasedEntity(attr='value')
}
```