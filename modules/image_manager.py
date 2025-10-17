from pathlib import Path
import pandas as pd
from PIL import Image
import numpy as np
from typing import List, Dict, Optional
from .data_models import Patient
from .file_utils import FileUtils

class ImageManager:
    """Gestor de imágenes médicas"""
    
    def __init__(self, data_path: Path):
        """
        Inicializar el gestor de imágenes
        
        Args:
            data_path (Path): Ruta al dataset
        """
        self.data_path = data_path
        self.patients: Dict[str, Patient] = {}
        self._load_patients()
    
    def _load_patients(self) -> None:
        """Cargar todos los pacientes del dataset"""
        fundus_path = self.data_path / "FundusImages"
        contour_path = self.data_path / "ExpertsSegmentations" / "Contours"
        contour_images_path = self.data_path / "ExpertsSegmentations" / "ImagesWithContours"
        
        # Encontrar todas las imágenes
        image_files = FileUtils.find_images(fundus_path)
        
        print(f"Encontradas {len(image_files)} imágenes en FundusImages")
        
        for image_file in image_files:
            patient_id, eye, _ = FileUtils.extract_patient_info(image_file.name)
            
            if patient_id and eye:
                # Buscar todos los archivos que contengan el ID y ojo
                
                # Encontrar contornos relacionados - método más robusto
                contour_files = []
                expected_prefix = f"RET{patient_id}{eye}"
                for contour_file in contour_path.glob("*.txt"):
                    if contour_file.name.startswith(expected_prefix):
                        contour_files.append(contour_file)
        
        
                '''
                contour_files = []
                for contour_file in contour_path.glob("*.txt"):
                    if f"RET{patient_id}{eye}" in contour_file.name:
                        contour_files.append(contour_file)
                '''
                
                
                # Encontrar imagen con contornos
                contour_image_pattern = f"Opht_cont_RET{patient_id}{eye}.jpg"
                contour_image_files = list(contour_images_path.glob(contour_image_pattern))
                
                '''
                # Encontrar imagen con contornos
                contour_image_pattern = f"Opht_cont_RET{patient_id}{eye}.jpg"
                contour_image_files = list(contour_images_path.glob(contour_image_pattern))
                '''
                
                patient_key = f"{patient_id}_{eye}"
                self.patients[patient_key] = Patient(
                    patient_id=patient_id,
                    eye=eye,
                    image_path=image_file,
                    contour_paths=contour_files,
                    contour_image_paths=contour_image_files
                )
    
    def get_patient(self, patient_id: str, eye: str) -> Optional[Patient]:
        """
        Obtener un paciente por ID y ojo
        
        Args:
            patient_id (str): ID del paciente
            eye (str): OD o OS
            
        Returns:
            Optional[Patient]: Objeto Patient o None si no se encuentra
        """
        patient_key = f"{patient_id}_{eye}"
        return self.patients.get(patient_key)
    
    def list_patients(self) -> List[Dict]:
        """
        Listar todos los pacientes
        
        Returns:
            List[Dict]: Lista de información de pacientes
        """
        patients_list = []
        for patient_key, patient in self.patients.items():
            try:
                has_contour_image = bool(patient.contour_image_paths and len(patient.contour_image_paths) > 0)
            except:
                has_contour_image = False
                
            try:
                contour_count = len(patient.contour_paths)
            except:
                contour_count = 0
                
            patients_list.append({
                'patient_id': patient.patient_id,
                'eye': patient.eye,
                'image_path': str(patient.image_path),
                'contour_count': contour_count,
                'has_contour_image': has_contour_image
            })
        return patients_list
    
    def load_image(self, patient_id: str, eye: str) -> Optional[Image.Image]:
        """
        Cargar imagen de un paciente usando PIL
        
        Args:
            patient_id (str): ID del paciente
            eye (str): OD o OS
            
        Returns:
            Optional[Image.Image]: Imagen PIL o None si hay error
        """
        patient = self.get_patient(patient_id, eye)
        if patient and patient.image_path.exists():
            try:
                return Image.open(patient.image_path)
            except Exception as e:
                print(f"Error cargando imagen: {e}")
        return None
    
    def get_image_info(self, patient_id: str, eye: str) -> Optional[Dict]:
        """
        Obtener información de la imagen
        
        Args:
            patient_id (str): ID del paciente
            eye (str): OD o OS
            
        Returns:
            Optional[Dict]: Información de la imagen
        """
        patient = self.get_patient(patient_id, eye)
        if patient:
            image = self.load_image(patient_id, eye)
            if image is not None:
                has_contour_image = len(patient.contour_image_paths) > 0
                
                return {
                    'patient_id': patient_id,
                    'eye': eye,
                    'dimensions': image.size,  # (width, height)
                    'mode': image.mode,
                    'format': image.format,
                    'file_size': patient.image_path.stat().st_size,
                    'contour_files': len(patient.contour_paths),
                    'has_contour_image': has_contour_image
                }
        return None
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        