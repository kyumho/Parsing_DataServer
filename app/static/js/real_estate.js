document.getElementById('realEstateForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const region = document.getElementById('region').value;
    const dealYmd = document.getElementById('dealYmd').value;

    fetch('/real_estate/fetch_real_estate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ region, dealYmd })
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById('result');
        if (data.error) {
            resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `<p>총 매물: ${data.total_properties}</p>
                                   <p>평균 가격: ${data.average_price}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = `<p>Error: ${error}</p>`;
    });
});
