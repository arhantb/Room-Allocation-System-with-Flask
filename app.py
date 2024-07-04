from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    group_file = request.files['group_file']
    hostel_file = request.files['hostel_file']

    if not group_file or not hostel_file:
        return jsonify({'error': 'No files uploaded'}), 400

    group_df = pd.read_csv(group_file)
    hostel_df = pd.read_csv(hostel_file)

    allocations = allocate_rooms(group_df, hostel_df)

    return jsonify(allocations)

def allocate_rooms(group_df, hostel_df):
    allocations = []

    for _, group in group_df.iterrows():
        group_id = group['Group ID']
        members = group['Members']
        gender = group['Gender']

        if isinstance(gender, str) and '&' in gender:
            boys_members = int(gender.split('&')[0].strip().split()[0])
            girls_members = int(gender.split('&')[1].strip().split()[0])
            boys_group = {'Group ID': group_id, 'Members': boys_members, 'Gender': 'Boys'}
            girls_group = {'Group ID': group_id, 'Members': girls_members, 'Gender': 'Girls'}
            group_list = [boys_group, girls_group]
        else:
            group_list = [group]

        for sub_group in group_list:
            sub_group_id = sub_group['Group ID']
            sub_members = sub_group['Members']
            sub_gender = sub_group['Gender']

            for _, room in hostel_df.iterrows():
                if room['Gender'] == sub_gender and room['Capacity'] >= sub_members:
                    allocations.append({
                        'Group ID': sub_group_id,
                        'Hostel Name': room['Hostel Name'],
                        'Room Number': room['Room Number'],
                        'Members Allocated': sub_members
                    })
                    hostel_df.at[room.name, 'Capacity'] -= sub_members
                    break

    return allocations

if __name__ == '__main__':
    app.run(debug=True)
