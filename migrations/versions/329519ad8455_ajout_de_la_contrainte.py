"""ajout de la contrainte

Revision ID: 329519ad8455
Revises: c86656799566
Create Date: 2023-12-29 01:45:35.233001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '329519ad8455'
down_revision = 'c86656799566'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('online_status', schema=None) as batch_op:
        # Ajoutez la clé étrangère avec un nom explicite
        batch_op.create_foreign_key(
            'fk_online_status_user_id',  # Nom de la contrainte
            'user',                       # Nom de la table de référence
            ['user_id'],                  # Colonne locale
            ['id'],                       # Colonne distante
        )

def downgrade():
    with op.batch_alter_table('online_status', schema=None) as batch_op:
        # Supprimez la clé étrangère avec le même nom
        batch_op.drop_constraint('fk_online_status_user_id', type_='foreignkey')

    with op.batch_alter_table('online_status') as batch_op:
        batch_op.drop_column('user_id')