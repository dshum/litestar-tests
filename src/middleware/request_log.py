from litestar import Request, Response


async def log_request_handler(request: Request) -> None:
    # db_engine = request.app.state.db_engine
    # async with async_sessionmaker(bind=db_engine) as session:
    #     log_service = RequestLogService(session=session, request=request)
    #     await log_service.log()
    pass


async def after_request(response: Response) -> Response:
    return response


async def after_response(request: Request) -> None:
    pass
