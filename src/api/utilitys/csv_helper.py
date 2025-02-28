import csv
from typing import List, Any
from pathlib import Path
from datetime import datetime

class CsvHelper:
    @staticmethod
    def export_to_csv(data: List[Any], filename: str = None) -> str:
        """
        Export a list of objects to a CSV file
        
        Args:
            data: List of objects to export
            filename: Optional filename, if not provided will generate based on timestamp
            
        Returns:
            str: Path to the generated CSV file
        """
        if not data:
            raise ValueError("No data to export")
            
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"export_{timestamp}.csv"
            
        # Ensure output directory exists
        output_dir = Path("exports")
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        
        # Get field names from the first object
        fieldnames = [key for key in data[0].__dict__.keys() if not key.startswith('_')]
        
        try:
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                for item in data:
                    writer.writerow({
                        field: getattr(item, field) 
                        for field in fieldnames
                    })
                    
            return str(filepath)
            
        except Exception as e:
            raise Exception(f"Failed to export CSV: {str(e)}")