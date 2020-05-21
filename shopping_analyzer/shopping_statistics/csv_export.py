import csv


def write_data_to_csv(source_directory, filename, data):
    with open(f'{source_directory}/report/{filename}', mode='w', newline='') as report_file:
        report_writer = csv.writer(report_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        report_writer.writerows(data)
