import pytest

from app.modules.extraction.normalize import normalize_frequency, parse_duration_days


@pytest.mark.parametrize(
    ("raw", "times", "label"),
    [
        ("1-0-1", ["08:00", "20:00"], "Twice daily"),
        ("1-1-1", ["08:00", "14:00", "20:00"], "Three times daily"),
        ("0-0-1", ["20:00"], "Once daily"),
        ("1-0-0-1", ["08:00", "22:00"], "Twice daily"),
        ("½-0-½", ["08:00", "20:00"], "Twice daily"),
        ("BD", ["08:00", "20:00"], "Twice daily"),
        ("b.i.d.", ["08:00", "20:00"], None),
        ("Twice a day after meals", ["08:00", "20:00"], "Twice daily"),
        ("TDS", ["08:00", "14:00", "20:00"], "Three times daily"),
        ("TID with food", ["08:00", "14:00", "20:00"], "Three times daily"),
        ("QID", ["08:00", "14:00", "20:00", "22:00"], "Four times daily"),
        ("OD", ["08:00"], "Once daily"),
        ("once daily", ["08:00"], "Once daily"),
        ("HS", ["22:00"], "Once daily at bedtime"),
        ("at night", ["22:00"], "Once daily at bedtime"),
        ("every evening", ["20:00"], "Once daily in the evening"),
        ("q8h", ["00:00", "08:00", "16:00"], "Every 8 hours"),
        ("every 12 hours", ["08:00", "20:00"], "Every 12 hours"),
        ("q6h", ["02:00", "08:00", "14:00", "20:00"], "Every 6 hours"),
    ],
)
def test_frequency_to_times(raw, times, label):
    s = normalize_frequency(raw)
    assert s.times == times
    assert not s.needs_attention
    if label:
        assert s.label == label


@pytest.mark.parametrize(
    "raw", ["SOS", "PRN", "as needed for pain", "SOS, max TDS", "when required"]
)
def test_as_needed_is_never_scheduled(raw):
    s = normalize_frequency(raw)
    assert s.as_needed is True
    assert s.times == []
    assert s.period == "as_needed"


def test_weekly_and_alternate_days():
    assert normalize_frequency("once a week").period == "weekly"
    assert normalize_frequency("alternate days").period == "alternate_days"
    assert normalize_frequency("STAT").period == "once"


def test_user_dose_times_are_respected():
    s = normalize_frequency("BD", {"morning": "07:30", "evening": "19:00"})
    assert s.times == ["07:30", "19:00"]


@pytest.mark.parametrize("raw", ["", None, "take as directed", "0-0-0", "q5h"])
def test_unclear_input_is_flagged(raw):
    assert normalize_frequency(raw).needs_attention is True


@pytest.mark.parametrize(
    ("raw", "days"),
    [
        ("x 7 days", 7),
        ("for 5 days", 5),
        ("7/7", 7),
        ("2/52", 14),
        ("3/12", 90),
        ("1 week", 7),
        ("2 weeks", 14),
        ("1 month", 30),
        ("90 days", 90),
        ("x5d", 5),
        ("ongoing", None),
        ("continue", None),
        ("", None),
        (None, None),
    ],
)
def test_duration_parsing(raw, days):
    assert parse_duration_days(raw) == days
