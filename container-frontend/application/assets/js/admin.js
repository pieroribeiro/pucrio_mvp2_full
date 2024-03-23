document.addEventListener('DOMContentLoaded', function() {
    // Function to fetch data from API and populate the table
    function fetchData(page = 1, search = '') {
        // Simulate fetching data from API with pagination and search filter
        // Replace this with your actual API endpoint
        const apiUrl = `https://api.example.com/quotes?page=${page}&search=${search}`;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById('table-body');
                const pagination = document.getElementById('pagination');

                // Clear previous table content
                tableBody.innerHTML = '';

                // Populate table with fetched data
                data.quotes.forEach(quote => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                    <td>${quote.currency}</td>
                    <td>${quote.value}</td>
                    <td>
                    <button class="btn btn-sm btn-primary me-1" onclick="editQuote(${quote.id})">Editar</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteQuote(${quote.id})">Excluir</button>
                    </td>
                    `;
                    tableBody.appendChild(row);
                });

                // Populate pagination links
                pagination.innerHTML = '';
                for (let i = 1; i <= data.totalPages; i++) {
                    const li = document.createElement('li');
                    li.classList.add('page-item');
                    const link = document.createElement('a');
                    link.classList.add('page-link');
                    link.href = '#';
                    link.textContent = i;
                    link.addEventListener('click', () => fetchData(i, search));
                    li.appendChild(link);
                    pagination.appendChild(li);
                }
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Initial fetch with page 1 and no search filter
    fetchData();

    // Search button click event
    const searchButton = document.getElementById('button-search');
    searchButton.addEventListener('click', () => {
        const searchTerm = document.querySelector('.form-control').value.trim();
        fetchData(1, searchTerm);
    });
});

// Function to simulate editing a quote
function editQuote(id) {
    // Simulate fetching quote data from API
    const apiUrl = `https://api.example.com/quotes/${id}`;
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // Populate edit quote modal with fetched data
            document.getElementById('editCurrency').value = data.currency;
            document.getElementById('editValue').value = data.value;
            document.getElementById('editQuoteId').value = data.id;
            // Show edit quote modal
            const editQuoteModal = new bootstrap.Modal(document.getElementById('editQuoteModal'), { backdrop: 'static' });
            editQuoteModal.show();
        })
        .catch(error => console.error('Error fetching quote data:', error));
}

// Function to simulate saving edited quote
function saveEditedQuote() {
    // Simulate saving edited quote to API
    const id = document.getElementById('editQuoteId').value;
    const currency = document.getElementById('editCurrency').value;
    const value = document.getElementById('editValue').value;
    console.log('Saving edited quote:', { id, currency, value });
    // Simulate closing modal after saving
    const editQuoteModal = new bootstrap.Modal(document.getElementById('editQuoteModal'));
    editQuoteModal.hide();
}

// Function to simulate deleting a quote
function deleteQuote(id) {
    // Simulate showing a confirmation dialog and then deleting the quote
    if (confirm('Tem certeza que deseja excluir esta cotação?')) {
        // Simulate sending delete request to API
        console.log('Deleting quote with ID:', id);
    }
}

// Function to simulate adding a quote
function addQuote() {
    // Simulate adding quote to API
    const currency = document.getElementById('addCurrency').value;
    const value = document.getElementById('addValue').value;
    console.log('Adding quote:', { currency, value });
    // Simulate closing modal after adding
    const addQuoteModal = new bootstrap.Modal(document.getElementById('addQuoteModal'));
    addQuoteModal.hide();
}
