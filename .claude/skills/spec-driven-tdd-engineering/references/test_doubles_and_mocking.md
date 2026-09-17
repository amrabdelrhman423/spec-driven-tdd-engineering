# Test Doubles & Mocking Best Practices

## 1. The Pyramid of Test Doubles

When testing code that interacts with external resources (APIs, databases, file systems), use test doubles according to the principle of least complexity:

1. **State Verification over Interaction Verification**:
   - Prefer checking output results and system state rather than asserting that method `x()` was called exactly 2 times with specific arguments.
   - Interaction testing creates tight coupling to implementation details.

2. **When to use Fakes**:
   - Whenever feasible, use an in-memory fake repository or fake client.
   - Fakes implement the exact same interface as production dependencies but operate synchronously in memory.

```python
# Good: In-memory fake repository
class FakeUserRepository:
    def __init__(self):
        self.users = {}

    def save(self, user):
        self.users[user.id] = user

    def find_by_id(self, user_id):
        return self.users.get(user_id)
```

---

## 2. Anti-Patterns to Avoid

- **Mocking the Unit Under Test**: Never mock the class or function you are actually testing.
- **Mocking Pure Data / Value Objects**: Never mock strings, dicts, or data structures. Pass real instances.
- **Over-mocking**: If a test requires more than 3 mocks, the component is doing too much and violates the Single Responsibility Principle (SRP).
- **Ignoring Failures**: Never write tests with empty `except` blocks or assertions like `assert True`.
