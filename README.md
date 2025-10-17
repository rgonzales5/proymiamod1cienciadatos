# Sistema de Gestion de Imagenes Medicas - PAPILA DB

## Descripcion
Sistema para gestionar imagenes de fondo de ojo del dataset PAPILA DB.

## Setup del proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU-USUARIO/TU-REPO.git
cd TU-REPO
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Descargar el dataset
**IMPORTANTE**: El dataset NO esta en GitHub por su tamano.

Descargar desde: la pagina oficial

Colocar en la carpeta:
```
data/PapilaDB-PAPILA/
```

Estructura esperada:
```
data/
└── PapilaDB-PAPILA/
    ├── ClinicalData/
    ├── ExpertsSegmentations/
    ├── FundusImages/
    └── HelpCode/
```

### 4. Ejecutar el proyecto
```bash
jupyter notebook main.ipynb
```

## Estructura del proyecto
```
.
├── main.ipynb
├── modules/
│   ├── data_models.py
│   ├── file_utils.py
│   ├── image_manager.py
│   └── metadata_manager.py
└── data/
    └── PapilaDB-PAPILA/ (descargar aparte)
```

## Colaboradores
- Ing. Rolando Gonzales C.
- Ing. Dennis Delgado
- poner nombre
- poner nombre