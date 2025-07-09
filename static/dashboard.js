// dashboard.js

function loadPage(section) {
  const content = document.getElementById('content');
  content.innerHTML = "<p>Loading...</p>";

  fetch(`/dashboard/${section}`)
    .then(res => {
      if (!res.ok) throw new Error("Page load failed");
      return res.text();
    })
    .then(html => {
      content.innerHTML = html;
    })
    .catch(err => {
      content.innerHTML = `<p>Error loading section: ${section}</p>`;
      console.error(err);
    });
}

