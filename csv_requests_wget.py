import csv

def modify_csv(csv_file):
    rows = []  # To store modified rows

    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # Modify the 'Price' field, e.g., increase each price by 5
            row['Price'] = str(float(row['Price']) + 5)
            rows.append(row)

    # Write the changes back to the CSV file
    fieldnames = ['Title', 'Author', 'Price']
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    csv_file_path = 'example.csv'
    modify_csv(csv_file_path)
