# =============================================================================================
#  ARCHIVO:      data_models.py
#  DESCRIPCIÓN:  Este archivo modela las clases usadas en el sistema. Principalmente Patient -> Paciente.
#
#  AUTOR:        Dennis Delgado A.
#  FECHA:        12-10-2025
#
#  HISTORIAL DE MODIFICACIONES:
#  -----------------------------------------------------------------------------
#  FECHA       | AUTOR            | VERSIÓN | DESCRIPCIÓN DEL CAMBIO
#  -----------------------------------------------------------------------------
#  12-10-2025  | Dennis Delgado   | 1.0     | Versión inicial del archivo.
#  13-10-2025  | Rolando Gonzales | 1.1     | Se mejoro la verificacion de error con 'raiseerror'.
#  -----------------------------------------------------------------------------
# =============================================================================================


from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

@dataclass
class Patient:
    """Clase para representar un paciente"""
    patient_id: str # tuve que aumentar esto por que me daba un error de tipo constante
    eye: str  # OD (ojo derecho) o OS (ojo izquierdo)
    image_path: Path
    contour_paths: List[Path]
    contour_image_paths: List[Path]  # AGREGAR ESTA LÍNEA
    clinical_data: Optional[dict] = None
    
    def __post_init__(self):
        """Validar datos después de la inicialización"""
        if self.eye not in ['OD', 'OS']:
            raise ValueError("El ojo debe ser 'OD' o 'OS'")
        if self.contour_image_paths is None:
            self.contour_image_paths = []  # Inicializar como lista vacía si es None