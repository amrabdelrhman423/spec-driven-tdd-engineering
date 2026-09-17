import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/repositories/auth_repository.dart';
import 'login_state.dart';

class LoginCubit extends Cubit<LoginState> {
  final AuthRepository authRepository;

  LoginCubit({required this.authRepository}) : super(const LoginInitial());

  Future<void> login({required String email, required String password}) async {
    // Invariant 2: Ignore duplicate submissions when already loading
    if (state is LoginLoading) return;

    // Invariant 3: Fast-fail validation
    if (!email.contains('@') || email.length < 5) {
      emit(const LoginFailure("Invalid email address format."));
      return;
    }

    emit(const LoginLoading());

    try {
      final user = await authRepository.login(email: email, password: password);
      emit(LoginSuccess(user));
    } catch (e) {
      emit(LoginFailure(e.toString().replaceAll('Exception: ', '')));
    }
  }
}
