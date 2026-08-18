document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("noteLiveSearch");
    const resultsContainer = document.getElementById("liveSearchResults");
    if (!searchInput || !resultsContainer) {
        return;
    }
    let timeout = null;
    searchInput.addEventListener("input", function () {
        clearTimeout(timeout);
        const query = this.value.trim();
        if (query.length === 0) {
            resultsContainer.innerHTML = "";
            resultsContainer.classList.add("d-none");
            return;
        }
        timeout = setTimeout(() => {
            fetch( `/notes/live-search/?q=${encodeURIComponent(query)}` )
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = "";
                if (data.results.length === 0) {
                    resultsContainer.innerHTML = ` <div class="p-3 text-muted"> No notes found.</div> `;
                } else {
                    data.results.forEach(note => {
                        const item = document.createElement("a");
                        item.href = note.url;
                        item.className = "list-group-item list-group-item-action";
                        item.innerHTML = `
                            <div class="fw-bold">  ${escapeHTML(note.title)} </div>
                            <small class="text-muted">  ${escapeHTML(note.content)} </small>
                            ${
                                note.category
                                ? `
                                <div class="mt-1"><span class="badge bg-primary"> ${escapeHTML(note.category)} </span> </div>`
                                : ""
                            } `;
                        resultsContainer.appendChild(item);
                    });
                }
                resultsContainer.classList.remove("d-none");
            })
            .catch(error => { console.error( "Live search error:",error); });
        }, 300);
    });
    document.addEventListener("click", function (event) {
        if (!searchInput.contains(event.target) &&!resultsContainer.contains(event.target) ) {
            resultsContainer.classList.add("d-none");
        }
    });
    function escapeHTML(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }
});