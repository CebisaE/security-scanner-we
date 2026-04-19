document.addEventListener("DOMContentLoaded", function () {

    function scanWebsite() {

        let url = document.getElementById("url").value;
        let output = document.getElementById("output");
        let loading = document.getElementById("loading");

        loading.style.display = "block";
        output.innerHTML = "";

        fetch("/scan", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "url=" + encodeURIComponent(url)
        })
        .then(response => response.text())
        .then(data => {
            loading.style.display = "none";
            output.innerHTML = data;
            loadHistory();
        });
    }

    function loadHistory() {
        fetch("/history")
            .then(res => res.json())
            .then(data => {
                let list = document.getElementById("historyList");

                if (!list) return;

                list.innerHTML = "";

                data.history.forEach(item => {
                    let li = document.createElement("li");
                    li.innerHTML = item;
                    list.appendChild(li);
                });
            });
    }

    // expose function globally for button click
    window.scanWebsite = scanWebsite;

    loadHistory();
});