document.addEventListener('DOMContentLoaded', () => {
    let currentPage = 1;
    const form = document.getElementById('realEstateForm');
    const resultDiv = document.getElementById('result');
    const regionInput = document.getElementById('region');
    const dealYmdInput = document.getElementById('dealYmd');

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        currentPage = 1;
        fetchRealEstateData();
    });

    regionInput.addEventListener('input', clearResultsAndButtons);
    dealYmdInput.addEventListener('input', clearResultsAndButtons);

    async function fetchRealEstateData() {
        const region = regionInput.value;
        const dealYmd = dealYmdInput.value;

        try {
            const response = await fetch('/real_estate/fetch_real_estate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ region, dealYmd, page: currentPage })
            });
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        }
    }

    function displayResults(data) {
        resultDiv.innerHTML = ''; // 기존 결과 초기화

        if (data.error) {
            resultDiv.innerHTML = `<p>Error: ${data.error}</p>`; // 에러가 있는 경우 에러 메시지 표시
            return;
        }

        if (data.length === 0) {
            resultDiv.innerHTML = `<p>No results found.</p>`; // 결과가 없는 경우 메시지 표시
            return;
        }

        // 결과를 테이블 형태로 표시
        const table = document.createElement('table');
        table.classList.add('result-table');

        // 테이블 헤더 생성
        const headerRow = document.createElement('tr');
        const headers = ['거래금액', '건축년도', '년', '월', '일', '아파트', '전용면적', '층', '법정동', '도로명'];
        headers.forEach(headerText => {
            const headerCell = document.createElement('th');
            headerCell.textContent = headerText;
            headerRow.appendChild(headerCell);
        });
        table.appendChild(headerRow);

        // 테이블 데이터 생성
        data.forEach(item => {
            const row = document.createElement('tr');
            headers.forEach(headerText => {
                const cell = document.createElement('td');
                cell.textContent = item[headerText];
                row.appendChild(cell);
            });
            table.appendChild(row);
        });

        resultDiv.appendChild(table); // 결과 div에 테이블 추가

        // 페이지네이션 버튼 추가
        let paginationDiv = document.getElementById('pagination');
        if (!paginationDiv) {
            paginationDiv = document.createElement('div');
            paginationDiv.id = 'pagination';
            paginationDiv.style.display = 'block';

            const prevButton = document.createElement('button');
            prevButton.id = 'prev';
            prevButton.textContent = '이전';
            prevButton.addEventListener('click', prevPage);

            const nextButton = document.createElement('button');
            nextButton.id = 'next';
            nextButton.textContent = '다음';
            nextButton.addEventListener('click', nextPage);

            paginationDiv.appendChild(prevButton);
            paginationDiv.appendChild(nextButton);

            resultDiv.appendChild(paginationDiv); // 결과 div에 페이지네이션 추가
        } else {
            paginationDiv.style.display = 'block';
        }
    }

    function clearResultsAndButtons() {
        resultDiv.innerHTML = ''; // 기존 결과 초기화
        const paginationDiv = document.getElementById('pagination');
        if (paginationDiv) {
            paginationDiv.style.display = 'none'; // 페이지네이션 버튼 숨기기
        }
    }

    function prevPage() {
        if (currentPage > 1) {
            currentPage--;
            fetchRealEstateData();
        }
    }

    function nextPage() {
        currentPage++;
        fetchRealEstateData();
    }

    // 초기 페이지네이션 버튼 숨기기
    clearResultsAndButtons();
});
