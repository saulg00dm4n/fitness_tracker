import reflex as rx
from reflexdevapp.template import template
from reflexdevapp.state import TrackerState


@rx.page(route="/history", title="История тренировок")
def history_page() -> rx.Component:
    return rx.fragment(
        rx.html("""<link rel="stylesheet" href="/styles.css">"""),

        template(
            rx.container(
                rx.hstack(
                    rx.select(
                        items=["Все", "Бег", "Велосипед", "Силовая"],
                        value=TrackerState.filter_type,
                        on_change=TrackerState.set_filter_type,
                        placeholder="Тип тренировки",
                    ),
                    rx.select(
                        items=["Дата ↓", "Дата ↑", "Калории ↓", "Калории ↑"],
                        value=TrackerState.sort_option,
                        on_change=TrackerState.set_sort_option,
                        placeholder="Сортировка",
                    ),
                    spacing="4",
                    mb="4",
                ),

                rx.heading("История тренировок", size="4", mb="4"),

                rx.cond(
                    TrackerState.page_workouts,
                    rx.vstack(
                        rx.foreach(
                            TrackerState.page_workouts,
                            lambda w: rx.card(
                                rx.vstack(
                                    rx.text(w["date"], font_weight="semibold", color="gray.600"),
                                    rx.text(f"Тип: {w['type']}", color="blue.700"),
                                    rx.text(
                                        f"Длительность: {w['duration_minutes']} мин {w['duration_seconds']} сек",
                                        color="blue.700"
                                    ),
                                    rx.text(f"Сожжено: {w['calories']} ккал", color="blue.700"),
                                    rx.button(
                                        "Удалить",
                                        color_scheme="red",
                                        variant="outline",
                                        size="2",
                                        mt="2",
                                        on_click=lambda: TrackerState.delete_workout(w["id"])
                                    ),
                                ),
                                padding="4",
                                mb="3",
                                border_radius="lg",
                                box_shadow="md",
                                class_name=f"card-animate type-{w['type']}"
                            )
                        ),
                        spacing="3",
                        align="stretch",
                    ),
                    rx.text("Нет записей тренировок.", color="gray.500"),
                ),

                rx.hstack(
                    rx.button("Назад", on_click=TrackerState.prev_page, is_disabled=TrackerState.current_page <= 1),
                    rx.text(TrackerState.page_label),
                    rx.button("Вперёд", on_click=TrackerState.next_page, is_disabled=TrackerState.current_page >= TrackerState.total_pages),
                    justify="center",
                    mt="4",
                ),

                max_width="600px",
                mx="auto",
                mt="6",
            )
        )
    )
