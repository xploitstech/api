"""Call request types and Metatx requesters

Revision ID: b4257b10daaf
Revises: dedd8a7d0624
Create Date: 2023-08-02 18:28:14.724453

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'b4257b10daaf'
down_revision = 'dedd8a7d0624'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # Blockchains
    op.create_table('blockchains',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=False),
    sa.Column('chain_id', sa.Integer(), nullable=False),
    sa.Column('testnet', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_blockchains')),
    sa.UniqueConstraint('id', name=op.f('uq_blockchains_id'))
    )

    op.create_index(op.f('ix_blockchains_chain_id'), 'blockchains', ['chain_id'], unique=False)
    op.create_index(op.f('ix_blockchains_name'), 'blockchains', ['name'], unique=True)
    
    op.add_column('registered_contracts', sa.Column('blockchain_id', sa.UUID(), nullable=True))
    op.create_foreign_key(op.f('fk_registered_contracts_blockchain_id_blockchains'), 'registered_contracts', 'blockchains', ['blockchain_id'], ['id'], ondelete='CASCADE')

    # Manual - Start
    op.execute(f"INSERT INTO blockchains (id, name, chain_id, testnet) VALUES ('{str(uuid.uuid4())}', 'ethereum', 1, FALSE),('{str(uuid.uuid4())}', 'polygon', 137, FALSE),('{str(uuid.uuid4())}', 'mumbai', 80001, TRUE),('{str(uuid.uuid4())}', 'wyrm', 322, FALSE),('{str(uuid.uuid4())}', 'zksync_era', 324, FALSE),('{str(uuid.uuid4())}', 'zksync_era_testnet', 280, TRUE),('{str(uuid.uuid4())}', 'gnosis', 100, FALSE);")
    op.execute("UPDATE registered_contracts SET blockchain_id = (SELECT id FROM blockchains WHERE blockchains.name = registered_contracts.blockchain);")
    op.alter_column("registered_contracts", "blockchain_id", nullable=False)
    # Manual - End

    op.drop_constraint('uq_registered_contracts_blockchain', 'registered_contracts', type_='unique')
    op.drop_index('ix_registered_contracts_blockchain', table_name='registered_contracts')
    op.drop_column('registered_contracts', 'blockchain')

    # Types
    op.create_table('call_request_types',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('request_type', sa.VARCHAR(length=128), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('required_params', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('method', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_call_request_types')),
    sa.UniqueConstraint('id', name=op.f('uq_call_request_types_id'))
    )

    op.create_index(op.f('ix_call_request_types_request_type'), 'call_request_types', ['request_type'], unique=True)

    op.add_column('call_requests', sa.Column('call_request_type_id', sa.UUID(), nullable=True))
    op.create_foreign_key(op.f('fk_call_requests_call_request_type_id_call_request_types'), 'call_requests', 'call_request_types', ['call_request_type_id'], ['id'], ondelete='CASCADE')

    # Manual - Start
    op.execute(f"INSERT INTO call_request_types (id, request_type, description, required_params, method) VALUES ('{str(uuid.uuid4())}', 'raw', 'A generic smart contract. You can ask users to submit arbitrary calldata to this contract.',ARRAY ['calldata'],''),('{str(uuid.uuid4())}', 'dropper-v0.2.0', 'A Dropper v0.2.0 contract. You can authorize users to submit claims against this contract.',ARRAY ['dropId','requestID','blockDeadline','amount','signer','signature'],'claim');")
    op.execute("UPDATE call_requests SET call_request_type_id = (SELECT call_request_types.id FROM call_request_types INNER JOIN registered_contracts ON call_requests.registered_contract_id = registered_contracts.id WHERE call_request_types.request_type = registered_contracts.contract_type);")
    op.alter_column("call_requests", "call_request_type_id", nullable=False)
    op.alter_column("call_request_types", "required_params", nullable=False)
    op.alter_column("call_request_types", "method", nullable=False)
    # Manual - End

    op.drop_index('ix_registered_contracts_contract_type', table_name='registered_contracts')
    op.drop_column('registered_contracts', 'contract_type')

    # Holders
    op.create_table('metatx_requesters',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', statement_timestamp())"), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_metatx_requesters')),
    sa.UniqueConstraint('id', name=op.f('uq_metatx_requesters_id'))
    )

    op.add_column('call_requests', sa.Column('metatx_requester_id', sa.UUID(), nullable=True))
    op.create_foreign_key(op.f('fk_call_requests_metatx_requester_id_metatx_requesters'), 'call_requests', 'metatx_requesters', ['metatx_requester_id'], ['id'], ondelete='CASCADE')
    op.add_column('registered_contracts', sa.Column('metatx_requester_id', sa.UUID(), nullable=True))
    op.create_foreign_key(op.f('fk_registered_contracts_metatx_requester_id_metatx_requesters'), 'registered_contracts', 'metatx_requesters', ['metatx_requester_id'], ['id'], ondelete='CASCADE')

    # Manual - Start
    op.execute("INSERT INTO metatx_requesters (id) SELECT DISTINCT moonstream_user_id FROM registered_contracts ON CONFLICT (id) DO NOTHING;")
    op.execute("INSERT INTO metatx_requesters (id) SELECT DISTINCT moonstream_user_id FROM call_requests ON CONFLICT (id) DO NOTHING;")
    op.execute("UPDATE registered_contracts SET metatx_requester_id = moonstream_user_id;")
    op.execute("UPDATE call_requests SET metatx_requester_id = moonstream_user_id;")
    op.alter_column("call_requests", "metatx_requester_id", nullable=False)
    op.alter_column("registered_contracts", "metatx_requester_id", nullable=False)
    # Manual - End

    op.drop_index('ix_call_requests_moonstream_user_id', table_name='call_requests')
    op.drop_column('call_requests', 'moonstream_user_id')
    op.drop_index('ix_registered_contracts_moonstream_user_id', table_name='registered_contracts')
    op.drop_column('registered_contracts', 'moonstream_user_id')

    # Other
    op.create_unique_constraint(op.f('uq_registered_contracts_blockchain_id'), 'registered_contracts', ['blockchain_id', 'metatx_requester_id', 'address'])

    op.create_unique_constraint(op.f('uq_call_requests_id'), 'call_requests', ['id'])
    op.create_unique_constraint(op.f('uq_registered_contracts_id'), 'registered_contracts', ['id'])
    op.create_unique_constraint(op.f('uq_leaderboard_scores_id'), 'leaderboard_scores', ['id'])
    op.create_unique_constraint(op.f('uq_leaderboards_id'), 'leaderboards', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # Blockchains
    op.add_column('registered_contracts', sa.Column('blockchain', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.create_index('ix_registered_contracts_blockchain', 'registered_contracts', ['blockchain'], unique=False)

    # Manual - Start
    op.execute("UPDATE registered_contracts SET blockchain = (SELECT blockchains.name FROM blockchains WHERE blockchains.id = registered_contracts.blockchain_id);")
    op.alter_column("registered_contracts", "blockchain", nullable=False)
    # Manual - End

    op.drop_constraint(op.f('fk_registered_contracts_blockchain_id_blockchains'), 'registered_contracts', type_='foreignkey')
    op.drop_constraint(op.f('uq_registered_contracts_blockchain_id'), 'registered_contracts', type_='unique')
    op.drop_column('registered_contracts', 'blockchain_id')
    
    op.drop_index(op.f('ix_blockchains_name'), table_name='blockchains')
    op.drop_index(op.f('ix_blockchains_chain_id'), table_name='blockchains')
    op.drop_table('blockchains')

    # Types
    op.add_column('registered_contracts', sa.Column('contract_type', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.create_index('ix_registered_contracts_contract_type', 'registered_contracts', ['contract_type'], unique=False)

    # Manual - Start
    # Hardcoded to set `dropper-v0.2.0`
    op.execute("UPDATE registered_contracts SET contract_type = 'dropper-v0.2.0';")
    op.alter_column("registered_contracts", "contract_type", nullable=False)
    # Manual - End

    op.drop_constraint(op.f('fk_call_requests_call_request_type_id_call_request_types'), 'call_requests', type_='foreignkey')
    op.drop_column('call_requests', 'call_request_type_id')

    op.drop_index(op.f('ix_call_request_types_request_type'), table_name='call_request_types')
    op.drop_table('call_request_types')

    # Holders
    op.add_column('registered_contracts', sa.Column('moonstream_user_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_index('ix_registered_contracts_moonstream_user_id', 'registered_contracts', ['moonstream_user_id'], unique=False)
    op.add_column('call_requests', sa.Column('moonstream_user_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_index('ix_call_requests_moonstream_user_id', 'call_requests', ['moonstream_user_id'], unique=False)

    # Manual - Start
    op.execute("UPDATE registered_contracts SET moonstream_user_id = metatx_requester_id;")
    op.execute("UPDATE call_requests SET moonstream_user_id = metatx_requester_id;")
    op.alter_column("registered_contracts", "moonstream_user_id", nullable=False)
    op.alter_column("call_requests", "moonstream_user_id", nullable=False)
    # Manual - End

    op.drop_constraint(op.f('fk_registered_contracts_metatx_requester_id_metatx_requesters'), 'registered_contracts', type_='foreignkey')
    op.drop_column('registered_contracts', 'metatx_requester_id')
    op.drop_constraint(op.f('fk_call_requests_metatx_requester_id_metatx_requesters'), 'call_requests', type_='foreignkey')
    op.drop_column('call_requests', 'metatx_requester_id')

    op.drop_table('metatx_requesters')

    # Other
    op.create_unique_constraint('uq_registered_contracts_blockchain', 'registered_contracts', ['blockchain', 'moonstream_user_id', 'address', 'contract_type'])
    
    # ### end Alembic commands ###
