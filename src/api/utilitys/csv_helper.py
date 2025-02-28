import csv
from typing import List, Any, Dict, Optional, IO
from io import StringIO
from datetime import datetime

class CsvHelper:
    @staticmethod
    def export_to_csv(data: List[Any], headers: Dict[str, str] = None) -> StringIO:
        """
        Export a list of objects to a CSV file stream
        
        Args:
            data: List of objects to export
            headers: Optional dictionary mapping field names to header labels, also controls column order
            
        Returns:
            StringIO: CSV file content as a string buffer
        """
        if not data:
            raise ValueError("No data to export")

        # If no headers provided, use all fields from first object
        if not headers:
            fieldnames = [key for key in data[0].__dict__.keys() if not key.startswith('_')]
            headers = {field: field for field in fieldnames}
        
        try:
            # Create string buffer for CSV content
            output = StringIO()
            writer = csv.writer(output)
            
            # Write header row
            writer.writerow(headers.values())
            
            # Write data rows
            for item in data:
                row = [getattr(item, field, '') for field in headers.keys()]
                writer.writerow(row)
            
            # Reset buffer position to start
            output.seek(0)
            return output
            
        except Exception as e:
            raise Exception(f"Failed to export CSV: {str(e)}")