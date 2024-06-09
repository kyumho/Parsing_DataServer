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

                    data.forEach(event => {
                        const eventTable = document.createElement('table');
                        eventTable.classList.add('event-table');

                        // Event Header
                        const eventHeader = document.createElement('thead');
                        const eventHeaderRow = document.createElement('tr');
                        const eventTitleCell = document.createElement('th');
                        eventTitleCell.colSpan = 4;
                        eventTitleCell.textContent = `${event.home_team} vs ${event.away_team} - ${new Date(event.commence_time).toLocaleString()}`;
                        eventHeaderRow.appendChild(eventTitleCell);
                        eventHeader.appendChild(eventHeaderRow);
                        eventTable.appendChild(eventHeader);

                         // Table Headers
                        const headerRow = document.createElement('tr');
                        const bookmakerHeader = document.createElement('th');
                        bookmakerHeader.textContent = '북메이커';
                        const lastUpdateHeader = document.createElement('th');
                        lastUpdateHeader.textContent = '마지막 업데이트';
                        const teamHeader = document.createElement('th');
                        teamHeader.textContent = '팀';
                        const oddsHeader = document.createElement('th');
                        oddsHeader.textContent = '배당률';

                        headerRow.appendChild(bookmakerHeader);
                        headerRow.appendChild(lastUpdateHeader);
                        headerRow.appendChild(teamHeader);
                        headerRow.appendChild(oddsHeader);
                        eventTable.appendChild(headerRow);

                        // Table Body
                        const tableBody = document.createElement('tbody');

                        event.bookmakers.forEach(bookmaker => {
                            bookmaker.markets.forEach(market => {
                                market.outcomes.forEach(outcome => {
                                    const row = document.createElement('tr');

                                    const bookmakerCell = document.createElement('td');
                                    bookmakerCell.textContent = bookmaker.title;
                                    const lastUpdateCell = document.createElement('td');
                                    lastUpdateCell.textContent = new Date(bookmaker.last_update).toLocaleString();
                                    const teamCell = document.createElement('td');
                                    teamCell.textContent = outcome.name;
                                    const oddsCell = document.createElement('td');
                                    oddsCell.textContent = outcome.price;

                                    row.appendChild(bookmakerCell);
                                    row.appendChild(lastUpdateCell);
                                    row.appendChild(teamCell);
                                    row.appendChild(oddsCell);

                                    tableBody.appendChild(row);
                                });
                            });
                        });

                        eventTable.appendChild(tableBody);
                        resultsDiv.appendChild(eventTable);
                    });
                })
                .catch(error => console.error('Error fetching data:', error));
        } else {
            alert('리그를 선택해주세요.');
        }
    });
});
