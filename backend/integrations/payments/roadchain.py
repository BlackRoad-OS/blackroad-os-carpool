"""
RoadChain Integration

Append-only ledger for all economic events.
NOT a blockchain - centralized, Stripe-mirrored ledger.

Per 12-ROADCHAIN.md
"""

from typing import Dict, Optional, List
from datetime import datetime
import hashlib
import json
from enum import Enum


class EntryType(str, Enum):
    """RoadChain entry types per 12-ROADCHAIN.md"""
    CREDIT_GRANT = "credit_grant"      # Credits added (Stripe payment)
    CREDIT_BURN = "credit_burn"        # Credits consumed (usage)
    TRANSFER = "transfer"              # Credits moved between entities
    VERIFICATION = "verification"      # Cryptographic proof
    REWARD = "reward"                  # Credits earned
    PAYOUT = "payout"                  # Credits → fiat


class EntityType(str, Enum):
    """Entity types in RoadChain"""
    USER = "user"
    ORG = "org"
    AGENT = "agent"
    SYSTEM = "system"


class RoadChainIntegration:
    """
    RoadChain ledger integration.

    Implements PS-SHA∞ (Persistent State SHA Infinity) hashing
    for cryptographically-linked entries.
    """

    def __init__(self, database):
        """
        Initialize RoadChain integration.

        Args:
            database: Database connection (SQLAlchemy session)
        """
        self.db = database

    async def create_entry(
        self,
        entry_type: EntryType,
        amount: float,
        from_entity_type: Optional[EntityType] = None,
        from_entity_id: Optional[str] = None,
        to_entity_type: Optional[EntityType] = None,
        to_entity_id: Optional[str] = None,
        currency: str = "ROADCOIN",
        stripe_payment_intent_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict:
        """
        Create a new RoadChain entry.

        Implements PS-SHA∞ hash chaining per 12-ROADCHAIN.md
        """

        # Get previous entry hash
        previous_entry = await self._get_latest_entry()
        previous_hash = previous_entry["entry_hash"] if previous_entry else None

        # Compute entry hash (PS-SHA∞)
        entry_data = {
            "entry_type": entry_type.value,
            "from": f"{from_entity_type}:{from_entity_id}" if from_entity_type else "null",
            "to": f"{to_entity_type}:{to_entity_id}" if to_entity_type else "null",
            "amount": str(amount),
            "currency": currency,
            "metadata": json.dumps(metadata or {}, sort_keys=True),
            "timestamp": datetime.utcnow().isoformat(),
        }

        entry_hash = self._compute_ps_sha_hash(entry_data, previous_hash)

        # Insert into database
        entry = await self.db.roadchain_entries.insert().values(
            entry_type=entry_type.value,
            from_entity_type=from_entity_type.value if from_entity_type else None,
            from_entity_id=from_entity_id,
            to_entity_type=to_entity_type.value if to_entity_type else None,
            to_entity_id=to_entity_id,
            amount=amount,
            currency=currency,
            stripe_payment_intent_id=stripe_payment_intent_id,
            previous_hash=previous_hash,
            entry_hash=entry_hash,
            metadata=metadata or {},
            idempotency_key=idempotency_key,
            created_at=datetime.utcnow()
        )

        # Update balance cache
        if to_entity_type and to_entity_id:
            await self._update_balance(to_entity_type, to_entity_id, amount, add=True)

        if from_entity_type and from_entity_id:
            await self._update_balance(from_entity_type, from_entity_id, amount, add=False)

        return entry

    async def get_balance(
        self,
        entity_type: EntityType,
        entity_id: str,
        currency: str = "ROADCOIN"
    ) -> float:
        """Get current balance for an entity"""
        result = await self.db.roadchain_balances.select().where(
            (self.db.roadchain_balances.c.entity_type == entity_type.value) &
            (self.db.roadchain_balances.c.entity_id == entity_id) &
            (self.db.roadchain_balances.c.currency == currency)
        ).first()

        return float(result["balance"]) if result else 0.0

    async def list_entries(
        self,
        entity_id: Optional[str] = None,
        entity_type: Optional[EntityType] = None,
        entry_type: Optional[EntryType] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict]:
        """List RoadChain entries with filters"""
        query = self.db.roadchain_entries.select()

        if entity_id and entity_type:
            query = query.where(
                ((self.db.roadchain_entries.c.from_entity_id == entity_id) &
                 (self.db.roadchain_entries.c.from_entity_type == entity_type.value)) |
                ((self.db.roadchain_entries.c.to_entity_id == entity_id) &
                 (self.db.roadchain_entries.c.to_entity_type == entity_type.value))
            )

        if entry_type:
            query = query.where(
                self.db.roadchain_entries.c.entry_type == entry_type.value
            )

        query = query.order_by(
            self.db.roadchain_entries.c.sequence_number.desc()
        ).limit(limit).offset(offset)

        return await query.all()

    async def verify_chain(
        self,
        from_sequence: int,
        to_sequence: int
    ) -> bool:
        """
        Verify chain integrity between two sequence numbers.

        Returns True if all hashes are valid.
        """
        entries = await self.db.roadchain_entries.select().where(
            (self.db.roadchain_entries.c.sequence_number >= from_sequence) &
            (self.db.roadchain_entries.c.sequence_number <= to_sequence)
        ).order_by(self.db.roadchain_entries.c.sequence_number).all()

        previous_hash = None

        for entry in entries:
            expected_hash = self._compute_ps_sha_hash(
                {
                    "entry_type": entry["entry_type"],
                    "from": f"{entry['from_entity_type']}:{entry['from_entity_id']}",
                    "to": f"{entry['to_entity_type']}:{entry['to_entity_id']}",
                    "amount": str(entry["amount"]),
                    "currency": entry["currency"],
                    "metadata": json.dumps(entry["metadata"], sort_keys=True),
                    "timestamp": entry["created_at"].isoformat(),
                },
                previous_hash
            )

            if entry["entry_hash"] != expected_hash:
                return False

            previous_hash = entry["entry_hash"]

        return True

    def _compute_ps_sha_hash(
        self,
        entry_data: Dict,
        previous_hash: Optional[str]
    ) -> str:
        """
        Compute PS-SHA∞ hash for an entry.

        Per 12-ROADCHAIN.md implementation.
        """
        canonical = {
            "prev": previous_hash or "GENESIS",
            "type": entry_data["entry_type"],
            "from": entry_data["from"],
            "to": entry_data["to"],
            "amount": entry_data["amount"],
            "currency": entry_data["currency"],
            "ts": entry_data["timestamp"],
            "meta": entry_data["metadata"],
        }

        serialized = json.dumps(canonical, sort_keys=True, separators=(',', ':'))
        hash_bytes = hashlib.sha256(serialized.encode('utf-8')).hexdigest()

        return f"ps-sha256:{hash_bytes}"

    async def _get_latest_entry(self) -> Optional[Dict]:
        """Get the most recent entry in the chain"""
        return await self.db.roadchain_entries.select().order_by(
            self.db.roadchain_entries.c.sequence_number.desc()
        ).first()

    async def _update_balance(
        self,
        entity_type: EntityType,
        entity_id: str,
        amount: float,
        add: bool = True
    ):
        """Update balance cache (materialized view)"""
        # Upsert balance
        current = await self.get_balance(entity_type, entity_id)
        new_balance = current + amount if add else current - amount

        if new_balance < 0:
            raise ValueError("Insufficient balance")

        await self.db.roadchain_balances.upsert().values(
            entity_type=entity_type.value,
            entity_id=entity_id,
            currency="ROADCOIN",
            balance=new_balance,
            updated_at=datetime.utcnow()
        )
