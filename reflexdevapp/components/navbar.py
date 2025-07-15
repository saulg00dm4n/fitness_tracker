import reflex as rx


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text("🏋️‍♂️ Fitness tracker", font_size="2xl", font_weight="bold"),
            rx.spacer(),
            rx.link("Главная", href="/"),
            rx.link("Трекер", href="/tracker", ml="4"),
            rx.link("История", href="/history", ml="4"),
            rx.link("График", href="/graph", ml="4"),
            rx.link("Профиль", href="/profile", ml="4"),
        ),
        w="100%",
        p="4",
        bg="transparent",
        position="sticky",
        top="0",
        box_shadow="sm",
    )
