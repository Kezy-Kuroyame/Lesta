// Сортировка таблиц
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.sortable').forEach(header => {
        header.addEventListener('click', function() {
            const table = this.closest('table');
            const columnIndex = this.cellIndex;
            const rows = Array.from(table.querySelectorAll('tbody tr'));
            const direction = this.classList.contains('asc') ? -1 : 1;

            // Сброс сортировки для других колонок
            table.querySelectorAll('.sortable').forEach(h => {
                h.classList.remove('asc', 'desc');
            });

            // Установка направления
            this.classList.toggle('asc', !this.classList.contains('asc'));
            this.classList.toggle('desc', direction === 1);

            // Сортировка
            rows.sort((a, b) => {
                const aVal = a.cells[columnIndex].textContent.trim();
                const bVal = b.cells[columnIndex].textContent.trim();
                return (isNaN(aVal) ?
                        aVal.localeCompare(bVal) :
                        parseFloat(aVal) - parseFloat(bVal)) * direction;
            });

            // Обновление таблицы
            const tbody = table.querySelector('tbody');
            rows.forEach(row => tbody.appendChild(row));
        });
    });
});