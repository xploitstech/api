"""ZkSync Era model

Revision ID: e4a796c0407d
Revises: c413d5265f76
Create Date: 2023-07-12 12:27:12.814892

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e4a796c0407d'
down_revision = 'c413d5265f76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('zksync_era_testnet_blocks',
    sa.Column('block_number', sa.BigInteger(), nullable=False),
    sa.Column('difficulty', sa.BigInteger(), nullable=True),
    sa.Column('extra_data', sa.VARCHAR(length=128), nullable=True),
    sa.Column('gas_limit', sa.BigInteger(), nullable=True),
    sa.Column('gas_used', sa.BigInteger(), nullable=True),
    sa.Column('base_fee_per_gas', sa.Numeric(precision=78, scale=0), nullable=True),
    sa.Column('hash', sa.VARCHAR(length=256), nullable=True),
    sa.Column('logs_bloom', sa.VARCHAR(length=1024), nullable=True),
    sa.Column('miner', sa.VARCHAR(length=256), nullable=True),
    sa.Column('nonce', sa.VARCHAR(length=256), nullable=True),
    sa.Column('parent_hash', sa.VARCHAR(length=256), nullable=True),
    sa.Column('receipt_root', sa.VARCHAR(length=256), nullable=True),
    sa.Column('uncles', sa.VARCHAR(length=256), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('state_root', sa.VARCHAR(length=256), nullable=True),
    sa.Column('timestamp', sa.BigInteger(), nullable=True),
    sa.Column('total_difficulty', sa.VARCHAR(length=256), nullable=True),
    sa.Column('transactions_root', sa.VARCHAR(length=256), nullable=True),
    sa.Column('indexed_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.Column('mix_hash', sa.VARCHAR(length=256), nullable=True),
    sa.Column('sha3_uncles', sa.VARCHAR(length=256), nullable=True),
    sa.Column('l1_batch_number', sa.BigInteger(), nullable=True),
    sa.Column('l1_batch_timestamp', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('block_number', name=op.f('pk_zksync_era_testnet_blocks'))
    )
    op.create_index(op.f('ix_zksync_era_testnet_blocks_block_number'), 'zksync_era_testnet_blocks', ['block_number'], unique=True)
    op.create_index(op.f('ix_zksync_era_testnet_blocks_hash'), 'zksync_era_testnet_blocks', ['hash'], unique=False)
    op.create_index(op.f('ix_zksync_era_testnet_blocks_timestamp'), 'zksync_era_testnet_blocks', ['timestamp'], unique=False)
    op.create_table('zksync_era_testnet_labels',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('label', sa.VARCHAR(length=256), nullable=False),
    sa.Column('block_number', sa.BigInteger(), nullable=True),
    sa.Column('address', sa.VARCHAR(length=256), nullable=True),
    sa.Column('transaction_hash', sa.VARCHAR(length=256), nullable=True),
    sa.Column('label_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('block_timestamp', sa.BigInteger(), nullable=True),
    sa.Column('log_index', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_zksync_era_testnet_labels')),
    sa.UniqueConstraint('id', name=op.f('uq_zksync_era_testnet_labels_id'))
    )
    op.create_index(op.f('ix_zksync_era_testnet_labels_address'), 'zksync_era_testnet_labels', ['address'], unique=False)
    op.create_index('ix_zksync_era_testnet_labels_address_block_number', 'zksync_era_testnet_labels', ['address', 'block_number'], unique=False)
    op.create_index('ix_zksync_era_testnet_labels_address_block_timestamp', 'zksync_era_testnet_labels', ['address', 'block_timestamp'], unique=False)
    op.create_index(op.f('ix_zksync_era_testnet_labels_block_number'), 'zksync_era_testnet_labels', ['block_number'], unique=False)
    op.create_index(op.f('ix_zksync_era_testnet_labels_block_timestamp'), 'zksync_era_testnet_labels', ['block_timestamp'], unique=False)
    op.create_index(op.f('ix_zksync_era_testnet_labels_label'), 'zksync_era_testnet_labels', ['label'], unique=False)
    op.create_index(op.f('ix_zksync_era_testnet_labels_transaction_hash'), 'zksync_era_testnet_labels', ['transaction_hash'], unique=False)
    op.create_table('zksync_era_testnet_transactions',
    sa.Column('hash', sa.VARCHAR(length=256), nullable=False),
    sa.Column('block_number', sa.BigInteger(), nullable=False),
    sa.Column('from_address', sa.VARCHAR(length=256), nullable=True),
    sa.Column('to_address', sa.VARCHAR(length=256), nullable=True),
    sa.Column('gas', sa.Numeric(precision=78, scale=0), nullable=True),
    sa.Column('gas_price', sa.Numeric(precision=78, scale=0), nullable=True),
    sa.Column('max_fee_per_gas', sa.Numeric(precision=78, scale=0), nullable=True),
    sa.Column('max_priority_fee_per_gas', sa.Numeric(precision=78, scale=0), nullable=True),
    sa.Column('input', sa.Text(), nullable=True),
    sa.Column('nonce', sa.VARCHAR(length=256), nullable=True),
    sa.Column('transaction_index', sa.BigInteger(), nullable=True),
    sa.Column('transaction_type', sa.Integer(), nullable=True),
    sa.Column('value', sa.Numeric(precision=78, scale=0), nullable=True),
    sa.Column('indexed_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.Column('l1_batch_number', sa.BigInteger(), nullable=True),
    sa.Column('l1_batch_tx_index', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['block_number'], ['zksync_era_testnet_blocks.block_number'], name=op.f('fk_zksync_era_testnet_transactions_block_number_zksync_era_testnet_blocks'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('hash', name=op.f('pk_zksync_era_testnet_transactions'))
    )
    op.create_index(op.f('ix_zksync_era_testnet_transactions_block_number'), 'zksync_era_testnet_transactions', ['block_number'], unique=False)
    op.create_index(op.f('ix_zksync_era_testnet_transactions_from_address'), 'zksync_era_testnet_transactions', ['from_address'], unique=False)
    op.create_index(op.f('ix_zksync_era_testnet_transactions_gas'), 'zksync_era_testnet_transactions', ['gas'], unique=False)
    op.create_index(op.f('ix_zksync_era_testnet_transactions_gas_price'), 'zksync_era_testnet_transactions', ['gas_price'], unique=False)
    op.create_index(op.f('ix_zksync_era_testnet_transactions_hash'), 'zksync_era_testnet_transactions', ['hash'], unique=True)
    op.create_index(op.f('ix_zksync_era_testnet_transactions_to_address'), 'zksync_era_testnet_transactions', ['to_address'], unique=False)
    op.create_index(op.f('ix_zksync_era_testnet_transactions_value'), 'zksync_era_testnet_transactions', ['value'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_zksync_era_testnet_transactions_value'), table_name='zksync_era_testnet_transactions')
    op.drop_index(op.f('ix_zksync_era_testnet_transactions_to_address'), table_name='zksync_era_testnet_transactions')
    op.drop_index(op.f('ix_zksync_era_testnet_transactions_hash'), table_name='zksync_era_testnet_transactions')
    op.drop_index(op.f('ix_zksync_era_testnet_transactions_gas_price'), table_name='zksync_era_testnet_transactions')
    op.drop_index(op.f('ix_zksync_era_testnet_transactions_gas'), table_name='zksync_era_testnet_transactions')
    op.drop_index(op.f('ix_zksync_era_testnet_transactions_from_address'), table_name='zksync_era_testnet_transactions')
    op.drop_index(op.f('ix_zksync_era_testnet_transactions_block_number'), table_name='zksync_era_testnet_transactions')
    op.drop_table('zksync_era_testnet_transactions')
    op.drop_index(op.f('ix_zksync_era_testnet_labels_transaction_hash'), table_name='zksync_era_testnet_labels')
    op.drop_index(op.f('ix_zksync_era_testnet_labels_label'), table_name='zksync_era_testnet_labels')
    op.drop_index(op.f('ix_zksync_era_testnet_labels_block_timestamp'), table_name='zksync_era_testnet_labels')
    op.drop_index(op.f('ix_zksync_era_testnet_labels_block_number'), table_name='zksync_era_testnet_labels')
    op.drop_index('ix_zksync_era_testnet_labels_address_block_timestamp', table_name='zksync_era_testnet_labels')
    op.drop_index('ix_zksync_era_testnet_labels_address_block_number', table_name='zksync_era_testnet_labels')
    op.drop_index(op.f('ix_zksync_era_testnet_labels_address'), table_name='zksync_era_testnet_labels')
    op.drop_table('zksync_era_testnet_labels')
    op.drop_index(op.f('ix_zksync_era_testnet_blocks_timestamp'), table_name='zksync_era_testnet_blocks')
    op.drop_index(op.f('ix_zksync_era_testnet_blocks_hash'), table_name='zksync_era_testnet_blocks')
    op.drop_index(op.f('ix_zksync_era_testnet_blocks_block_number'), table_name='zksync_era_testnet_blocks')
    op.drop_table('zksync_era_testnet_blocks')
    # ### end Alembic commands ###
