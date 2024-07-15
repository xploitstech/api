"""Bytea address in labels

Revision ID: 38ad819f94ed
Revises: 792ca9c4722c
Create Date: 2024-07-15 16:16:35.400430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38ad819f94ed'
down_revision: Union[str, None] = '792ca9c4722c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('amoy_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('arbitrum_nova_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('arbitrum_one_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('arbitrum_sepolia_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('avalanche_fuji_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('avalanche_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('base_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('blast_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('blast_sepolia_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('ethereum_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('game7_orbit_arbitrum_sepolia_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('mantle_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('mantle_sepolia_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('mumbai_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('polygon_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('proofofplay_apex_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('sepolia_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('starknet_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('starknet_sepolia_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('xai_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('xai_sepolia_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('xdai_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('zksync_era_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    op.alter_column('zksync_era_sepolia_labels', 'address',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.LargeBinary(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('zksync_era_sepolia_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('zksync_era_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('xdai_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('xai_sepolia_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('xai_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('starknet_sepolia_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('starknet_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('sepolia_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('proofofplay_apex_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('polygon_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('mumbai_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('mantle_sepolia_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('mantle_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('game7_orbit_arbitrum_sepolia_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('ethereum_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('blast_sepolia_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('blast_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('base_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('avalanche_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('avalanche_fuji_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('arbitrum_sepolia_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('arbitrum_one_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('arbitrum_nova_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('amoy_labels', 'address',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=64),
               nullable=True)
    # ### end Alembic commands ###
