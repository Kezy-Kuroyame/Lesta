document.addEventListener('DOMContentLoaded', function() {
    // Элементы DOM
    const addFileBtn = document.getElementById('add-file-btn');
    const fileInput = document.getElementById('file-input');
    const uploadForm = document.getElementById('upload-form');
    const analyzeBtn = document.getElementById('analyze-btn');

    // 1. Обработка добавления файлов
    if (addFileBtn && fileInput) {
        addFileBtn.addEventListener('click', function() {
            fileInput.click();
        });

        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                uploadForm.submit();
            }
        });
    }

    // 2. Обработка удаления файлов
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const fileItem = this.closest('.file-item');
            const fileIndex = fileItem.dataset.fileIndex;

            // Создаем скрытую форму для отправки
            const form = document.createElement('form');
            form.method = 'post';
            form.action = '';

            // Добавляем CSRF токен
            const csrf = document.createElement('input');
            csrf.type = 'hidden';
            csrf.name = 'csrfmiddlewaretoken';
            csrf.value = document.querySelector('[name=csrfmiddlewaretoken]').value;
            form.appendChild(csrf);

            // Добавляем индекс файла
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'delete_file';
            input.value = fileIndex;
            form.appendChild(input);

            // Отправляем форму
            document.body.appendChild(form);
            form.submit();
        });
    });
    
    // 3. Обновление состояния кнопки "Анализировать"
    function updateAnalyzeButton() {
        if (analyzeBtn) {
            const fileCount = document.querySelectorAll('.file-item').length;
            analyzeBtn.textContent = `Анализировать (${fileCount}/10)`;
            analyzeBtn.disabled = fileCount < 2;
        }
    }
    
    updateAnalyzeButton();
});