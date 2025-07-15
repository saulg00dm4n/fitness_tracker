import reflex as rx


def Chart(labels: list[str], data: list[float], chart_id: str = "weeklyCaloriesChart") -> rx.Component:
    return rx.fragment(
        rx.html(f'<canvas id="{chart_id}"></canvas>'),
        rx.script(
            f"""
            setTimeout(function() {{
                console.log("Calling renderChart with:", {labels}, {data});
                if (window.renderChart) {{
                    window.renderChart("{chart_id}", {labels}, {data}, "bar");
                }} else {{
                    console.error("renderChart is not defined");
                }}
            }}, 500);
            """,
            is_raw=True
        )
    )
