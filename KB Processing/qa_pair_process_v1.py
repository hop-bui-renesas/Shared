import pandas as pd
import re
import json
import logging
import sys
import os
import string
import openpyxl
from argparse import ArgumentParser
logger = logging.getLogger("log4j")

class QAPairProcessing():
    def __init__(self, ble_path, ra_path, jsonl_save_path):
        
        self.validate_input(ble_path, ra_path, jsonl_save_path)

        self.ble_df = self.process_dataframe(ble_path)
        self.ra_df = self.process_dataframe(ra_path)
        
        self.ble_df.dropna(inplace=True)
        self.ra_df.dropna(inplace=True)
        
        self.jsonl_save_path = jsonl_save_path

    def validate_input(self, ble_path, ra_path, jsonl_save_path):
        if not os.path.exists(ble_path):
            raise Exception(f"The path {ble_path} does not exists")
        if not os.path.exists(ra_path):
            raise Exception(f"The path {ra_path} does not exists")
        if not os.path.exists(jsonl_save_path):
            raise Exception(f"The path {jsonl_save_path} does not exists")

    def process_dataframe(self, path):
        # Read in the files
        df = pd.read_excel(path)
        workbook = openpyxl.load_workbook(path)

        # Create a `Worksheet` object 
        worksheet = workbook[workbook.sheetnames[0]]

        # List of indices corresponding to all hidden rows
        hidden_rows_idx = [int(row) - 2 for row, dimension in worksheet.row_dimensions.items() if dimension.hidden]

        # List of indices corresponding to all hidden columns
        hidden_cols_idx = [
            string.ascii_uppercase.index(col_name) 
            for col_name in [
                col 
                for col, dimension in worksheet.column_dimensions.items() 
                if dimension.hidden
            ] 
        ]

        # Find names of columns corresponding to hidden column indices
        hidden_cols_name = df.columns[hidden_cols_idx].tolist()

        # Drop the hidden columns and rows
        df.drop(hidden_cols_name, axis=1, inplace=True)
        df.drop(hidden_rows_idx, axis=0, inplace=True)

        # Reset the index and return dataframe
        df.reset_index(drop=True, inplace=True)
        
        return df

    def extract_qa_pairs(self, df):
        try:
            text = df["Action Description"]
            title = df["Ticket Name"]
            # print("Title", title)
            match_question = re.search(
                r"question:(.*?)(?:answer:|$)", text, re.IGNORECASE | re.DOTALL
            )
            match_answer = re.search(r"answer:(.*$)", text, re.IGNORECASE | re.DOTALL)
            format_answer = {
                "question": match_question.group(1).strip() if match_question else title,
                "answer": match_answer.group(1).strip() if match_answer else text,
            }
            return format_answer
        except Exception as e:
            text = df["Action Description"]
            title = df["Ticket Name"]
            print(text)
            print(title)
            logger.error(f"Error in Extract QA Pairs : {e}")
            

    def convert_to_jsonl(self, df):
        # Convert DataFrame to JSONL format
        save_name = df[1]
        df = df[0]
        with open(os.path.join(self.jsonl_save_path, f"{save_name}.jsonl"), "w") as jsonl_file:
            for index, row in df.iterrows():
                json_data = row["QA_Pair"]
                json_line = json.dumps(json_data)
                jsonl_file.write(json_line + "\n")

        print(f"DataFrame converted to JSONL format and saved to {self.jsonl_save_path}")
        
    def main(self):
        print("Extracting QA Pairs")
        self.ble_df["QA_Pair"] = self.ble_df.apply(self.extract_qa_pairs, axis=1) # type: ignore
        self.ra_df['QA_Pair'] = self.ra_df.apply(self.extract_qa_pairs, axis=1) # type: ignore
        
        ble_save_name = "processed_ble"
        ra_save_name = "processed_ra"
        
        self.ble_df.to_csv(os.path.join(self.jsonl_save_path,f"{ble_save_name}.csv"), index = False)
        self.ra_df.to_csv(os.path.join(self.jsonl_save_path,f"{ra_save_name}.csv"), index = False)
        
        for i in [[self.ble_df, ble_save_name], [self.ra_df, ra_save_name]]:
            self.convert_to_jsonl(i)
        
if __name__ == "__main__":
    
    parser = ArgumentParser(description='Key-Value Pair Parser')
    parser.add_argument('-ble_path', '--ble_path', type=str, help='Knowledge Base : BLE File Path')
    parser.add_argument('-ra_path', '--ra_path', type=str, help='Knowledge Base : RA File Path')
    parser.add_argument('-jsonl_save_path', '--jsonl_save_path', type=str, help='Formatted data store Path')
    args = parser.parse_args()

    if not os.path.exists(args.jsonl_save_path):
        os.makedirs(args.jsonl_save_path)

    qa_pair_processing_class = QAPairProcessing(args.ble_path, args.ra_path, args.jsonl_save_path)
    qa_pair_processing_class.main()
    
    print("Finished processing the Knowledge Base QA Pairs")