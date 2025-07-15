import reflex as rx
from reflexdevapp.components import navbar, footer


def template(page: rx.Component) -> rx.Component:
    return rx.fragment(
        rx.script(src="https://cdn.jsdelivr.net/npm/chart.js"),
        rx.script(src="/chart_component.js"),
        rx.vstack(
            navbar.navbar(),
            rx.container(page, max_width="800px", padding_y="8"),
            footer.footer(),
            min_h="100vh"
        )
    )
