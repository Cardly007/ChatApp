"""ajout des autres tables dans la BD

Revision ID: 796dd40e791e
Revises: 3b7f4edfef30
Create Date: 2023-12-27 11:34:21.029437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '796dd40e791e'
down_revision = '3b7f4edfef30'
branch_labels = None
depends_on = None


def upgrade():
    # Ne rien faire dans cette fonction si vous ne souhaitez pas créer de nouvelles tables.
    pass

# def upgrade():
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.create_table('chat_room',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('room_name', sa.String(length=50), nullable=False),
#     sa.Column('created_at', sa.DateTime(), nullable=True),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_table('message',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('salle_id', sa.Integer(), nullable=False),
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('content', sa.Text(), nullable=False),
#     sa.Column('date_et_heure', sa.DateTime(), nullable=True),
#     sa.Column('reponse_a', sa.Integer(), nullable=True),
#     sa.ForeignKeyConstraint(['reponse_a'], ['message.id'], ),
#     sa.ForeignKeyConstraint(['salle_id'], ['chat_room.id'], ),
#     sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_table('online_status',
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('Est_en_line', sa.Boolean(), nullable=True),
#     sa.Column('last_online_at', sa.DateTime(), nullable=True),
#     sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
#     sa.PrimaryKeyConstraint('user_id')
#     )
#     op.create_table('private_message',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('sender_id', sa.Integer(), nullable=False),
#     sa.Column('receiver_id', sa.Integer(), nullable=False),
#     sa.Column('content', sa.Text(), nullable=False),
#     sa.Column('date_et_heure', sa.DateTime(), nullable=True),
#     sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ),
#     sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_table('file',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('message_id', sa.Integer(), nullable=False),
#     sa.Column('chemin_file', sa.String(length=255), nullable=False),
#     sa.Column('file_type', sa.String(length=50), nullable=False),
#     sa.ForeignKeyConstraint(['message_id'], ['message.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     with op.batch_alter_table('user', schema=None) as batch_op:
#         batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=False))
#         batch_op.add_column(sa.Column('photo_profil', sa.String(length=255), nullable=True))
#         batch_op.add_column(sa.Column('bio', sa.Text(), nullable=True))
#         batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # Cette fonction est vide car nous ne voulons pas effectuer de changements lors de la rétrogradation
    pass

# def downgrade():
#     # ### commands auto generated by Alembic - please adjust! ###
#     with op.batch_alter_table('user', schema=None) as batch_op:
#         batch_op.drop_constraint(None, type_='unique')
#         batch_op.drop_column('bio')
#         batch_op.drop_column('photo_profil')
#         batch_op.drop_column('email')

#     op.drop_table('file')
#     op.drop_table('private_message')
#     op.drop_table('online_status')
#     op.drop_table('message')
#     op.drop_table('chat_room')
#     # ### end Alembic commands ###
