# SalleVoice Backend

Este es el repositorio del backend de la aplicación SalleVoice.

## Instalación

En este fichero se comentará el proceso recomendado para la ejecución de la plataforma. Es posible conseguir ejecutar la aplicación sin seguir estrictamente estos pasos. 

### Requisitos previos a la instalación de la aplicación

#### Creación de un entorno virtual con Python

Un entorno virtual permite aislar las dependencias de tu proyecto para evitar conflictos con otras aplicaciones. A continuación, se describen los pasos para crear y activar un entorno virtual en Python:

1. **Instalar `virtualenv`**:
    Si no tienes `virtualenv` instalado, puedes instalarlo usando `pip`:
    ```bash
    pip install virtualenv
    ```

2. **Crear el entorno virtual**:
    Navega a la raíz de tu proyecto y ejecuta el siguiente comando para crear un entorno virtual llamado `venv`:
    ```bash
    virtualenv venv
    ```
    
#### Instalación de Chocolaty

Chocolaty es un gestor de paquetes para Windows que facilita la instalación de software. Podemos descargar este gestor de paquetes en su página web oficial: [Chocolaty](https://chocolatey.org/)

#### Instalación de FFmpeg con Chocolaty

Una vez que Chocolaty esté instalado, puede instalar FFmpeg ejecutando el siguiente comando en PowerShell:

```powershell
choco install ffmpeg
```

#### Instalación de AWS CLI

Para utilizar Amazon Polly, es necesario instalar AWS CLI y configurar una cuenta de AWS. Siga las instrucciones en el siguiente enlace para instalar AWS CLI:

[Instalación de AWS CLI](https://aws.amazon.com/es/cli/)


#### Creación de un usuario en IAM Identity Center

Para gestionar el acceso a los recursos de AWS, es necesario crear un usuario en IAM Identity Center. Esto permite definir permisos específicos para cada usuario y mejorar la seguridad de la aplicación. Siga las instrucciones en el siguiente enlace para acceder y crear un usuario en IAM Identity Center:

[Creación de un usuario en IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/getting-started.html)

#### Configuración de claves para Amazon Polly

Al finalizar el proceso de instalación, se le proporcionarán tres claves necesarias para habilitar el servicio de Amazon Polly. Estas claves deben ser añadidas al archivo `polly_service.ts` para que la aplicación pueda utilizar Amazon Polly correctamente. Las claves son las siguientes:

1. **AWS_ACCESS_KEY_ID**: Esta clave identifica su cuenta de AWS.
2. **AWS_SECRET_ACCESS_KEY**: Esta clave es la contraseña asociada a su cuenta de AWS.

Asegúrese de agregar estas claves en el archivo `polly_service.ts` de la siguiente manera:

```typescript
self.client = Session(
            aws_access_key_id="your-access-key-id",
            aws_secret_access_key="your-secret-access-key",
            region_name="us-east-1"
        ).client("polly")
```

Reemplace `'your-access-key-id'` y `'your-secret-access-key'` con los valores proporcionados. Se puede modificar la región si así se desea, pero algunos servicios de Polly pueden no estar disponibles. 

#### Instalación de dependencias

Es importante instalar todas las dependencias almacenadas en el archivo `requirements.txt` ubicado en la raíz del proyecto. Esto se realiza con el siguiente comando:

```bash
# Este comando se debe ejecutar una vez activado el entorno virtual explicado en el apartado **Ejecuacion de la aplicación**
pip install -r requirements.txt
```

### Ejecución de la aplicación

Para consumir la API, necesitamos ejecutar la aplicación en un entorno de desarrollo utilizando FastAPI. A continuación, se detallan los pasos para ejecutar la aplicación:

1. Activar el entorno virtual:
    ```bash
    # En una terminal introducir el siguiente comando para activar el entorno virtual
    .\venv\Scripts\activate
    # IMPORTANTE: si no se han instalado las dependencias se debe ejecutar
    pip install -r requirements.txt 
    ```

2. Ejecutar la aplicación con FastAPI:
    ```bash
    fastapi dev .\app\main.py
    ```

Esto iniciará el servidor de desarrollo y podrá acceder a la API en `http://127.0.0.1:8000`.



