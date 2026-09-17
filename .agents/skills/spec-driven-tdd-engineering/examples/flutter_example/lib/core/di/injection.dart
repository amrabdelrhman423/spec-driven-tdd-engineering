import 'package:get_it/get_it.dart';
import '../../features/auth/domain/repositories/auth_repository.dart';
import '../../features/auth/presentation/cubit/login_cubit.dart';

final getIt = GetIt.instance;

void configureDependencies({AuthRepository? authRepositoryOverride}) {
  if (authRepositoryOverride != null) {
    getIt.registerSingleton<AuthRepository>(authRepositoryOverride);
  }

  getIt.registerFactory<LoginCubit>(
    () => LoginCubit(authRepository: getIt<AuthRepository>()),
  );
}
