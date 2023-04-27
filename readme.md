## Create chunks

### Step 1: Split the CSV file into parts of 100000 lines and prefix the generated files with "file_".
'''
split -l 100000 -d filename.csv file_
'''

### Step 2: Add .csv to all generated files.
'''
for i in $(find file_*); do mv $i "$i.csv"; done
'''

### Step 3: Copy header from first generated file at the beginning of the other files.
'''
for i in $(find . -type f -name "file_*.csv" -not -name "file_00.csv");
    do echo -e "$(head -1 file_00.csv)\n$(cat $i)" > $i;
done
'''
