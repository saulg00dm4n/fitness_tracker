import reflex as rx
from datetime import datetime
from reflexdevapp.models import Workout, UserProfile
from sqlmodel import select
import io
import csv


class TrackerState(rx.State):
    workout_type: str = ""
    duration_minutes: str = ""
    duration_seconds: str = ""
    weight: str = ""
    message: str = ""
    workouts: list[Workout] = []

    filter_type: str = "Все"
    sort_option: str = "Дата ↓"

    current_page: int = 1
    page_size: int = 5

    def calculate_calories(self, type: str, duration_min: float, weight_kg: float) -> float:
        met_values = {"бег": 9.8, "велосипед": 8.5, "силовая": 6.0}
        met = met_values.get(type.lower(), 5.0)
        duration_hr = duration_min / 60
        return round(met * weight_kg * duration_hr, 1)

    def set_duration_minutes(self, value: str): self.duration_minutes = value
    def set_duration_seconds(self, value: str): self.duration_seconds = value
    def set_weight(self, value: str): self.weight = value
    def set_workout_type(self, value: str): self.workout_type = value

    def add_workout(self):
        if not self.workout_type:
            self.message = "❌ Укажите тип тренировки"
            return

        try:
            minutes = int(self.duration_minutes) if self.duration_minutes else 0
            seconds = int(self.duration_seconds) if self.duration_seconds else 0
            if not (0 <= seconds < 60):
                self.message = "❌ Секунды должны быть от 0 до 59"
                return
        except ValueError:
            self.message = "❌ Некорректные данные"
            return

        if minutes == 0 and seconds == 0:
            self.message = "❌ Укажите длительность больше 0"
            return

        with rx.session() as session:
            if self.weight:
                weight = float(self.weight)
            else:
                profile = session.exec(select(UserProfile)).first()
                weight = profile.weight if profile else 0.0

            if weight <= 0:
                self.message = "❌ Укажите корректный вес"
                return

            total_minutes = minutes + seconds / 60
            calories = self.calculate_calories(self.workout_type, total_minutes, weight)

            workout = Workout(
                type=self.workout_type,
                duration=round(total_minutes, 2),
                calories=calories,
                date=datetime.now(),
                weight=weight,
            )

            session.add(workout)
            session.commit()
            session.refresh(workout)

        self.duration_minutes = ""
        self.duration_seconds = ""
        self.workout_type = ""
        self.message = f"✅ Тренировка '{workout.type}' добавлена"
        self.load_workouts()

    def delete_workout(self, workout_id: int):
        with rx.session() as session:
            workout = session.exec(select(Workout).where(Workout.id == workout_id)).first()
            if workout:
                session.delete(workout)
                session.commit()
        self.load_workouts()

    def load_workouts(self):
        with rx.session() as session:
            stmt = select(Workout).order_by(Workout.date.desc())
            self.workouts = session.exec(stmt).all()

    def set_filter_type(self, value: str):
        self.filter_type = value
        self.current_page = 1

    def set_sort_option(self, value: str):
        self.sort_option = value
        self.current_page = 1

    def sort_workouts(self, workouts: list[dict]) -> list[dict]:
        match self.sort_option:
            case "Дата ↑":
                return sorted(workouts, key=lambda x: x["datetime"])
            case "Дата ↓":
                return sorted(workouts, key=lambda x: x["datetime"], reverse=True)
            case "Калории ↑":
                return sorted(workouts, key=lambda x: x["calories"])
            case "Калории ↓":
                return sorted(workouts, key=lambda x: x["calories"], reverse=True)
            case _:
                return workouts

    @rx.var
    def filtered_workouts(self) -> list[dict]:
        filtered = self.workouts
        if self.filter_type.lower() != "все":
            filtered = [w for w in self.workouts if w.type.lower() == self.filter_type.lower()]

        result = []
        for w in filtered:
            duration_min = int(w.duration)
            duration_sec = int(round((w.duration - duration_min) * 60))
            result.append({
                "id": w.id,
                "datetime": w.date,
                "date": w.date.strftime("%Y-%m-%d %H:%M:%S"),
                "type": w.type.title(),
                "duration": round(w.duration, 2),
                "duration_minutes": duration_min,
                "duration_seconds": duration_sec,
                "calories": round(w.calories, 1),
                "weight": w.weight,
            })
        return self.sort_workouts(result)

    @rx.var
    def total_pages(self) -> int:
        return max((len(self.filtered_workouts) + self.page_size - 1) // self.page_size, 1)

    @rx.var
    def page_workouts(self) -> list[dict]:
        start = (self.current_page - 1) * self.page_size
        return self.filtered_workouts[start:start + self.page_size]

    @rx.var
    def page_label(self) -> str:
        return f"Страница {self.current_page} из {self.total_pages}"

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    def export_csv(self):
        output = io.StringIO()
        output.write('\ufeff')
        writer = csv.writer(output)
        writer.writerow(["Дата и время", "Тип", "Минуты", "Секунды", "Вес (кг)", "Калории"])

        for w in self.filtered_workouts:
            writer.writerow([
                w["datetime"].strftime("%Y-%m-%d %H:%M:%S"),
                w["type"],
                w["duration_minutes"],
                w["duration_seconds"],
                w["weight"],
                w["calories"]
            ])

        csv_data = output.getvalue()
        output.close()

        filename = f"workouts_{datetime.now():%Y%m%d_%H%M%S}.csv"
        return rx.download(filename=filename, data=csv_data)

    @rx.var
    def profile_weight_val(self) -> float | None:
        with rx.session() as session:
            profile = session.exec(select(UserProfile)).first()
            return profile.weight if profile else None

    @rx.event
    def load_profile_weight(self):
        with rx.session() as session:
            profile = session.exec(select(UserProfile)).first()
            if profile:
                self.weight = str(profile.weight)


class UserProfileState(rx.State):
    profile_weight: str = ""

    def set_profile_weight(self, value: str):
        self.profile_weight = value

    def load_profile(self):
        with rx.session() as session:
            profile = session.exec(select(UserProfile)).first()
            if profile:
                self.profile_weight = str(profile.weight)

    def save_profile(self):
        try:
            weight = float(self.profile_weight)
        except ValueError:
            return rx.window_alert("❌ Введите корректный вес \n P.S. Если значение веса нецелое, введите его через точку")

        with rx.session() as session:
            profile = session.exec(select(UserProfile)).first()
            if not profile:
                profile = UserProfile(weight=weight)
                session.add(profile)
            else:
                profile.weight = weight
            session.commit()

        return rx.window_alert("✅ Вес обновлён")
