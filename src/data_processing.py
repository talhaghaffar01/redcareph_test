from src.schema import ProcessedData, Product
from typing import List, Dict, Any
import json
import os

class DataProcessor:
    def __init__(self, input_directory, output_directory):
        """
        Initializes the DataProcessor object.

        Args:
            input_directory (str): The directory containing the input data files.
            output_directory (str): The directory where processed data will be saved.
        """
        self.input_directory = input_directory
        self.output_directory = output_directory

    def process_data(self, filename):
        """
        Processes the data from the input file and saves the processed data to the output directory.

        Args:
            filename (str): The name of the input file to process.

        Returns:
            str or None: The filepath where the processed data is saved, or None if the operation fails.
        """
        try:
            if not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory)

            output_filename = "processed_raw_data.json"
            output_filepath = os.path.join(self.output_directory, output_filename)
            input_filepath = os.path.join(self.input_directory, filename)

            with open(input_filepath, 'r') as file:
                raw_data = json.load(file)

            processed_data = self._process_json_data(raw_data)

            with open(output_filepath, 'w') as file:
                json.dump(processed_data, file, indent=4)

            print(f"Data processed successfully and saved at: {output_filepath}")
            return output_filepath
        except Exception as e:
            print(f"An error occurred during data processing: {str(e)}")
            return None

    def _process_json_data(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Processes the raw JSON data into a structured format.

        Args:
            raw_data (Dict[str, Any]): The raw JSON data to process.

        Returns:
            List[Dict[str, Any]]: The processed data in a structured format.
        """
        processed_data = []
        for result in raw_data.get('results', []):
            processed_result = {
                "application_number": result.get('application_number', ''),
                "sponsor_name": result.get('sponsor_name', ''),
                "products": [
                    {
                        "product_number": product.get('product_number', ''),
                        "reference_drug": product.get('reference_drug', ''),
                        "brand_name": product.get('brand_name', ''),
                        "active_ingredients": product.get('active_ingredients', []),
                        "reference_standard": product.get('reference_standard', ''),
                        "dosage_form": product.get('dosage_form', ''),
                        "route": product.get('route', ''),
                        "marketing_status": product.get('marketing_status', '')
                    }
                    for product in result.get('products', [])
                ]
            }
            processed_data.append(processed_result)
        return processed_data
