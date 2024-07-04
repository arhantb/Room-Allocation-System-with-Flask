document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData(this);

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.json()).then(data => {
        let results = document.getElementById('results');
        results.innerHTML = '';

        if (data.error) {
            results.innerText = data.error;
            return;
        }

        let table = document.createElement('table');
        let headers = ['Group ID', 'Hostel Name', 'Room Number', 'Members Allocated'];
        let headerRow = document.createElement('tr');
        headers.forEach(header => {
            let th = document.createElement('th');
            th.innerText = header;
            headerRow.appendChild(th);
        });
        table.appendChild(headerRow);

        data.forEach(row => {
            let tr = document.createElement('tr');
            headers.forEach(key => {
                let td = document.createElement('td');
                td.innerText = row[key];
                tr.appendChild(td);
            });
            table.appendChild(tr);
        });
        results.appendChild(table);
    }).catch(error => {
        console.error('Error:', error);
    });
});
