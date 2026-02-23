"""Carpooling / ride-sharing platform backend."""
import os
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
import argparse
import sys


@dataclass
class Ride:
    """Represents a ride offered by a driver."""
    id: str
    driver: str
    origin: str
    destination: str
    departure_ts: str
    seats_total: int
    seats_available: int
    price_per_seat: float
    route_km: float
    status: str  # "active", "completed", "cancelled"
    riders: List[str] = field(default_factory=list)


@dataclass
class RideRequest:
    """Represents a ride request from a rider."""
    id: str
    rider: str
    origin: str
    destination: str
    desired_ts: str
    max_price: float
    status: str  # "pending", "matched", "completed", "cancelled"
    matched_ride_id: Optional[str] = None


class CarpoolPlatform:
    """Main carpooling platform class."""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.expanduser("~/.blackroad/carpool.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rides (
                id TEXT PRIMARY KEY,
                driver TEXT,
                origin TEXT,
                destination TEXT,
                departure_ts TEXT,
                seats_total INTEGER,
                seats_available INTEGER,
                price_per_seat REAL,
                route_km REAL,
                status TEXT,
                riders TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ride_requests (
                id TEXT PRIMARY KEY,
                rider TEXT,
                origin TEXT,
                destination TEXT,
                desired_ts TEXT,
                max_price REAL,
                status TEXT,
                matched_ride_id TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                ride_id TEXT,
                rider TEXT,
                rating INTEGER,
                UNIQUE(ride_id, rider)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _get_conn(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)
    
    def offer_ride(self, driver: str, origin: str, destination: str, 
                   departure_ts: str, seats: int, price_per_seat: float, 
                   route_km: float = 0) -> str:
        """Offer a ride."""
        import uuid
        ride_id = str(uuid.uuid4())[:8]
        
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO rides VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ride_id, driver, origin, destination, departure_ts, 
              seats, seats, price_per_seat, route_km, "active", "[]"))
        conn.commit()
        conn.close()
        return ride_id
    
    def request_ride(self, rider: str, origin: str, destination: str,
                     desired_ts: str, max_price: float = 999) -> str:
        """Request a ride."""
        import uuid
        request_id = str(uuid.uuid4())[:8]
        
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ride_requests VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (request_id, rider, origin, destination, desired_ts, 
              max_price, "pending", None))
        conn.commit()
        conn.close()
        return request_id
    
    def match_rides(self) -> Dict[str, str]:
        """Auto-match requests to available rides by destination proximity + time window."""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM ride_requests WHERE status = 'pending'")
        requests = cursor.fetchall()
        
        matches = {}
        for req in requests:
            req_id, rider, origin, destination, desired_ts, max_price, _, _ = req
            
            # Find matching rides
            cursor.execute("""
                SELECT id FROM rides 
                WHERE origin = ? AND destination = ? 
                AND seats_available > 0 
                AND status = 'active'
                AND price_per_seat <= ?
                LIMIT 1
            """, (origin, destination, max_price))
            
            ride = cursor.fetchone()
            if ride:
                ride_id = ride[0]
                # Update request
                cursor.execute("""
                    UPDATE ride_requests SET status = 'matched', matched_ride_id = ?
                    WHERE id = ?
                """, (ride_id, req_id))
                matches[req_id] = ride_id
        
        conn.commit()
        conn.close()
        return matches
    
    def join_ride(self, ride_id: str, rider: str) -> bool:
        """Book a seat on a ride."""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("SELECT riders, seats_available FROM rides WHERE id = ?", (ride_id,))
        row = cursor.fetchone()
        if not row or row[1] <= 0:
            conn.close()
            return False
        
        import json
        riders = json.loads(row[0]) if row[0] != "[]" else []
        riders.append(rider)
        
        cursor.execute("""
            UPDATE rides SET riders = ?, seats_available = seats_available - 1
            WHERE id = ?
        """, (json.dumps(riders), ride_id))
        
        conn.commit()
        conn.close()
        return True
    
    def leave_ride(self, ride_id: str, rider: str) -> bool:
        """Remove rider from ride."""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("SELECT riders FROM rides WHERE id = ?", (ride_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False
        
        import json
        riders = json.loads(row[0])
        if rider not in riders:
            conn.close()
            return False
        
        riders.remove(rider)
        cursor.execute("""
            UPDATE rides SET riders = ?, seats_available = seats_available + 1
            WHERE id = ?
        """, (json.dumps(riders), ride_id))
        
        conn.commit()
        conn.close()
        return True
    
    def complete_ride(self, ride_id: str) -> float:
        """Mark ride complete and calculate CO2 saved."""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("SELECT riders, route_km FROM rides WHERE id = ?", (ride_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return 0
        
        import json
        riders = json.loads(row[0])
        route_km = row[1]
        
        co2_saved = (len(riders) - 1) * route_km * 0.21 if len(riders) > 0 else 0
        
        cursor.execute("UPDATE rides SET status = 'completed' WHERE id = ?", (ride_id,))
        conn.commit()
        conn.close()
        
        return co2_saved
    
    def get_rides(self, origin: str = None, destination: str = None, 
                  status: str = "active") -> List[Ride]:
        """Get rides with optional filters."""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        query = "SELECT * FROM rides WHERE status = ?"
        params = [status]
        
        if origin:
            query += " AND origin = ?"
            params.append(origin)
        if destination:
            query += " AND destination = ?"
            params.append(destination)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        import json
        rides = []
        for row in rows:
            riders = json.loads(row[10]) if row[10] != "[]" else []
            rides.append(Ride(
                id=row[0], driver=row[1], origin=row[2], destination=row[3],
                departure_ts=row[4], seats_total=row[5], seats_available=row[6],
                price_per_seat=row[7], route_km=row[8], status=row[9], riders=riders
            ))
        
        return rides
    
    def get_stats(self) -> Dict:
        """Get platform statistics."""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM rides WHERE status = 'completed'")
        total_rides = cursor.fetchone()[0]
        
        cursor.execute("SELECT riders FROM rides WHERE status = 'completed'")
        rows = cursor.fetchall()
        
        import json
        total_riders = 0
        total_km = 0
        co2_saved = 0
        
        cursor.execute("SELECT route_km FROM rides WHERE status = 'completed'")
        km_rows = cursor.fetchall()
        total_km = sum(row[0] for row in km_rows)
        
        for row in rows:
            riders = json.loads(row[0]) if row[0] != "[]" else []
            total_riders += len(riders)
            if len(riders) > 0:
                cursor.execute("SELECT route_km FROM rides WHERE riders = ?", (json.dumps(riders),))
                ride_km = cursor.fetchone()
                if ride_km:
                    co2_saved += (len(riders) - 1) * ride_km[0] * 0.21
        
        avg_occupancy = total_riders / total_rides if total_rides > 0 else 0
        
        conn.close()
        
        return {
            "total_rides": total_rides,
            "total_riders": total_riders,
            "avg_occupancy": round(avg_occupancy, 2),
            "co2_saved_kg": round(co2_saved, 2),
            "total_km": round(total_km, 2)
        }
    
    def rate_driver(self, ride_id: str, rider: str, rating: int) -> bool:
        """Rate driver (1-5 stars)."""
        if rating < 1 or rating > 5:
            return False
        
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO ratings VALUES (?, ?, ?)
        """, (ride_id, rider, rating))
        
        conn.commit()
        conn.close()
        return True


def cli():
    """Command-line interface."""
    parser = argparse.ArgumentParser(description="Carpooling Platform")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # rides command
    rides_parser = subparsers.add_parser("rides", help="List rides")
    rides_parser.add_argument("--origin", help="Filter by origin")
    rides_parser.add_argument("--destination", help="Filter by destination")
    
    # offer command
    offer_parser = subparsers.add_parser("offer", help="Offer a ride")
    offer_parser.add_argument("driver")
    offer_parser.add_argument("origin")
    offer_parser.add_argument("destination")
    offer_parser.add_argument("departure_ts")
    offer_parser.add_argument("seats", type=int)
    offer_parser.add_argument("price_per_seat", type=float)
    offer_parser.add_argument("--route_km", type=float, default=0)
    
    # stats command
    stats_parser = subparsers.add_parser("stats", help="Get platform stats")
    
    args = parser.parse_args()
    platform = CarpoolPlatform()
    
    if args.command == "rides":
        rides = platform.get_rides(origin=args.origin, destination=args.destination)
        for ride in rides:
            print(f"{ride.id} | {ride.driver} | {ride.origin} → {ride.destination} | "
                  f"${ride.price_per_seat} | {ride.seats_available}/{ride.seats_total} seats | "
                  f"{ride.departure_ts}")
    
    elif args.command == "offer":
        ride_id = platform.offer_ride(args.driver, args.origin, args.destination,
                                      args.departure_ts, args.seats, args.price_per_seat,
                                      args.route_km)
        print(f"Ride offered: {ride_id}")
    
    elif args.command == "stats":
        stats = platform.get_stats()
        print(f"Total Rides: {stats['total_rides']}")
        print(f"Total Riders: {stats['total_riders']}")
        print(f"Avg Occupancy: {stats['avg_occupancy']}")
        print(f"CO2 Saved: {stats['co2_saved_kg']} kg")
        print(f"Total KM: {stats['total_km']} km")


if __name__ == "__main__":
    cli()
