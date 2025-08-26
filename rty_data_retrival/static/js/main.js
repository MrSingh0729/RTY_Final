document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Toggle
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
    
    // Initialize Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.classList.add('fade');
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });
    
    // Format numbers with commas
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
    
    // Format percentage
    function formatPercentage(value) {
        return parseFloat(value).toFixed(2) + '%';
    }
    
    // Update last updated time
    function updateLastUpdatedTime() {
        const now = new Date();
        const timeString = now.getHours().toString().padStart(2, '0') + ':' + 
                          now.getMinutes().toString().padStart(2, '0');
        const lastUpdatedElement = document.getElementById('last-updated');
        if (lastUpdatedElement) {
            lastUpdatedElement.textContent = timeString;
        }
    }
    
    updateLastUpdatedTime();
    setInterval(updateLastUpdatedTime, 60000); // Update every minute
    
    // Handle form submissions with loading indicator
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
            }
        });
    });
    
    // Initialize DataTables with common options
    function initDataTables() {
        // Check if DataTables are already initialized and destroy them
        const dataTables = document.querySelectorAll('table[id$="Table"]');
        dataTables.forEach(function(table) {
            if ($.fn.DataTable.isDataTable(table)) {
                $(table).DataTable().destroy();
            }
            
            $(table).DataTable({
                responsive: true,
                pageLength: 10,
                lengthMenu: [ [10, 25, 50, 100], [10, 25, 50, 100] ],
                dom: '<"row"<"col-sm-6"l><"col-sm-6"f>>' +
                     '<"row"<"col-sm-12"tr>>' +
                     '<"row"<"col-sm-5"i><"col-sm-7"p>>',
                language: {
                    search: "_INPUT_",
                    searchPlaceholder: "Search records..."
                },
                destroy: true
            });
        });
    }
    
    // Initialize DataTables on page load
    initDataTables();
    
    // Handle export buttons
    const exportButtons = document.querySelectorAll('.export-btn');
    exportButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const format = this.getAttribute('data-format');
            const url = this.getAttribute('data-url');
            
            if (format && url) {
                window.location.href = url + '&format=' + format;
            }
        });
    });
    
    // Handle date range pickers
    const dateRangePickers = document.querySelectorAll('.date-range-picker');
    dateRangePickers.forEach(function(picker) {
        $(picker).daterangepicker({
            opens: 'left',
            locale: {
                format: 'YYYY-MM-DD'
            }
        });
    });
    
    // Handle datetime-local inputs
    const datetimeInputs = document.querySelectorAll('input[type="datetime-local"]');
    datetimeInputs.forEach(function(input) {
        const now = new Date();
        const localDateTime = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
                                .toISOString().slice(0, 16);
        input.setAttribute('max', localDateTime);
    });
    
    // Initialize charts if Chart.js is available
    if (typeof Chart !== 'undefined') {
        // Chart default options
        Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
        Chart.defaults.color = '#6c757d';
        
        // Create a chart for each canvas with 'chart' in its ID
        const chartCanvases = document.querySelectorAll('canvas[id*="chart"]');
        chartCanvases.forEach(function(canvas) {
            const ctx = canvas.getContext('2d');
            const chartType = canvas.getAttribute('data-chart-type') || 'line';
            
            // This is a placeholder - actual chart implementation would depend on the specific use case
            new Chart(ctx, {
                type: chartType,
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'Dataset',
                        data: [12, 19, 3, 5, 2, 3],
                        backgroundColor: 'rgba(67, 97, 238, 0.2)',
                        borderColor: 'rgba(67, 97, 238, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        });
    }
    
    // Handle confirmation dialogs
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
    
    // Handle file uploads
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const fileName = this.files[0]?.name || 'No file selected';
            const label = this.nextElementSibling;
            if (label && label.classList.contains('custom-file-label')) {
                label.textContent = fileName;
            }
        });
    });
});