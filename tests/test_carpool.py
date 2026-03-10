"""
Tests for the CarpoolPlatform ride-sharing module (src/carpool.py).

These tests use only the Python standard library and run with the
existing CI configuration (pytest tests/).
"""

import sys
import os
import tempfile
import pytest

# Allow importing from src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from carpool import CarpoolPlatform, Ride, RideRequest


@pytest.fixture
def platform(tmp_path):
    """Provide a fresh CarpoolPlatform backed by a temporary SQLite database."""
    db_file = str(tmp_path / "test_carpool.db")
    return CarpoolPlatform(db_path=db_file)


# ---------------------------------------------------------------------------
# Offer ride
# ---------------------------------------------------------------------------

class TestOfferRide:
    def test_returns_ride_id(self, platform):
        ride_id = platform.offer_ride(
            driver="alice",
            origin="Downtown",
            destination="Airport",
            departure_ts="2026-06-01T08:00",
            seats=3,
            price_per_seat=5.0,
        )
        assert ride_id is not None
        assert isinstance(ride_id, str)

    def test_ride_visible_in_get_rides(self, platform):
        platform.offer_ride("alice", "A", "B", "2026-06-01T08:00", 2, 4.0)
        rides = platform.get_rides()
        assert len(rides) == 1
        assert rides[0].driver == "alice"

    def test_ride_seats_match(self, platform):
        platform.offer_ride("bob", "X", "Y", "2026-06-01T09:00", 4, 3.0)
        rides = platform.get_rides()
        assert rides[0].seats_total == 4
        assert rides[0].seats_available == 4

    def test_ride_status_is_active(self, platform):
        platform.offer_ride("carol", "A", "B", "2026-06-01T10:00", 2, 2.0)
        rides = platform.get_rides(status="active")
        assert rides[0].status == "active"

    def test_multiple_rides_stored(self, platform):
        for i in range(3):
            platform.offer_ride(f"driver{i}", "A", "B", "2026-06-01T08:00", 2, 5.0)
        assert len(platform.get_rides()) == 3


# ---------------------------------------------------------------------------
# Request ride
# ---------------------------------------------------------------------------

class TestRequestRide:
    def test_returns_request_id(self, platform):
        req_id = platform.request_ride("dave", "A", "B", "2026-06-01T08:00")
        assert req_id is not None

    def test_request_with_max_price(self, platform):
        req_id = platform.request_ride("eve", "A", "B", "2026-06-01T08:00", max_price=10.0)
        assert req_id is not None


# ---------------------------------------------------------------------------
# Join ride
# ---------------------------------------------------------------------------

class TestJoinRide:
    def test_join_reduces_available_seats(self, platform):
        ride_id = platform.offer_ride("alice", "A", "B", "2026-06-01T08:00", 3, 5.0)
        result = platform.join_ride(ride_id, "bob")
        assert result is True
        rides = platform.get_rides()
        assert rides[0].seats_available == 2

    def test_join_unknown_ride_returns_false(self, platform):
        result = platform.join_ride("nonexistent_id", "bob")
        assert result is False

    def test_join_full_ride_returns_false(self, platform):
        ride_id = platform.offer_ride("alice", "A", "B", "2026-06-01T08:00", 1, 5.0)
        platform.join_ride(ride_id, "bob")
        result = platform.join_ride(ride_id, "carol")
        assert result is False

    def test_rider_appears_in_ride(self, platform):
        ride_id = platform.offer_ride("alice", "A", "B", "2026-06-01T08:00", 3, 5.0)
        platform.join_ride(ride_id, "bob")
        rides = platform.get_rides()
        assert "bob" in rides[0].riders


# ---------------------------------------------------------------------------
# Leave ride
# ---------------------------------------------------------------------------

class TestLeaveRide:
    def test_leave_increases_available_seats(self, platform):
        ride_id = platform.offer_ride("alice", "A", "B", "2026-06-01T08:00", 3, 5.0)
        platform.join_ride(ride_id, "bob")
        result = platform.leave_ride(ride_id, "bob")
        assert result is True
        rides = platform.get_rides()
        assert rides[0].seats_available == 3

    def test_leave_unknown_rider_returns_false(self, platform):
        ride_id = platform.offer_ride("alice", "A", "B", "2026-06-01T08:00", 3, 5.0)
        result = platform.leave_ride(ride_id, "nobody")
        assert result is False

    def test_leave_unknown_ride_returns_false(self, platform):
        result = platform.leave_ride("bad_id", "bob")
        assert result is False


# ---------------------------------------------------------------------------
# Match rides
# ---------------------------------------------------------------------------

class TestMatchRides:
    def test_match_returns_mapping(self, platform):
        platform.offer_ride("alice", "Downtown", "Airport", "2026-06-01T08:00", 3, 5.0)
        req_id = platform.request_ride("bob", "Downtown", "Airport", "2026-06-01T08:00")
        matches = platform.match_rides()
        assert req_id in matches

    def test_no_match_when_no_rides(self, platform):
        platform.request_ride("bob", "A", "B", "2026-06-01T08:00")
        matches = platform.match_rides()
        assert len(matches) == 0

    def test_no_match_when_price_too_high(self, platform):
        platform.offer_ride("alice", "A", "B", "2026-06-01T08:00", 3, 20.0)
        req_id = platform.request_ride("bob", "A", "B", "2026-06-01T08:00", max_price=5.0)
        matches = platform.match_rides()
        assert req_id not in matches


# ---------------------------------------------------------------------------
# Complete ride
# ---------------------------------------------------------------------------

class TestCompleteRide:
    def test_complete_marks_status(self, platform):
        ride_id = platform.offer_ride("alice", "A", "B", "2026-06-01T08:00", 3, 5.0, route_km=10)
        platform.join_ride(ride_id, "bob")
        platform.complete_ride(ride_id)
        completed = platform.get_rides(status="completed")
        assert len(completed) == 1
        assert completed[0].status == "completed"

    def test_complete_returns_co2_saved(self, platform):
        ride_id = platform.offer_ride("alice", "A", "B", "2026-06-01T08:00", 3, 5.0, route_km=100)
        platform.join_ride(ride_id, "bob")
        co2 = platform.complete_ride(ride_id)
        # 1 extra rider × 100 km × 0.21 kg/km = 21 kg
        assert co2 == pytest.approx(21.0)

    def test_complete_unknown_ride_returns_zero(self, platform):
        co2 = platform.complete_ride("bad_id")
        assert co2 == 0


# ---------------------------------------------------------------------------
# Rating
# ---------------------------------------------------------------------------

class TestRating:
    def test_valid_rating_returns_true(self, platform):
        ride_id = platform.offer_ride("alice", "A", "B", "2026-06-01T08:00", 3, 5.0)
        assert platform.rate_driver(ride_id, "bob", 5) is True

    def test_rating_below_1_returns_false(self, platform):
        ride_id = platform.offer_ride("alice", "A", "B", "2026-06-01T08:00", 3, 5.0)
        assert platform.rate_driver(ride_id, "bob", 0) is False

    def test_rating_above_5_returns_false(self, platform):
        ride_id = platform.offer_ride("alice", "A", "B", "2026-06-01T08:00", 3, 5.0)
        assert platform.rate_driver(ride_id, "bob", 6) is False


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

class TestStats:
    def test_stats_empty_platform(self, platform):
        stats = platform.get_stats()
        assert stats["total_rides"] == 0
        assert stats["avg_occupancy"] == 0

    def test_stats_after_completed_ride(self, platform):
        ride_id = platform.offer_ride("alice", "A", "B", "2026-06-01T08:00", 3, 5.0, route_km=50)
        platform.join_ride(ride_id, "bob")
        platform.complete_ride(ride_id)
        stats = platform.get_stats()
        assert stats["total_rides"] == 1
        assert stats["total_km"] == 50.0


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

class TestGetRidesFiltering:
    def test_filter_by_origin(self, platform):
        platform.offer_ride("a", "Alpha", "Omega", "2026-06-01T08:00", 2, 3.0)
        platform.offer_ride("b", "Beta", "Omega", "2026-06-01T08:00", 2, 3.0)
        rides = platform.get_rides(origin="Alpha")
        assert len(rides) == 1
        assert rides[0].driver == "a"

    def test_filter_by_destination(self, platform):
        platform.offer_ride("a", "X", "NY", "2026-06-01T08:00", 2, 3.0)
        platform.offer_ride("b", "X", "LA", "2026-06-01T08:00", 2, 3.0)
        rides = platform.get_rides(destination="LA")
        assert len(rides) == 1
        assert rides[0].driver == "b"
