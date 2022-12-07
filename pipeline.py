from modules.file_handler import FileHandler
from modules.csv_processor import CsvProcessor

def main():
    files_to_process = FileHandler().spec_and_file()
    print(files_to_process)
    for files in files_to_process:
        processor = CsvProcessor(files)
        processor.load_schema()
        df = processor.load_data()
        print(df)
        processor.write_data()

if __name__ == "__main__":
    main()