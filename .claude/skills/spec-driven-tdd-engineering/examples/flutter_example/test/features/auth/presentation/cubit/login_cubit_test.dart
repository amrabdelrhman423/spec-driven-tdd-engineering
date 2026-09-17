import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:flutter_auth_example/features/auth/domain/entities/user.dart';
import 'package:flutter_auth_example/features/auth/domain/repositories/auth_repository.dart';
import 'package:flutter_auth_example/features/auth/presentation/cubit/login_cubit.dart';
import 'package:flutter_auth_example/features/auth/presentation/cubit/login_state.dart';

class MockAuthRepository extends Mock implements AuthRepository {}

void main() {
  late LoginCubit loginCubit;
  late MockAuthRepository mockAuthRepository;

  setUp(() {
    mockAuthRepository = MockAuthRepository();
    loginCubit = LoginCubit(authRepository: mockAuthRepository);
  });

  tearDown(() {
    loginCubit.close();
  });

  const tUser = User(id: 'user_123', email: 'user@example.com');
  const tEmail = 'user@example.com';
  const tPassword = 'SecretPassword123!';

  group('LoginCubit TDD Test Suite', () {
    test('initial state should be LoginInitial', () {
      expect(loginCubit.state, equals(const LoginInitial()));
    });

    test(
      'Scenario 1: emits [LoginLoading, LoginSuccess] when login succeeds',
      () async {
        // Test Intent: Proves that valid credentials trigger Loading then Success
        when(() => mockAuthRepository.login(email: tEmail, password: tPassword))
            .thenAnswer((_) async => tUser);

        final expectedStates = [
          const LoginLoading(),
          const LoginSuccess(tUser),
        ];

        expectLater(loginCubit.stream, emitsInOrder(expectedStates));

        await loginCubit.login(email: tEmail, password: tPassword);

        verify(() => mockAuthRepository.login(email: tEmail, password: tPassword)).called(1);
      },
    );

    test(
      'Scenario 2: emits [LoginLoading, LoginFailure] when credentials are invalid',
      () async {
        // Test Intent: Proves failure handling produces clean error state
        when(() => mockAuthRepository.login(email: tEmail, password: tPassword))
            .thenThrow(Exception('Invalid credentials'));

        final expectedStates = [
          const LoginLoading(),
          const LoginFailure('Invalid credentials'),
        ];

        expectLater(loginCubit.stream, emitsInOrder(expectedStates));

        await loginCubit.login(email: tEmail, password: tPassword);
      },
    );

    test(
      'Invariant 3: fast-fails with LoginFailure when email format is invalid',
      () async {
        // Test Intent: Proves domain invariant without triggering repository
        await loginCubit.login(email: 'invalid-email', password: tPassword);

        expect(loginCubit.state, equals(const LoginFailure("Invalid email address format.")));
        verifyZeroInteractions(mockAuthRepository);
      },
    );
  });
}
