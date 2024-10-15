"""device data, connect log

Revision ID: 698610592768
Revises: 24d5a0f27b28
Create Date: 2024-10-02 14:27:58.446794

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "698610592768"
down_revision: str | None = "24d5a0f27b28"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "connect_logs",
        sa.Column("device_id", sa.UUID(), nullable=False),
        sa.Column("ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("connect_status", sa.SMALLINT(), nullable=False),
        sa.Column("ip", sa.TEXT(), nullable=False),
        sa.ForeignKeyConstraint(
            ["device_id"], ["devices.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("device_id", "ts"),
    )
    op.create_table(
        "device_attribute",
        sa.Column("device_id", sa.UUID(), nullable=False),
        sa.Column("key", sa.TEXT(), nullable=False),
        sa.Column("last_update", sa.DateTime(timezone=True), nullable=False),
        sa.Column("bool_v", sa.BOOLEAN(), nullable=True),
        sa.Column("str_v", sa.TEXT(), nullable=True),
        sa.Column("long_v", sa.BIGINT(), nullable=True),
        sa.Column("double_v", sa.DOUBLE_PRECISION(), nullable=True),  # type: ignore
        sa.Column(
            "json_v", postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), nullable=True
        ),
        sa.Column("device_can_edit", sa.BOOLEAN(), nullable=False),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("device_id", "key"),
    )
    op.create_index(
        "device_attribute_device_id_idx", "device_attribute", ["device_id"], unique=False
    )
    op.create_index(
        "device_attribute_device_id_key_idx", "device_attribute", ["device_id", "key"], unique=False
    )
    op.create_table(
        "device_data",
        sa.Column("device_id", sa.UUID(), nullable=False),
        sa.Column("ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("key", sa.TEXT(), nullable=False),
        sa.Column("bool_v", sa.BOOLEAN(), nullable=True),
        sa.Column("str_v", sa.TEXT(), nullable=True),
        sa.Column("long_v", sa.BIGINT(), nullable=True),
        sa.Column("double_v", sa.DOUBLE_PRECISION(), nullable=True),  # type: ignore
        sa.Column(
            "json_v", postgresql.JSON(none_as_null=True, astext_type=sa.Text()), nullable=True
        ),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("device_id", "ts", "key"),
    )
    op.create_index(
        "device_data_device_id_ts_key_idx", "device_data", ["device_id", "ts", "key"], unique=False
    )
    op.create_table(
        "device_data_latest",
        sa.Column("device_id", sa.UUID(), nullable=False),
        sa.Column("ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("key", sa.TEXT(), nullable=False),
        sa.Column("bool_v", sa.BOOLEAN(), nullable=True),
        sa.Column("str_v", sa.TEXT(), nullable=True),
        sa.Column("long_v", sa.BIGINT(), nullable=True),
        sa.Column("double_v", sa.DOUBLE_PRECISION(), nullable=True),  # type: ignore
        sa.Column(
            "json_v", postgresql.JSON(none_as_null=True, astext_type=sa.Text()), nullable=True
        ),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("device_id", "key"),
    )
    op.create_index(
        "device_data_latest_device_id_idx", "device_data_latest", ["device_id"], unique=False
    )
    op.create_index(
        "device_data_latest_device_id_key_idx",
        "device_data_latest",
        ["device_id", "key"],
        unique=False,
    )

    # Create extension
    op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")

    # Create hypertable
    # chunk_time_interval = 14 days not experimentally determined
    op.execute(
        """
        SELECT create_hypertable(
            'device_data',
            'ts',
            chunk_time_interval => INTERVAL '14 days',
            if_not_exists => TRUE
        );
        """
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("device_data_latest_device_id_key_idx", table_name="device_data_latest")
    op.drop_index("device_data_latest_device_id_idx", table_name="device_data_latest")
    op.drop_table("device_data_latest")
    op.drop_index("device_data_device_id_ts_key_idx", table_name="device_data")
    op.drop_table("device_data")
    op.drop_index("device_attribute_device_id_key_idx", table_name="device_attribute")
    op.drop_index("device_attribute_device_id_idx", table_name="device_attribute")
    op.drop_table("device_attribute")
    op.drop_table("connect_logs")
    # ### end Alembic commands ###