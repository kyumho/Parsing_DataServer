async function searchNews() {
    const query = document.getElementById('query').value;
    if (query) {
        const response = await fetch('/news/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({query})
        });
        const data = await response.json();
        displayResults(data);
    }
}

function displayResults(data) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = ''; // Clear previous results

    if (data.length > 0) {
        data.forEach(item => {
            const newsItem = document.createElement('div');
            newsItem.className = 'news-item';

            const newsTitle = document.createElement('h2');
            newsTitle.className = 'news-title';
            newsTitle.innerHTML = item.title; // Use innerHTML to display HTML entities correctly
            newsItem.appendChild(newsTitle);

            const newsDescription = document.createElement('p');
            newsDescription.className = 'news-description';
            newsDescription.textContent = item.description;
            newsItem.appendChild(newsDescription);

            const newsLink = document.createElement('a');
            newsLink.className = 'news-link';
            newsLink.href = item.link;
            newsLink.textContent = '자세히 보기';
            newsLink.target = '_blank';
            newsItem.appendChild(newsLink);

            resultsContainer.appendChild(newsItem);
        });
    } else {
        resultsContainer.innerHTML = '<p>검색 결과가 없습니다.</p>';
    }
}

