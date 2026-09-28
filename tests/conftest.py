"""
pytest 全域 fixtures — 使用 In-Memory SQLite 隔離測試環境
不依賴任何外部資料庫或環境變數
"""

import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool


# ── In-Memory SQLite Engine ───────────────────────────────────────────────────
# connect_args={"check_same_thread": False}：允許跨 thread 使用（SQLite 限制）
# StaticPool：確保整個測試期間共用同一個 in-memory 連線，不會在 fixture 間消失
TEST_DATABASE_URL = "sqlite://"


@pytest.fixture(name="engine", scope="session")
def engine_fixture():
    """建立測試用 SQLite In-Memory engine（整個 session 共用）"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # 所有 SQLModel Table 建立（在 models 被 import 後才有 metadata）
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine):
    """
    每個測試函式都有獨立的 Session。
    測試結束後 rollback，確保測試間完全隔離。
    """
    with Session(engine) as session:
        yield session
        session.rollback()
