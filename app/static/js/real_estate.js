document.getElementById('realEstateForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const region = document.getElementById('region').value;
    const dealYmd = document.getElementById('dealYmd').value;

    fetch('/real_estate/fetch_real_estate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({region, dealYmd})
    })
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').innerHTML = `<p>Error: ${error.message}</p>`;
        });
});

function displayResults(data) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';

    if (data.error) {
        resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        return;
    }

    const table = document.createElement('table');
    table.classList.add('result-table');

    const headerRow = document.createElement('tr');
    const headers = ['거래금액', '건축년도', '년', '월', '일', '아파트', '전용면적', '층', '법정동', '도로명'];
    headers.forEach(headerText => {
        const headerCell = document.createElement('th');
        headerCell.textContent = headerText;
        headerRow.appendChild(headerCell);
    });
    table.appendChild(headerRow);

    data.forEach(item => {
        const row = document.createElement('tr');
        headers.forEach(headerText => {
            const cell = document.createElement('td');
            cell.textContent = item[headerText];
            row.appendChild(cell);
        });
        table.appendChild(row);
    });

    resultDiv.appendChild(table);
}
