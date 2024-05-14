document.addEventListener("DOMContentLoaded", function() {
    const accordionButtons = document.querySelectorAll(".accordion-button");

    accordionButtons.forEach(button => {
        const accordionHeader = button.parentElement;
        const accordionItem = accordionHeader.parentElement;
        const accordionContent = accordionItem.querySelector(".accordion-content");

        button.addEventListener("click", () => {
            const isVisible = accordionContent.style.display === "block";

            closeAllAccordionPanels()

            // Toggle accordion content visibility
            accordionContent.style.display = isVisible ? "none" : "block";

            // Toggle button text
            button.textContent = isVisible ? "Show Forecast" : "Hide Forecast";

            // Draw chart if content is visible
            if (!isVisible) {
                const chartData = JSON.parse(accordionContent.getAttribute("data-chart-data"));
                const chartLabels = JSON.parse(accordionContent.getAttribute("data-chart-labels"));
                drawChart(accordionContent.querySelector("#chartCanvas"), chartLabels, chartData);
            }
        });
    });
});

function drawChart(canvas, labels, data) {
    const ctx = canvas.getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Sales',
                data: data,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
};

function closeAllAccordionPanels() {
    const accordionContents = document.querySelectorAll('.accordion-content');
    const accordionButtons = document.querySelectorAll('.accordion-button');

    accordionContents.forEach(content => {
        content.style.display = 'none';
    });

    accordionButtons.forEach(button => {
        button.textContent = 'Show Forecast';
    });
};
