const API_URL = "http://127.0.0.1:5000";


function setQuestion(question) {

    document.getElementById("question").value = question;

}


async function askQuestion() {

    const question =
        document.getElementById("question").value.trim();

    const loading =
        document.getElementById("loading");

    const error =
        document.getElementById("error");

    const querySection =
        document.getElementById("query-section");

    const resultSection =
        document.getElementById("result-section");


    if (!question) {

        error.textContent =
            "Please enter a question.";

        error.classList.remove("hidden");

        return;
    }


    error.classList.add("hidden");

    querySection.classList.add("hidden");

    resultSection.classList.add("hidden");

    loading.classList.remove("hidden");


    try {

        const response = await fetch(
            `${API_URL}/ask`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.error || "Something went wrong"
            );

        }


        // Show generated query

        document.getElementById("query").textContent =
            JSON.stringify(
                data.query,
                null,
                2
            );

        querySection.classList.remove("hidden");


        // Show results

        displayResults(data.result);

        resultSection.classList.remove("hidden");


    } catch (err) {

        error.textContent =
            err.message;

        error.classList.remove("hidden");

    }


    loading.classList.add("hidden");
}


function displayResults(result) {

    const resultDiv =
        document.getElementById("result");


    // Count result

    if (result.type === "count") {

        resultDiv.innerHTML =
            `<h3>Total: ${result.count}</h3>`;

        return;
    }


    // Data result

    if (
        result.type === "data" &&
        result.results.length > 0
    ) {

        const data = result.results;

        const columns =
            Object.keys(data[0]);


        let html = "<table>";

        html += "<thead><tr>";


        columns.forEach(column => {

            html += `<th>${column}</th>`;

        });


        html += "</tr></thead>";

        html += "<tbody>";


        data.forEach(row => {

            html += "<tr>";


            columns.forEach(column => {

                html += `<td>${row[column]}</td>`;

            });


            html += "</tr>";

        });


        html += "</tbody>";

        html += "</table>";


        resultDiv.innerHTML = html;

    } else {

        resultDiv.innerHTML =
            "<p>No results found.</p>";

    }

}