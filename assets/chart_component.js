// assets/chart_component.js

const script = document.createElement("script");
script.src = "https://cdn.jsdelivr.net/npm/chart.js";
script.onload = () => {
    window.renderChart = function (id, labels, data, type = "bar") {
        const ctx = document.getElementById(id)?.getContext("2d");
        if (!ctx || !window.Chart) {
            console.error("Canvas context or Chart.js not loaded");
            return;
        }

        // Удаление старого графика
        if (!window._charts) window._charts = {};
        if (window._charts[id]) window._charts[id].destroy();

        const darkTheme = document.documentElement.classList.contains("dark");

        // Градиентная цветовая шкала
        const getColor = (value) => {
            if (value < 500) return "rgba(144, 238, 144, 0.7)"; // lightgreen
            if (value < 1500) return "rgba(255, 230, 100, 0.8)"; // yellow
            if (value < 3000) return "rgba(255, 165, 0, 0.8)";   // orange
            return "rgba(255, 99, 132, 0.8)"; // red
        };

        const backgroundColors = data.map(getColor);

        const chart = new Chart(ctx, {
            type: type,
            data: {
                labels: labels,
                datasets: [{
                    label: "Калории",
                    data: data,
                    backgroundColor: backgroundColors,
                    borderColor: "rgba(0,0,0,0.1)",
                    borderWidth: 1,
                    tension: 0.3,
                }]
            },
            options: {
                responsive: true,
                animation: {
                    duration: 800,
                    easing: 'easeOutQuart',
                },
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            color: darkTheme ? "white" : "black",
                        }
                    },
                    tooltip: {
                        backgroundColor: darkTheme ? "#333" : "#fff",
                        titleColor: darkTheme ? "#fff" : "#000",
                        bodyColor: darkTheme ? "#ddd" : "#222"
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: darkTheme ? "#aaa" : "#333",
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: darkTheme ? "#aaa" : "#333",
                        }
                    }
                }
            }
        });

        window._charts[id] = chart;

        // Добавим кнопку PNG
        const exportBtnId = id + "_export_btn";
        if (!document.getElementById(exportBtnId)) {
            const btn = document.createElement("button");
            btn.textContent = "Сохранить график (PNG)";
            btn.id = exportBtnId;
            btn.style.marginTop = "12px";
            btn.style.display = "block";
            btn.style.background = "#3b82f6";
            btn.style.color = "white";
            btn.style.border = "none";
            btn.style.padding = "8px 12px";
            btn.style.borderRadius = "6px";
            btn.style.cursor = "pointer";

            ctx.canvas.parentNode.appendChild(btn);

            btn.addEventListener("click", () => {
                const link = document.createElement("a");
                link.href = chart.toBase64Image();
                link.download = "chart.png";
                link.click();
            });
        }
    };
};
document.head.appendChild(script);
