import reflex as rx
from datetime import date, datetime, timedelta
from sqlmodel import Session, select, create_engine
from reflexdevapp.models import Workout
from reflexdevapp.template import template
from reflexdevapp.components.chart import Chart

engine = create_engine("sqlite:///reflex.db")


def get_week_chart_data():
    today = date.today()
    week_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    calories_by_day = {d: 0.0 for d in week_dates}

    with Session(engine) as session:
        statement = select(Workout).where(
            Workout.date >= datetime.combine(week_dates[0], datetime.min.time())
        )
        results = session.exec(statement).all()

        for workout in results:
            workout_day = workout.date.date()
            if workout_day in calories_by_day:
                calories_by_day[workout_day] += workout.calories

    labels = [str(d) for d in week_dates]
    data = [calories_by_day[d] for d in week_dates]
    return labels, data


@rx.page(route="/graph", title="График")
def graph_page():
    labels, data = get_week_chart_data()

    return template(
        rx.fragment(
            rx.script(src="/assets/chart_component.js", is_raw=True),
            rx.container(
                rx.heading("Калории за последнюю неделю", size="2", mb="4"),
                Chart(labels=labels, data=data),
                rx.hstack(
                    rx.text(f"Всего калорий: {sum(data):.1f}", font_weight="bold"),
                    rx.spacer(),
                    rx.text(f"Среднее в день: {sum(data)/len(data):.1f}", font_weight="bold"),
                    mt="4",
                ),
                max_width="700px",
                mx="auto",
                mt="8",
            )
        )
    )
