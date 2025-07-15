import reflex as rx


def footer() -> rx.Component:
    return rx.box(
        rx.text("©2025 Miigaik corp.", font_size="sm", color="gray.600"),
        padding="4",
        text_align="center",
        bg="gray.50"
    )
