import reflex as rx
from reflexdevapp.state import UserProfileState
from reflexdevapp.template import template


@rx.page(route="/profile", title="Профиль пользователя")
def profile_page() -> rx.Component:
    return template(
        rx.container(
            rx.vstack(
                rx.heading("Профиль пользователя"),
                rx.text("Введите ваш вес (кг), чтобы он подставлялся автоматически в трекере."),
                rx.input(
                    placeholder="Вес (кг)",
                    value=UserProfileState.profile_weight,
                    on_change=UserProfileState.set_profile_weight,
                    input_mode="decimal"
                ),
                rx.button("Сохранить", on_click=UserProfileState.save_profile),
                spacing="4",
                align="start",
                padding="4",
            )
        )
    )
