from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request

from app.core.deps import CurrentUser, DbSession
from app.core.ratelimit import rate_limit
from app.modules.reminders import service
from app.modules.reminders.schemas import (
    ActionIn,
    ActionResult,
    PushConfig,
    SettingsIn,
    SettingsOut,
    SubscriptionIn,
    SubscriptionOut,
    TestResult,
)
from app.shared.push import get_push_sender, vapid_keys

router = APIRouter(prefix="/push", tags=["reminders"])


@router.get("/config", response_model=PushConfig)
async def config(user: CurrentUser):
    return PushConfig(public_key=vapid_keys().public_key, provider=get_push_sender().name)


@router.get("/subscriptions", response_model=list[SubscriptionOut])
async def list_subscriptions(user: CurrentUser, session: DbSession):
    return await service.list_subscriptions(session, user.id)


@router.post(
    "/subscriptions",
    response_model=SubscriptionOut,
    status_code=201,
    dependencies=[Depends(rate_limit("push:subscribe", 20, 3600))],
)
async def subscribe(data: SubscriptionIn, request: Request, user: CurrentUser, session: DbSession):
    out = await service.subscribe(session, user, data, request.headers.get("user-agent"))
    await session.commit()
    return out


@router.delete("/subscriptions", status_code=204)
async def unsubscribe(
    user: CurrentUser, session: DbSession, endpoint: str = Query(min_length=10, max_length=2000)
):
    await service.unsubscribe(session, user.id, endpoint)
    await session.commit()


@router.get("/settings", response_model=SettingsOut)
async def get_settings(user: CurrentUser, session: DbSession):
    return await service.get_settings_for(session, user.id)


@router.put("/settings", response_model=SettingsOut)
async def put_settings(data: SettingsIn, user: CurrentUser, session: DbSession):
    out = await service.update_settings(session, user.id, data)
    await session.commit()
    return out


@router.post(
    "/test", response_model=TestResult, dependencies=[Depends(rate_limit("push:test", 10, 600))]
)
async def test(user: CurrentUser, session: DbSession):
    sent, removed = await service.send_test(session, user)
    await session.commit()
    return TestResult(sent=sent, removed=removed)


@router.post(
    "/actions",
    response_model=ActionResult,
    dependencies=[Depends(rate_limit("push:action", 60, 60, by="ip"))],
)
async def action(data: ActionIn, session: DbSession):
    """Called by the service worker from a notification button; the token is the credential."""
    updated = await service.apply_action(session, data.token, data.action)
    await session.commit()
    return ActionResult(updated=updated)
