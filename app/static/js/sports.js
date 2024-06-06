document.addEventListener('DOMContentLoaded', (event) => {
    const dropdownButton = document.querySelector('.dropdown-button');
    const dropdownContent = document.querySelector('.dropdown-content');
    const fetchDataButton = document.getElementById('fetch-data');

    let selectedLeague = null;

    dropdownContent.addEventListener('click', (e) => {
        if (e.target.tagName === 'A') {
            selectedLeague = e.target.getAttribute('data-league');
            dropdownButton.textContent = e.target.textContent;
        }
    });

    fetchDataButton.addEventListener('click', () => {

        if (selectedLeague) {
            fetch(`/sports/fetch-odds?league=${selectedLeague}`)
                .then(response => response.json())
                .then(data => {
                    const resultsDiv = document.getElementById('results');
                    resultsDiv.innerHTML = '';
                    data.forEach(item => {
                        const resultItem = document.createElement('div');
                        resultItem.classList.add('result-item');
                        resultItem.textContent = `${item.team}: ${item.probability}`;
                        resultsDiv.appendChild(resultItem);
                    });
                })
                .catch(error => console.error('Error fetching data:', error));
        } else {
            alert('Please select a league and specify start and end dates.');
        }
    });
});
