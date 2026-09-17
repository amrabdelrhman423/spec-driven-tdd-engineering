# Implementation Tasks: User Authentication (Login)

**Spec Reference**: [`spec.md`](./spec.md)  
**Plan Reference**: [`plan.md`](./plan.md)  
**Risk Tier**: `MEDIUM`

---

## Phase 1: Domain Entities & Failure Contracts
- [x] **Task 1.1**: Define `User` domain entity with `Equatable`.
- [x] **Task 1.2**: Define `Failure` taxonomy (`AuthFailure`, `NetworkFailure`, `ServerFailure`).
- [x] **Task 1.3**: Define `AuthRepository` abstract interface.

---

## Phase 2: State Management & TDD Cycles
- [x] **Task 2.1**: Define `LoginState` (`Initial`, `Loading`, `Success`, `Failure`).
- [x] **Task 2.2**: Cubit TDD Cycle 1: Successful Login
  - [x] **Red**: Author failing test asserting `[LoginLoading, LoginSuccess]`.
  - [x] **Green**: Implement minimal `login()` calling repository and emitting states.
  - [x] **Refactor**: Clean variable naming.
- [x] **Task 2.3**: Cubit TDD Cycle 2: Failed Login
  - [x] **Red**: Author failing test asserting `[LoginLoading, LoginFailure]`.
  - [x] **Green**: Catch failure and emit `LoginFailure`.
  - [x] **Refactor**: Deduplicate error mapping.

---

## Phase 3: Dependency Injection
- [x] **Task 3.1**: Register `AuthRepository` and `LoginCubit` with GetIt service locator.
