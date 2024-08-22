from fastapi import APIRouter, Depends, Response, status
from database.datasource import get_async_session
from crud.board_dao import find_board, add_board, find_board_one
from schemas.board_schema import BoardAdd, BoardDetails, BoardSearch
from logger import get_logger

logger = get_logger()

router = APIRouter()

@router.get("/boards")
async def board_list(board_search: BoardSearch = Depends(), session = Depends(get_async_session)):

    boards = await find_board(session, board_search)

    list_board = []
    for board in boards:
        board_detail = BoardDetails(**board.__dict__)
        board_detail.content_summary = board.plain_text[0:20] if board.plain_text else None
        list_board.append(board_detail)

    return list_board

@router.post("/boards")
async def board_add(board_add: BoardAdd, response: Response, session = Depends(get_async_session)):

    # session.begin() 으로 감싸인 구문은 Transaction 영역
    async with session.begin():
        board = await add_board(session, board_add)
    
    session.refresh(board)
    logger.debug(f'Created [{board.seq_board}]')

    response.status_code=status.HTTP_201_CREATED
    response.headers.append('location', f'/boards/{board.seq_board}')
    return response

@router.get("/boards/{seq_board}")
async def board_details(seq_board: int, session = Depends(get_async_session)):

    board = await find_board_one(session, seq_board)

    board_detail = BoardDetails(**board.__dict__)
    return board_detail

@router.patch("/boards/{seq_board}")
async def board_modify(seq_board: int, session = Depends(get_async_session)):
    
    pass