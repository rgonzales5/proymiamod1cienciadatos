import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional

class MetadataManager:
    """Gestor de metadatos del dataset médico"""
    
    def __init__(self, data_path: Path):
        """
        Inicializar el gestor de metadatos
        
        Args:
            data_path (Path): Ruta al dataset
        """
        self.data_path = data_path
        self.clinical_data_od = None
        self.clinical_data_os = None
        self._load_clinical_data()
    
    def _load_clinical_data(self) -> None:
        """Cargar datos clínicos desde archivos Excel"""
        clinical_path = self.data_path / "ClinicalData"
        
        try:
            od_file = clinical_path / "patient_data_od.xlsx"
            os_file = clinical_path / "patient_data_os.xlsx"
            
            if od_file.exists():
                self.clinical_data_od = pd.read_excel(od_file)
            if os_file.exists():
                self.clinical_data_os = pd.read_excel(os_file)
                
        except Exception as e:
            print(f"Error cargando datos clínicos: {e}")
    
    def get_patient_clinical_data(self, patient_id: str, eye: str) -> Optional[Dict]:
        """
        Obtener datos clínicos de un paciente
        
        Args:
            patient_id (str): ID del paciente
            eye (str): OD o OS
            
        Returns:
            Optional[Dict]: Datos clínicos del paciente
        """
        try:
            # VERIFICAR que patient_id sea numérico
            if not patient_id.isdigit():
                print(f"Error: ID de paciente '{patient_id}' no es numérico")
                return None
                
            patient_id_int = int(patient_id)
            
            if eye == 'OD' and self.clinical_data_od is not None:
                patient_data = self.clinical_data_od[
                    self.clinical_data_od['PatientID'] == patient_id_int
                ]
            elif eye == 'OS' and self.clinical_data_os is not None:
                patient_data = self.clinical_data_os[
                    self.clinical_data_os['PatientID'] == patient_id_int
                ]
            else:
                return None
            
            if not patient_data.empty:
                return patient_data.iloc[0].to_dict()
            else:
                print(f"No se encontraron datos clínicos para paciente {patient_id} ({eye})")
                return None
                
        except Exception as e:
            print(f"Error obteniendo datos clínicos para {patient_id}{eye}: {e}")
            return None
    
    def update_clinical_data(self, patient_id: str, eye: str, updates: Dict) -> bool:
        """
        Actualizar datos clínicos de un paciente
        
        Args:
            patient_id (str): ID del paciente
            eye (str): OD o OS
            updates (Dict): Datos a actualizar
            
        Returns:
            bool: True si se actualizó correctamente
        """
        # Esta es una implementación basica - en un sistema real
        # se guardaría en una base de datos
        print(f"Datos actualizados para paciente {patient_id} ({eye}): {updates}")
        return True