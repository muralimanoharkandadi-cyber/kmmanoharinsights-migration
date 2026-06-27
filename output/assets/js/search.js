let searchIndex = [];

async function loadSearch() {

    const response = await fetch("/search-index.json");
    searchIndex = await response.json();

}

function renderResults(results) {

    const container = document.getElementById("articles");

    if (!container) return;

    container.innerHTML = "";

    results.forEach(article => {

        const labels = article.labels.join(" • ");

        container.innerHTML += `
<article class="post-card">

<h2>
<a href="${article.slug}/">
${article.title}
</a>
</h2>

<p class="post-summary">
${article.summary}
</p>

<p class="post-meta">

${labels}

</p>

</article>
`;

    });

}

function searchArticles() {

    const q = document
        .getElementById("search")
        .value
        .toLowerCase()
        .trim();

    if (!q) {
        renderResults(searchIndex);
        return;
    }

    const results = searchIndex.filter(article =>

        article.title.toLowerCase().includes(q) ||

        article.summary.toLowerCase().includes(q) ||

        article.labels.join(" ").toLowerCase().includes(q)

    );

    renderResults(results);

}

loadSearch().then(() => {

    renderResults(searchIndex);

});