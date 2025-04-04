document.addEventListener("DOMContentLoaded", function () {
    const paginationLinks = document.querySelectorAll(".page-link-custom");

    paginationLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            const filename = this.getAttribute("data-filename");
            const page = this.getAttribute("data-page");

            // Получаем текущий URL и параметры
            const urlParams = new URLSearchParams(window.location.search);

            // Устанавливаем новую страницу для конкретного файла
            urlParams.set(`page_${filename}`, page);

            // Перенаправляем с обновлёнными параметрами
            window.location.search = urlParams.toString();
        });
    });
});