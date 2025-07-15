import reflex as rx
from reflexdevapp.template import template


@rx.page("/", title="Главная")
def index_page() -> rx.Component:
    return template(
        rx.center(
            rx.vstack(
                rx.heading("Добро пожаловать!", size="1"),
                rx.text("Это персональный фитнес‑трекер на Reflex.", font_size="2"),
                rx.text(
                    "Следите за тренировками, рассчитывайте калории и экспортируйте данные в CSV.",
                    font_size="3",
                    mt="2",
                    text_align="center",
                ),
                rx.button(
                    "Перейти к трекеру",
                    on_click=rx.redirect("/tracker"),
                    size="2",
                    color_scheme="green",
                    mt="4",
                ),
            ),
            min_h="100vh",
        )
    )
