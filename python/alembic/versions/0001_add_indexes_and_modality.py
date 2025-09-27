from alembic import op
import sqlalchemy as sa

revision = '0001_add_indexes_and_modality'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('samples') as batch_op:
        batch_op.add_column(sa.Column('modality', sa.Text(), nullable=True))
        batch_op.create_index('idx_samples_source', ['source'])
    with op.batch_alter_table('studies') as batch_op:
        batch_op.create_index('idx_studies_source', ['source'])

def downgrade():
    with op.batch_alter_table('samples') as batch_op:
        batch_op.drop_index('idx_samples_source')
        batch_op.drop_column('modality')
    with op.batch_alter_table('studies') as batch_op:
        batch_op.drop_index('idx_studies_source')
