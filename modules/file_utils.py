import os
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

class FileUtils:
    """Utilidades para manejo de archivos del dataset PapilaDB"""
    
    
    

    
    @staticmethod
    def extract_patient_info(filename: str) -> tuple:
        """
        Extraer información del paciente desde el nombre del archivo
        """
        try:
            base_name = Path(filename).stem
            
            # Caso 1: Imágenes de fondo (RET002OD.jpg, RET010OD.jpg, etc.)
            if base_name.startswith('RET'):
                import re
                # Patrón más flexible para IDs de 2-3 dígitos
                ret_match = re.match(r'RET(\d{2,3})(OD|OS)$', base_name)
                if ret_match:
                    patient_id = ret_match.group(1).zfill(3)  # Rellena con ceros a la izquierda
                    eye = ret_match.group(2)
                    return patient_id, eye, 'image'
            
            # Caso 2: Archivos de contorno (RET002OD_cup_exp1.txt)
            elif base_name.startswith('RET') and '_' in base_name:
                import re
                # Extraer "RET002OD" de "RET002OD_cup_exp1"
                ret_match = re.match(r'RET(\d{2,3})(OD|OS)_', base_name)
                if ret_match:
                    patient_id = ret_match.group(1).zfill(3)
                    eye = ret_match.group(2)
                    return patient_id, eye, 'contour'
            
            # Caso 3: Imágenes con contornos (Opht_cont_RET002OD.jpg)
            elif 'RET' in base_name:
                import re
                # Encontrar "RET002OD" en "Opht_cont_RET002OD"
                ret_match = re.search(r'RET(\d{2,3})(OD|OS)', base_name)
                if ret_match:
                    patient_id = ret_match.group(1).zfill(3)
                    eye = ret_match.group(2)
                    return patient_id, eye, 'contour_image'
            
            return None, None, None
            
        except Exception as e:
            print(f"Error extrayendo info de {filename}: {e}")
            return None, None, None    
    
    
    
    
    
    @staticmethod
    def load_clinical_data(file_path: Path) -> pd.DataFrame:
        """
        Cargar datos clínicos desde archivo Excel
        
        Args:
            file_path (Path): Ruta al archivo Excel
            
        Returns:
            pd.DataFrame: DataFrame con datos clínicos
        """
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            print(f"Error cargando datos clínicos: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def find_images(base_path: Path) -> List[Path]:
        """
        Encontrar todas las imágenes en el dataset
        
        Args:
            base_path (Path): Ruta base del dataset
            
        Returns:
            List[Path]: Lista de rutas de imágenes
        """
        image_extensions = ['.jpg', '.jpeg', '.png']
        images = []
        
        for ext in image_extensions:
            images.extend(base_path.glob(f'**/*{ext}'))
        
        return images