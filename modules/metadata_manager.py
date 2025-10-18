# =============================================================================================
#  ARCHIVO:      metadata_manager.py
#  DESCRIPCIÓN:  Este archivo mmaneja los pacientes y sus imagenes.
#
#  AUTOR:        Dennis Delgado A.
#  FECHA:        12-10-2025
#
#  HISTORIAL DE MODIFICACIONES:
#  -----------------------------------------------------------------------------
#  FECHA       | AUTOR            | VERSIÓN | DESCRIPCIÓN DEL CAMBIO
#  -----------------------------------------------------------------------------
#  12-10-2025  | Dennis Delgado   | 1.0     | Versión inicial del archivo.
#  14-10-2025  | Herland Maldonado | 1.1     | se puso manejo de escepciones al tratar con los archivos excelod_file = clinical_path / "patient_data_od.xlsx"
#  15-10-2025  | Dennis Delgado | 1.2     | se arreglaron los formatos de las columnas de los datos. self.clinical_data_os.columns = ['ID',...
#  15-10-2025  | Rolando Gonzales | 1.2     | se arreglaron el aceso al archivo excel y el formato de de lectura
#  16-10-2025  | Wilson Cruz | 1.2     | se mejoro el sistema de excepciones del metodo "get_patient_clinical_data"
#  -----------------------------------------------------------------------------
# =============================================================================================

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
    



    # metadata_manager.py - Método _load_clinical_data - REEMPLAZAR:
    def _load_clinical_data(self) -> None:
        """Cargar datos clínicos desde archivos Excel"""
        clinical_path = self.data_path / "ClinicalData"
        
        try:
            od_file = clinical_path / "patient_data_od.xlsx"
            os_file = clinical_path / "patient_data_os.xlsx"
            
            if od_file.exists():
                # Leer saltando las primeras 2 filas de encabezados
                self.clinical_data_od = pd.read_excel(od_file, header=2)
                # Limpiar y estandarizar nombres de columnas
                self.clinical_data_od.columns = ['ID', 'Age', 'Gender', 'Diagnosis', 'dioptre_1', 'dioptre_2', 
                                               'astigmatism', 'Phakic/Pseudophakic', 'Pneumatic', 'Perkins', 
                                               'Pachymetry', 'Axial_Length', 'VF_MD']
                print(f"Datos OD cargados: {len(self.clinical_data_od)} pacientes")
                
            if os_file.exists():
                self.clinical_data_os = pd.read_excel(os_file, header=2)
                self.clinical_data_os.columns = ['ID', 'Age', 'Gender', 'Diagnosis', 'dioptre_1', 'dioptre_2', 
                                               'astigmatism', 'Phakic/Pseudophakic', 'Pneumatic', 'Perkins', 
                                               'Pachymetry', 'Axial_Length', 'VF_MD']
                print(f"Datos OS cargados: {len(self.clinical_data_os)} pacientes")
                    
        except Exception as e:
            print(f"Error cargando datos clínicos: {e}")


    def get_patient_clinical_data(self, patient_id: str, eye: str) -> Optional[Dict]:
        """
        Obtener datos clínicos de un paciente
        """
        try:
            # Formatear ID para coincidir con el Excel (ej: "002" -> "#002")
            excel_id = f"#{patient_id.zfill(3)}"
            
            clinical_data = self.clinical_data_od if eye == 'OD' else self.clinical_data_os
            if clinical_data is None:
                print(f"No hay datos clínicos cargados para {eye}")
                return None
            
            # DEBUG: Verificar columnas disponibles
            print(f"Columnas disponibles: {list(clinical_data.columns)}")
            print(f"Buscando ID: {excel_id}")
            
            # Búsqueda robusta - manejar espacios y formato
            clinical_data['ID_clean'] = clinical_data['ID'].astype(str).str.strip().str.upper()
            excel_id_clean = excel_id.strip().upper()
            patient_data = clinical_data[clinical_data['ID_clean'] == excel_id_clean]
            
            if not patient_data.empty:
                print(f"Datos encontrados para {excel_id}")
                # Convertir a dict y limpiar la columna temporal
                result = patient_data.iloc[0].to_dict()
                result.pop('ID_clean', None)  # Remover columna temporal
                return result
            else:
                # Intentar búsqueda alternativa
                all_ids = clinical_data['ID'].dropna().unique()
                print(f"IDs disponibles en {eye}: {all_ids[:10]}...")  # Mostrar primeros 10
                print(f"No se encontraron datos clínicos para paciente {excel_id} ({eye})")
                return None
                
        except Exception as e:
            print(f"Error obteniendo datos clínicos para {patient_id}{eye}: {e}")
            import traceback
            traceback.print_exc()
            return None



