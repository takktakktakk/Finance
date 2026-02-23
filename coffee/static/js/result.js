document.addEventListener("DOMContentLoaded", function () {

    const ctx = document.getElementById("tasteChart");
    if (!ctx) return;

    new Chart(ctx, {
        type: "radar",
        data: {
            labels: [
                "acidity",
                "sweetness",
                "bitterness",
                "flavor",
                "aroma",
                "body",
                "after taste",
                "balance"
            ],
            datasets: [{
                label: "Taste Balance",
                data: [
                    recipe.acidity,
                    recipe.sweetness,
                    recipe.bitterness,
                    recipe.flavor,
                    recipe.aroma,
                    recipe.body,
                    recipe.after_taste,
                    recipe.balance
                ],
                fill: true,
                backgroundColor: "rgba(111, 78, 55, 0.25)",  // 薄いブラウン
                borderColor: "#6f4e37",                      // コーヒーブラウン
                pointBackgroundColor: "#6f4e37",
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                r: {
                    min: 0,
                    max: 5,
                    ticks: {
                        stepSize: 1,
                        backdropColor: "transparent",
                        color: "#6f4e37"
                    },
                    grid: {
                        color: "rgba(111, 78, 55, 0.2)"
                    },
                    angleLines: {
                        color: "rgba(111, 78, 55, 0.2)"
                    },
                    pointLabels: {
                        color: "#6f4e37",
                        font: {
                            size: 12,
                            weight: "bold"
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });

});