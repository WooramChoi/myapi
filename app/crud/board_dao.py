from models.board import Board
from schemas.board_schema import BoardAdd, BoardSearch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from logger import get_logger
logger = get_logger()

async def find_board_one(session: AsyncSession, seq_board: int):
    query = select(Board).where(Board.seq_board == seq_board)
    rslt = await session.scalar(query)
    return rslt

async def find_board(session: AsyncSession, board_search: BoardSearch):
    query = select(Board)
    rslt = await session.scalars(query)
    return rslt.all()
        
async def add_board(session: AsyncSession, board_add: BoardAdd):
    board = Board(**board_add.__dict__)
    session.add(board)
    return board