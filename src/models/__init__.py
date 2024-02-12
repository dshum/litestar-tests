from typing import Any

from advanced_alchemy.base import UUIDBase
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase

from models.user import User
from models.topic import Topic
from models.test import Test
from models.question import Question
from models.model_action_log import ModelActionLog
from models.request_log import RequestLog
from models.user_test import UserTest
from models.password_reset import PasswordReset
