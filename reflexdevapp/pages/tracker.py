import reflex as rx
from reflexdevapp.state import TrackerState
from reflexdevapp.template import template


@rx.page(route="/tracker", title="Трекер", on_load=TrackerState.load_profile_weight)
def tracker_page() -> rx.Component:
    return template(
        rx.container(
            rx.vstack(
                rx.heading("Персональный Фитнес‑Трекер", size="1", mb="4"),

                rx.cond(
                    TrackerState.message != "",
                    rx.box(
                        rx.text(
                            TrackerState.message,
                            color="white",
                            font_weight="medium"
                        ),
                        p="3",
                        mb="4",
                        border_radius="md",
                        bg=rx.cond(
                            TrackerState.message.startswith("❌"),
                            "red.500",
                            "green.500",
                        ),
                    ),
                ),

                rx.card(
                    rx.form(
                        rx.vstack(
                            rx.select(
                                items=["Бег", "Велосипед", "Силовая"],
                                placeholder="Тип тренировки",
                                value=TrackerState.workout_type,
                                on_change=TrackerState.set_workout_type,
                                mb="3",
                            ),
                            rx.input(
                                type_="number",
                                placeholder="Минуты",
                                value=TrackerState.duration_minutes,
                                on_change=TrackerState.set_duration_minutes,
                                mb="3",
                            ),
                            rx.input(
                                type_="number",
                                placeholder="Секунды",
                                value=TrackerState.duration_seconds,
                                on_change=TrackerState.set_duration_seconds,
                                mb="3",
                            ),
                            rx.input(
                                type_="number",
                                placeholder="Вес (кг)",
                                default_value=TrackerState.weight,
                                on_change=TrackerState.set_weight,
                                mb="3",
                            ),
                            rx.button(
                                "Добавить тренировку",
                                type_="submit",
                                color_scheme="blue",
                                width="full",
                            ),
                        ),
                        on_submit=TrackerState.add_workout,
                        spacing="4",
                    ),
                    box_shadow="lg",
                    border_radius="xl",
                    p="6",
                    mb="6",
                ),

                rx.button(
                    "Скачать CSV",
                    on_click=TrackerState.export_csv,
                    color_scheme="green",
                    variant="solid",
                    mt="4",
                ),
            ),
            max_width="600px",
            mx="auto",
            mt="8",
            mb="8",
        )
    )
