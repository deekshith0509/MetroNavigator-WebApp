document.addEventListener('DOMContentLoaded', function() {
    // Station search functionality
    function setupStationSearch(selectId) {
        const select = document.getElementById(selectId);
        if (!select) return;

        const wrapper = document.createElement('div');
        wrapper.className = 'relative';
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.className = 'form-input w-full';
        searchInput.placeholder = 'Search stations...';

        select.parentNode.insertBefore(wrapper, select);
        wrapper.appendChild(searchInput);
        wrapper.appendChild(select);

        searchInput.addEventListener('input', function(e) {
            const searchText = e.target.value.toLowerCase();
            Array.from(select.options).forEach(option => {
                if (option.value === '') return; // Skip placeholder option
                const match = option.text.toLowerCase().includes(searchText);
                option.style.display = match ? '' : 'none';
            });
        });
    }

    setupStationSearch('source');
    setupStationSearch('destination');

    // Form validation
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const source = document.getElementById('source').value;
            const destination = document.getElementById('destination').value;

            if (source === destination) {
                e.preventDefault();
                alert('Please select different stations for source and destination');
            }
        });
    }
});
