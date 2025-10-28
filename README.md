DriveFlow (Sistema de Alquiler de Autos)Este es un proyecto de sistema de escritorio para la gestión de alquiler de vehículos, desarrollado en Python con Tkinter.Este repositorio representa la refactorización completa de un proyecto monolítico anterior, aplicando una arquitectura de software moderna (3 Capas + MVVM) para mejorar la mantenibilidad, escalabilidad y testeabilidad del código.ArquitecturaEste proyecto implementa una arquitectura limpia de 3 capas combinada con el patrón MVVM (Model-View-ViewModel) para la capa de interfaz de usuario.Capa de Datos (Data Layer):Responsable de la persistencia y el origen de los datos.datasources: Implementación de la conexión a la base de datos (ej. SQLServerDataSource).repositories: Implementación de las interfaces de repositorio (ej. ClienteRepositoryImpl).Capa de Dominio (Domain Layer):El "cerebro" de la aplicación. Contiene la lógica de negocio pura.models: Entidades de negocio (ej. Cliente).repositories: Interfaces (contratos) de los repositorios (ej. IClienteRepository).usecases: Clases que encapsulan acciones de negocio específicas (ej. GuardarClienteUseCase).Capa de IU (UI Layer):Responsable de la presentación y la interacción con el usuario.views: Las ventanas de Tkinter (ej. ClienteView). Son "tontas" y solo notifican al ViewModel.viewmodels: Contienen el estado de la UI y la lógica de presentación (ej. ClienteViewModel).theme.py: Módulo de estilo centralizado para la apariencia de la aplicación.CaracterísticasGestión de Clientes: CRUD completo de clientes.Tema Oscuro: Interfaz de usuario moderna y consistente.Arquitectura Limpia: Código desacoplado y fácil de mantener.(Próximamente): Gestión de Vehículos, Reservas, Contratos y Pagos.Instalación y EjecuciónSigue estos pasos para ejecutar el proyecto localmente.1. PrerrequisitosPython 3.8 o superior.Un servidor SQL Server (Express, Developer, etc.) accesible.Controlador ODBC de Microsoft SQL Server (ej. ODBC Driver 17).2. Clonar el Repositoriogit clone [https://github.com/StoneFind22/DriveFlow.git](https://github.com/StoneFind22/DriveFlow.git)
cd DriveFlow
3. Configurar el EntornoSe recomienda encarecidamente usar un entorno virtual.# Crear el entorno virtual
python -m venv venv

# Activar el entorno
# En Windows (PowerShell):
./venv/Scripts/Activate

# En macOS/Linux:
source venv/bin/activate
4. Instalar DependenciasInstala todas las bibliotecas necesarias.pip install -r requirements.txt
5. Configurar Variables de EntornoEste proyecto usa un archivo .env para manejar las credenciales de la base de datos de forma segura.Copia el archivo de ejemplo:copy .env.example .env
Edita el archivo .env con tus credenciales de SQL Server:DB_SERVER=localhost
DB_NAME=AlquilerAutos
DB_USERNAME=tu_usuario_sql
DB_PASSWORD=tu_contraseña_sql
(Nota: Si usas autenticación de Windows, deja DB_USERNAME y DB_PASSWORD en blanco).6. Ejecutar la AplicaciónUna vez que la base de datos esté configurada y las dependencias instaladas, inicia la aplicación:python main.py


## ⚖️ Licencia
Este proyecto está bajo los términos de la [Licencia MIT](LICENSE).