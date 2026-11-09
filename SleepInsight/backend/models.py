from __future__ import annotations

from datetime import datetime, date
from typing import Optional

from sqlalchemy import String, Integer, Float, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    display_name: Mapped[str] = mapped_column(String(80), default="Student")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sleep_records: Mapped[list["SleepRecord"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    caffeine_events: Mapped[list["CaffeineEvent"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    exercise_sessions: Mapped[list["ExerciseSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    screen_records: Mapped[list["ScreenRecord"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    goals: Mapped[list["Goal"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class SleepRecord(Base):
    __tablename__ = "sleep_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=1, index=True)
    sleep_date: Mapped[date] = mapped_column(Date, unique=True, index=True)
    bedtime: Mapped[str] = mapped_column(String(5))
    wake_time: Mapped[str] = mapped_column(String(5))
    latency_minutes: Mapped[int] = mapped_column(Integer, default=0)
    awakenings: Mapped[int] = mapped_column(Integer, default=0)
    quality: Mapped[int] = mapped_column(Integer)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    sleep_midpoint_minutes: Mapped[int] = mapped_column(Integer)
    actual_sleep_start_iso: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="sleep_records")


class CaffeineEvent(Base):
    __tablename__ = "caffeine_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=1, index=True)
    event_date: Mapped[date] = mapped_column(Date, index=True)
    time: Mapped[str] = mapped_column(String(5))
    amount_mg: Mapped[float] = mapped_column(Float)
    beverage_type: Mapped[str] = mapped_column(String(60), default="Other")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="caffeine_events")


class ExerciseSession(Base):
    __tablename__ = "exercise_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=1, index=True)
    event_date: Mapped[date] = mapped_column(Date, index=True)
    time: Mapped[str] = mapped_column(String(5))
    duration_minutes: Mapped[int] = mapped_column(Integer)
    intensity: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="exercise_sessions")


class ScreenRecord(Base):
    __tablename__ = "screen_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=1, index=True)
    event_date: Mapped[date] = mapped_column(Date, unique=True, index=True)
    total_minutes: Mapped[int] = mapped_column(Integer)
    pre_bed_minutes: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="screen_records")


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=1, index=True)
    goal_type: Mapped[str] = mapped_column(String(40))
    title: Mapped[str] = mapped_column(String(120))
    target_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    target_time: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    target_nights_per_week: Mapped[int] = mapped_column(Integer, default=5)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    adaptive_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="goals")


class RecommendationLog(Base):
    __tablename__ = "recommendation_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, default=1, index=True)
    rule_id: Mapped[str] = mapped_column(String(60))
    title: Mapped[str] = mapped_column(String(160))
    priority_score: Mapped[float] = mapped_column(Float)
    reason: Mapped[str] = mapped_column(Text)
    confidence: Mapped[str] = mapped_column(String(20))
    dismissed: Mapped[bool] = mapped_column(Boolean, default=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
