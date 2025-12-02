# Deep Dive: Poetry vs Pip

Este documento explica técnicamente por qué elegimos **Poetry** sobre `pip` para este framework, usando analogías claras para explicarlo a gerencia.

---

## 1. La Analogía del Chef (Para explicarlo fácil)

Imagina que vas a cocinar un pastel (tu software).

*   **Pip (`requirements.txt`)**: Es como una receta que dice: *"Usa harina y huevos"*.
    *   **El problema**: No especifica la marca ni el tipo. Hoy compras harina "Selecta", mañana "Lider". Hoy el pastel queda rico, mañana se quema.
    *   **En Software**: Instalas hoy y funciona. Instalas mañana en el servidor y falla porque se actualizó una librería "por debajo".

*   **Poetry (`poetry.lock`)**: Es una receta que dice: *"Usa 500g de Harina Selecta Lote #452 y 3 Huevos Calbuco Lote #99"*.
    *   **La ventaja**: El pastel sabe **exactamente igual** hoy, mañana, en mi cocina o en la cocina del restaurante (Producción).
    *   **En Software**: Garantiza que el código que probaste en tu notebook es **bit a bit idéntico** al que corre en Producción.

---

## 2. Comparativa Técnica

| Característica | Pip (`requirements.txt`) | Poetry (`pyproject.toml` + `lock`) |
| :--- | :--- | :--- |
| **Resolución de Conflictos** | **Ciega**. Instala lo que le pides. Si A pide "numpy 1.0" y B pide "numpy 2.0", `pip` rompe todo sin avisar. | **Inteligente**. Calcula el árbol matemático de dependencias antes de instalar. Si hay conflicto, te avisa y no te deja romper el entorno. |
| **Reproducibilidad** | **Baja**. `pip freeze` es manual y propenso a errores. | **Total**. El archivo `poetry.lock` es la "foto" exacta del universo de librerías. |
| **Gestión de Entornos** | Manual (tienes que crear el venv tú mismo). | **Automática**. Poetry crea y gestiona los entornos virtuales por ti. |
| **Separación Dev/Prod** | Difícil. Necesitas `requirements-dev.txt`, `requirements-test.txt`, etc. | **Nativa**. `poetry add --group dev pytest` separa claramente lo que va a producción de lo que es para desarrollo. |

---

## 3. ¿Por qué es crítico para "Lo Nuestro" (DataPipe)?

Para nuestro framework Multi-Cloud y Dockerizado, **Poetry no es un lujo, es una necesidad** por 3 razones:

### A. Seguridad en Docker
Cuando construimos la imagen Docker, copiamos el `poetry.lock`.
*   **Con Pip**: Podría pasar que la imagen que construyes hoy en tu PC sea distinta a la que construye el CI/CD mañana, causando bugs "fantasmas" imposibles de rastrear.
*   **Con Poetry**: La imagen es **inmutable**. Tenemos certeza matemática de qué código está corriendo.

### B. El "Infierno de Dependencias" (Dependency Hell)
Usamos librerías pesadas y complejas: `google-cloud-bigquery`, `boto3` (AWS), `azure-storage-blob`, `pandas`, `fastavro`.
*   Estas librerías a menudo pelean entre sí (ej. una quiere `urllib3 v1` y la otra `urllib3 v2`).
*   **Pip** dejaría que se instalen versiones incompatibles, y el error saltaría **en tiempo de ejecución** (cuando el proceso ya está corriendo a las 3 AM).
*   **Poetry** detecta el conflicto **al instalar** (en tu máquina), obligándote a arreglarlo antes de subir a producción.

### C. Empaquetado Profesional
Nuestro framework es una herramienta CLI (`datapipe ...`). Poetry facilita empaquetar esto como una aplicación real, gestionando los "entry points" (los comandos) de forma estándar, tal como lo hacen las grandes librerías open source.

---

## 4. Resumen para Jefatura

> "Usar **Poetry** es nuestra póliza de seguro contra fallos en producción. Nos cuesta lo mismo implementarlo, pero nos ahorra cientos de horas de debugging futuro por incompatibilidades de librerías."
