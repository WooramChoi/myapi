# "launch.json" 을 실행할 경우: app 를 include 하기 위해 app directory 를 append
import sys, os
if __name__ != "__main__":
    sys.path.append(os.path.join(os.getcwd(), 'app'))

from typing import Union
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from database.datasource import init_database, close_database
import routers
import uvicorn
import aio_pika
import asyncio
from logger import get_logger

logger = get_logger()

async def get_rabbitmq_connection():
    """RabbitMQ Connection 객체 생성

    Returns:
        type: AbstractRobustConnection
    """
    return await aio_pika.connect_robust('amqp://my-rabbit')

async def consume_messages():
    """RabbitMQ 메시지 Consumer
    """
    connection = await get_rabbitmq_connection()

    async with connection:
        channel = await connection.channel()

        # 수신할 Queue 지정
        queue = await channel.declare_queue('api', durable=True)

        async for message in queue:
            async with message.process():
                msg = message.body.decode()
                logger.info(f'Received: {msg}')

                # (테스트 코드) "inspect" Queue 에 메시지 전송
                await channel.default_exchange.publish(aio_pika.Message(body=f'API Received [{msg}]'.encode()), routing_key='inspect')

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('On StartUp')

    logger.info('Init Database')
    await init_database()
    logger.info('Init Database Done')

    logger.info('Init RabbitMQ')
    try:
        app.state.rabbitmq_connection = await get_rabbitmq_connection()
        logger.info('Ready to Consuming')
        asyncio.create_task(consume_messages()) # async job 을 asyncio 에 등록
        logger.info('Ready to Consuming Done')
    except:
        logger.warning('Init RabbitMQ Server Not Responsed')
    logger.info('Init RabbitMQ Done')

    yield
    logger.info('On Shutdown')

    logger.info('Close Database')
    await close_database()
    logger.info('Close Database Done')

    logger.info('Close RabbitMQ Connection')
    try:
        await app.state.rabbitmq_connection.close()
    except:
        logger.warning('Init RabbitMQ Server Not Responsed')
    logger.info('Close RabbitMQ Connection Done')

    logger.info('###################')

app = FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f'RequestValidationError')

    method = request.method
    url: str
    if method == 'GET':
        url = f'{request.url}?{request.query_params}'
    else:
        url = request.url
        
    logger.error(f'[{method}] {url}')
    if method != 'GET':
        logger.debug(exc.body)

    return JSONResponse(status_code=422, content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}))

app.include_router(routers.board_router)

@app.get("/")
async def read_root():
    logger.info('root controller')
    return {"msg": "Hello, World!"}

def main():
    uvicorn.run(app, log_level="debug", host='0.0.0.0', port=8001)

if __name__ == '__main__':
    main()