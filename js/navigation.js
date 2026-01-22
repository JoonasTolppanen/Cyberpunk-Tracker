document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".menu-button");
    const content = document.getElementById("content");

    function loadPage(page) {
        fetch(page)
            .then(res => {
                if (!res.ok) throw new Error("Fetch failed");
                return res.text();
            })
            .then(html => {
                content.innerHTML = html;
            })
            .catch(() => {
                content.innerHTML = "<h1>Error loading page</h1>";
            });
    }

    function setActive(hash) {
        buttons.forEach(btn => {
            btn.classList.toggle("active", btn.getAttribute("href") === hash);
        });
    }

    // Handle menu clicks
    buttons.forEach(button => {
        button.addEventListener("click", e => {
            e.preventDefault();

            const page = button.dataset.page;
            const hash = button.getAttribute("href");

            loadPage(page);
            setActive(hash);

            location.hash = hash;
        });
    });

    // Handle direct load & back/forward
    function handleHashChange() {
        const hash = location.hash || "#bio";
        const activeBtn = document.querySelector(`a[href="${hash}"]`);

        if (activeBtn) {
            loadPage(activeBtn.dataset.page);
            setActive(hash);
        }
    }

    window.addEventListener("hashchange", handleHashChange);

    // Initial load
    handleHashChange();
});
